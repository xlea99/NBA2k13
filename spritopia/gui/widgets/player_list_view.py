"""
Shared, reusable list view for displaying players.

Renders a sortable table with [optional ID] · Name · Archetype · Rarity columns
and a single text filter that matches against name + archetype + rarity.

Designed to be used as the core list rendering primitive for any screen that
needs a "list of players": Roster Manager (both panes), and eventually a
refactored PlayerFinderWidget. Bespoke filter UIs (operator-per-field, game
constraint awareness, etc.) belong in the wrapper, not here.
"""

from dataclasses import dataclass
from typing import Optional, List, Callable

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)

from spritopia.gui.theme import COLORS, get_archetype_style, get_rarity_style


@dataclass
class PlayerListEntry:
    """A single row in a PlayerListView."""
    player: object         # Player dict-like (must support indexing for First_Name etc.)
    id_label: Optional[str] = None    # Optional left-most label, e.g. "#001" or "S-1234"
    extra_data: Optional[object] = None  # Free-form payload returned via signals (e.g. RosterID)
    pending_state: Optional[str] = None  # None | "add" | "remove" — visual overlay only


class _NumericSortItem(QTableWidgetItem):
    """QTableWidgetItem that sorts by a numeric key instead of display string.

    QTableWidget's default sort is by display text — for raw integer SpriteIDs
    that gives the classic '0, 1, 10, 100, 101, 11' alphabetical-ordering
    surprise. We override __lt__ to compare numerically when both items expose
    a numeric sort key.
    """
    def __init__(self, display_text: str, sort_value):
        super().__init__(display_text)
        self._sort_value = sort_value

    def __lt__(self, other):
        if isinstance(other, _NumericSortItem):
            return self._sort_value < other._sort_value
        return super().__lt__(other)


def _try_extract_int(label: Optional[str]):
    """Best-effort parse the first integer found in a label like '#001' or '12'.

    Returns the int on success, or None if no digits are present.
    """
    if not label:
        return None
    digits = "".join(ch for ch in label if ch.isdigit())
    if not digits:
        return None
    try:
        return int(digits)
    except ValueError:
        return None


class PlayerListView(QWidget):
    """
    A simple, focused list of players with text filter + selection.

    Signals:
        selection_changed(PlayerListEntry|None) — fired when the selected row changes
        entry_double_clicked(PlayerListEntry) — fired on double-click (commonly used
            as a shortcut for the primary action, e.g. "add to roster")
    """

    selection_changed = Signal(object)         # PlayerListEntry or None
    entry_double_clicked = Signal(object)      # PlayerListEntry

    def __init__(self, *, show_id_column: bool = False, id_header: str = "#",
                 placeholder: str = "Search…", parent=None):
        super().__init__(parent)
        self._show_id_column = show_id_column
        self._id_header = id_header
        self._all_entries: List[PlayerListEntry] = []
        self._setup_ui(placeholder)

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self, placeholder: str):
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(6)

        # Header row: filter input + count label
        header_row = QHBoxLayout()
        header_row.setSpacing(8)

        self._filter = QLineEdit()
        self._filter.setPlaceholderText(placeholder)
        self._filter.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{ border-color: {COLORS['accent_primary']}; }}
        """)
        self._filter.textChanged.connect(self._apply_filter)
        header_row.addWidget(self._filter, stretch=1)

        self._count_lbl = QLabel("0")
        self._count_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        header_row.addWidget(self._count_lbl)

        lo.addLayout(header_row)

        # Table
        cols = []
        if self._show_id_column:
            cols.append(self._id_header)
        cols += ["Name", "Arch", "Rarity"]

        self._table = QTableWidget()
        self._table.setColumnCount(len(cols))
        self._table.setHorizontalHeaderLabels(cols)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSortingEnabled(True)
        self._table.setShowGrid(False)
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                gridline-color: {COLORS['border_dark']};
                color: {COLORS['text_primary']};
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 4px 8px;
                border-bottom: 1px solid {COLORS['border_dark']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent_primary']};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_secondary']};
                padding: 6px 8px;
                border: none;
                border-bottom: 1px solid {COLORS['border_dark']};
                font-size: 11px;
                font-weight: bold;
            }}
        """)

        header = self._table.horizontalHeader()
        if self._show_id_column:
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)            # Name
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)   # Arch
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)   # Rarity
        else:
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self._table.itemSelectionChanged.connect(self._on_selection_changed)
        self._table.itemDoubleClicked.connect(self._on_double_click)

        lo.addWidget(self._table, stretch=1)

    # ── Public API ────────────────────────────────────────────────────────────

    def set_entries(self, entries: List[PlayerListEntry]):
        """Replace the full list of entries. Re-applies the current filter."""
        self._all_entries = list(entries)
        self._apply_filter()

    def selected_entry(self) -> Optional[PlayerListEntry]:
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return None
        idx = rows[0].row()
        item = self._table.item(idx, 0)
        if item is None:
            return None
        return item.data(Qt.UserRole)

    def clear_selection(self):
        self._table.clearSelection()

    # ── Filter / render ───────────────────────────────────────────────────────

    def _apply_filter(self, *_):
        query = self._filter.text().strip().lower()
        if query:
            visible = [e for e in self._all_entries if self._entry_matches(e, query)]
        else:
            visible = list(self._all_entries)

        self._render(visible)
        total = len(self._all_entries)
        shown = len(visible)
        if shown == total:
            self._count_lbl.setText(f"{total}")
        else:
            self._count_lbl.setText(f"{shown} / {total}")

    def _entry_matches(self, entry: PlayerListEntry, query: str) -> bool:
        p = entry.player
        first = (p["First_Name"] or "").lower()
        last = (p["Last_Name"] or "").lower()
        arch = (p["Archetype_Name"] or "").lower()
        rarity = str(p["Rarity"] or "").lower()
        if query in first or query in last or query in f"{first} {last}".strip():
            return True
        if query in arch or query in rarity:
            return True
        if entry.id_label and query in entry.id_label.lower():
            return True
        return False

    def _render(self, entries: List[PlayerListEntry]):
        # Batch paint events while we tear down and rebuild rows — for large
        # rosters (487+ rows × 4 columns) this is the difference between a
        # smooth swap and a multi-second hang as Qt repaints after each setItem.
        self._table.setUpdatesEnabled(False)
        # Disable sorting during repopulation to avoid scrambled rows
        self._table.setSortingEnabled(False)
        self._table.setRowCount(len(entries))

        for row_idx, entry in enumerate(entries):
            p = entry.player
            col = 0

            if self._show_id_column:
                label = entry.id_label or ""
                sort_key = _try_extract_int(label)
                if sort_key is not None:
                    id_item = _NumericSortItem(label, sort_key)
                else:
                    id_item = QTableWidgetItem(label)
                id_item.setData(Qt.UserRole, entry)
                id_item.setForeground(QColor(COLORS['text_muted']))
                self._table.setItem(row_idx, col, id_item)
                col += 1

            # Name (anchor for UserRole if no id column)
            first = p["First_Name"] or ""
            last = p["Last_Name"] or ""
            name_str = f"{first} {last}".strip() or "—"
            name_item = QTableWidgetItem(name_str)
            if not self._show_id_column:
                name_item.setData(Qt.UserRole, entry)
            self._table.setItem(row_idx, col, name_item)
            col += 1

            # Archetype (3-char abbrev with archetype color)
            arch_name = p["Archetype_Name"] or ""
            arch_item = QTableWidgetItem(arch_name[:3].upper() if arch_name else "?")
            arch_item.setTextAlignment(Qt.AlignCenter)
            arch_style = get_archetype_style(arch_name)
            if arch_style:
                arch_item.setForeground(QColor(arch_style["color"]))
            self._table.setItem(row_idx, col, arch_item)
            col += 1

            # Rarity (colored)
            rarity = p["Rarity"] or ""
            rarity_item = QTableWidgetItem(str(rarity))
            rarity_item.setTextAlignment(Qt.AlignCenter)
            rarity_style = get_rarity_style(rarity)
            if rarity_style:
                rarity_item.setForeground(QColor(rarity_style["color"]))
            self._table.setItem(row_idx, col, rarity_item)

            # Pending overlay — make queued ADDs and REMOVEs visually obvious
            # so the user can tell at a glance "this row is about to change."
            # Apply AFTER per-column foreground colors so the row's identity
            # (archetype/rarity colors) stays readable; pending state shows
            # via a strong background tint + a colored marker on the ID column,
            # plus strikethrough text for removes.
            if entry.pending_state in ("add", "remove"):
                if entry.pending_state == "add":
                    bg = QColor(40, 100, 60)         # clearly green
                    marker_text = "+"
                    marker_color = QColor("#34d399")  # bright green
                else:
                    bg = QColor(110, 40, 40)         # clearly red
                    marker_text = "×"
                    marker_color = QColor("#f87171")  # bright red

                for c in range(self._table.columnCount()):
                    item = self._table.item(row_idx, c)
                    if item is None:
                        continue
                    item.setBackground(bg)
                    if entry.pending_state == "remove":
                        f = item.font()
                        f.setStrikeOut(True)
                        item.setFont(f)

                # Prefix the ID column with a colored marker — most obvious
                # signal of "this is a pending change" at a glance.
                if self._show_id_column:
                    id_item = self._table.item(row_idx, 0)
                    if id_item is not None:
                        id_item.setText(f"{marker_text} {entry.id_label or ''}")
                        id_item.setForeground(marker_color)
                        f = id_item.font()
                        f.setBold(True)
                        # Keep strikethrough on remove; explicitly disable on add
                        # so a previously-rendered remove doesn't bleed through.
                        f.setStrikeOut(entry.pending_state == "remove")
                        id_item.setFont(f)

        self._table.setSortingEnabled(True)
        self._table.setUpdatesEnabled(True)

    # ── Internal slots ────────────────────────────────────────────────────────

    def _on_selection_changed(self):
        self.selection_changed.emit(self.selected_entry())

    def _on_double_click(self, item: QTableWidgetItem):
        # Find the UserRole anchor for this row
        anchor_col = 0  # if id column shown, anchor is col 0; otherwise col 0 (name)
        anchor = self._table.item(item.row(), anchor_col)
        if anchor is None:
            return
        entry = anchor.data(Qt.UserRole)
        if entry is not None:
            self.entry_double_clicked.emit(entry)
