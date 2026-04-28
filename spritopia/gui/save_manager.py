"""
Save Manager - Handles pending changes queue and batch saving.

Changes are queued and not applied until explicitly confirmed.
This prevents accidental data loss and allows grouping of changes.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional
from datetime import datetime

from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QFrame, QDialog, QScrollArea, QProgressDialog, QApplication, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from spritopia.gui.theme import COLORS
from spritopia.common.logger import log


class ChangeType(Enum):
    """Types of changes that can be queued."""
    ADD_PLAYER_TO_DB = "add_player_db"
    UPDATE_PLAYER_IN_DB = "update_player_db"
    DELETE_PLAYER_FROM_DB = "delete_player_db"
    ADD_PLAYER_TO_ROSTER = "add_player_roster"
    REMOVE_PLAYER_FROM_ROSTER = "remove_player_roster"
    SYNC_ROSTER_TO_ROS = "sync_roster_ros"


@dataclass
class PendingChange:
    """A single pending change in the queue."""
    change_type: ChangeType
    description: str  # Human-readable description
    data: Any  # The data needed to execute this change
    execute_fn: Callable  # Function to call to execute this change
    timestamp: datetime = field(default_factory=datetime.now)
    group_id: Optional[str] = None  # For grouping related changes


class PendingChangesManager(QObject):
    """
    Manages a queue of pending changes.

    Signals:
        changes_updated: Emitted when the pending changes list changes
        save_started: Emitted when save process begins
        save_progress: Emitted with (current, total) during save
        save_completed: Emitted when all changes are saved
        save_error: Emitted with error message if save fails
    """

    changes_updated = Signal()
    save_started = Signal()
    save_progress = Signal(int, int)  # current, total
    save_completed = Signal()
    save_error = Signal(str)

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        self._initialized = True
        self._pending_changes: List[PendingChange] = []
        self._is_saving = False

    @property
    def has_pending_changes(self) -> bool:
        return len(self._pending_changes) > 0

    @property
    def pending_count(self) -> int:
        return len(self._pending_changes)

    @property
    def is_saving(self) -> bool:
        return self._is_saving

    def add_change(self, change: PendingChange):
        """Add a change to the pending queue."""
        self._pending_changes.append(change)
        log.info(f"Queued change: {change.description}")
        self.changes_updated.emit()

    def add_player_to_db(self, player, execute_fn: Callable):
        """Queue adding a player to the database."""
        name = f"{player['First_Name'] or '???'} {player['Last_Name'] or '???'}"
        change = PendingChange(
            change_type=ChangeType.ADD_PLAYER_TO_DB,
            description=f"Add {name} to Players.db",
            data=player,
            execute_fn=execute_fn
        )
        self.add_change(change)

    def add_player_to_roster(self, player, roster_name: str, execute_fn: Callable):
        """Queue adding a player to a roster."""
        name = f"{player['First_Name'] or '???'} {player['Last_Name'] or '???'}"
        change = PendingChange(
            change_type=ChangeType.ADD_PLAYER_TO_ROSTER,
            description=f"Add {name} to {roster_name}.ROS",
            data={'player': player, 'roster': roster_name},
            execute_fn=execute_fn
        )
        self.add_change(change)

    def sync_roster(self, roster_name: str, execute_fn: Callable):
        """Queue syncing a roster to .ROS file via RedMC."""
        change = PendingChange(
            change_type=ChangeType.SYNC_ROSTER_TO_ROS,
            description=f"Sync {roster_name} via RedMC",
            data={'roster': roster_name},
            execute_fn=execute_fn
        )
        self.add_change(change)

    def get_changelog(self) -> List[str]:
        """Get list of human-readable change descriptions."""
        return [f"• {c.description}" for c in self._pending_changes]

    def get_changelog_by_type(self) -> dict:
        """Get changes organized by type."""
        by_type = {}
        for change in self._pending_changes:
            type_name = change.change_type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(change.description)
        return by_type

    def clear_all(self):
        """Clear all pending changes without executing them."""
        self._pending_changes.clear()
        self.changes_updated.emit()

    def execute_all(self, parent_widget=None) -> bool:
        """
        Execute all pending changes.

        Returns True if all changes succeeded, False otherwise.
        """
        if not self._pending_changes:
            return True

        if self._is_saving:
            return False

        self._is_saving = True
        self.save_started.emit()

        total = len(self._pending_changes)
        errors = []

        # Create progress dialog
        if parent_widget:
            progress = QProgressDialog(
                "Saving changes...",
                None,  # No cancel
                0,
                total,
                parent_widget
            )
            progress.setWindowTitle("Saving")
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            progress.show()
            QApplication.processEvents()

        for i, change in enumerate(self._pending_changes[:]):  # Copy list to iterate
            try:
                self.save_progress.emit(i + 1, total)
                if parent_widget:
                    progress.setValue(i)
                    progress.setLabelText(f"Saving: {change.description}")
                    QApplication.processEvents()

                # Execute the change
                change.execute_fn(change.data)
                log.info(f"Executed: {change.description}")

            except Exception as e:
                error_msg = f"Failed: {change.description} - {str(e)}"
                log.exception(error_msg)
                errors.append(error_msg)

        if parent_widget:
            progress.close()

        # Clear the queue
        self._pending_changes.clear()
        self._is_saving = False

        if errors:
            self.save_error.emit("\n".join(errors))
            self.changes_updated.emit()
            return False
        else:
            self.save_completed.emit()
            self.changes_updated.emit()
            return True


def get_save_manager() -> PendingChangesManager:
    """Get the singleton save manager instance."""
    return PendingChangesManager()


class SaveButton(QWidget):
    """
    A save button that shows pending changes count and glows when there are changes.

    Hovering shows a changelog tooltip.
    Clicking executes all pending changes.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._glow_state = False
        self._glow_timer = QTimer(self)
        self._glow_timer.timeout.connect(self._toggle_glow)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Save button
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedHeight(36)
        self.save_btn.setMinimumWidth(100)
        self._update_button_style(has_changes=False)
        self.save_btn.clicked.connect(self._on_save_clicked)
        layout.addWidget(self.save_btn)

        # Pending count badge
        self.count_badge = QLabel("0")
        self.count_badge.setAlignment(Qt.AlignCenter)
        self.count_badge.setFixedSize(24, 24)
        self.count_badge.setStyleSheet(f"""
            background-color: {COLORS['accent_danger']};
            color: white;
            font-size: 11px;
            font-weight: bold;
            border-radius: 12px;
        """)
        self.count_badge.hide()
        layout.addWidget(self.count_badge)

    def _connect_signals(self):
        manager = get_save_manager()
        manager.changes_updated.connect(self._on_changes_updated)
        manager.save_started.connect(self._on_save_started)
        manager.save_completed.connect(self._on_save_completed)
        manager.save_error.connect(self._on_save_error)

    def _update_button_style(self, has_changes: bool, glow: bool = False):
        if has_changes:
            if glow:
                bg_color = COLORS['accent_warning']
                border = f"2px solid {COLORS['accent_success']}"
            else:
                bg_color = COLORS['accent_success']
                border = "none"
            self.save_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: white;
                    border: {border};
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: #0ea572;
                }}
                QPushButton:disabled {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text_muted']};
                }}
            """)
        else:
            self.save_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text_muted']};
                    border: none;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 6px;
                }}
            """)

    def _toggle_glow(self):
        self._glow_state = not self._glow_state
        manager = get_save_manager()
        self._update_button_style(manager.has_pending_changes, self._glow_state)

    def _on_changes_updated(self):
        manager = get_save_manager()
        count = manager.pending_count

        if count > 0:
            self.count_badge.setText(str(count))
            self.count_badge.show()
            self.save_btn.setEnabled(True)
            self._update_button_style(has_changes=True)

            # Build tooltip with changelog
            changelog = manager.get_changelog()
            if len(changelog) > 10:
                tooltip_lines = changelog[:10] + [f"... and {len(changelog) - 10} more"]
            else:
                tooltip_lines = changelog
            self.setToolTip("<b>Pending Changes:</b><br/>" + "<br/>".join(tooltip_lines))

            # Start glow animation
            if not self._glow_timer.isActive():
                self._glow_timer.start(800)
        else:
            self.count_badge.hide()
            self.save_btn.setEnabled(False)
            self._update_button_style(has_changes=False)
            self.setToolTip("No pending changes")
            self._glow_timer.stop()

    def _on_save_clicked(self):
        manager = get_save_manager()
        if manager.has_pending_changes:
            # Find parent window for modal dialog
            parent = self.window()
            manager.execute_all(parent_widget=parent)

    def _on_save_started(self):
        self.save_btn.setEnabled(False)
        self.save_btn.setText("Saving...")
        self._glow_timer.stop()

    def _on_save_completed(self):
        self.save_btn.setText("Save")
        self._on_changes_updated()

    def _on_save_error(self, error_msg: str):
        self.save_btn.setText("Save")
        self._on_changes_updated()
        log.error(f"Save error: {error_msg}")

        # Surface the failure to the user. The most actionable case is height-bucket
        # exhaustion ("Out of space to add more players to roster with this height: …"),
        # which we call out explicitly so the user knows to pick a different height.
        is_height_exhaustion = "Out of space to add more players to roster with this height" in error_msg
        if is_height_exhaustion:
            title = "Roster Height Bucket Full"
            preamble = (
                "One or more players couldn't be added to the roster because every "
                "height-adjustment slot for that height is already taken (max 254 players "
                "per RealHeight). Pick a different height for the affected player(s) and "
                "try saving again.\n\n"
            )
        else:
            title = "Save Failed"
            preamble = "One or more queued changes failed to save:\n\n"

        box = QMessageBox(self.window())
        box.setWindowTitle(title)
        box.setIcon(QMessageBox.Warning)
        box.setText(preamble + error_msg)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()


class SaveConfirmDialog(QDialog):
    """Dialog showing pending changes before saving."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Save")
        self.setMinimumSize(400, 300)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # Header
        header = QLabel("The following changes will be saved:")
        header.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(header)

        # Changelog scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: 1px solid #333; }")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(4)

        manager = get_save_manager()
        for desc in manager.get_changelog():
            label = QLabel(desc)
            label.setWordWrap(True)
            content_layout.addWidget(label)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll, stretch=1)

        # Warning about RedMC if applicable
        by_type = manager.get_changelog_by_type()
        if ChangeType.SYNC_ROSTER_TO_ROS.value in by_type:
            warning = QLabel("⚠️ This will use RedMC which takes over the screen. Do not interact with your computer until complete.")
            warning.setWordWrap(True)
            warning.setStyleSheet(f"color: {COLORS['accent_warning']}; padding: 8px;")
            layout.addWidget(warning)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save All")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_success']};
                color: white;
                padding: 8px 24px;
                font-weight: bold;
                border-radius: 4px;
            }}
        """)
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)
