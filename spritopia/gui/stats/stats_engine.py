"""
Stats Engine - Core calculation and aggregation logic for player statistics.

This module handles:
- Aggregating raw game stats into player career stats
- Calculating advanced metrics (efficiency, per-game averages, shooting splits)
- Filtering and sorting statistics
- Generating leaderboards
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import math


@dataclass
class PlayerCareerStats:
    """Aggregated career statistics for a single player."""
    sprite_id: int
    games_played: int = 0
    wins: int = 0
    losses: int = 0

    # Totals
    total_points: int = 0
    total_assists: int = 0
    total_offensive_rebounds: int = 0
    total_defensive_rebounds: int = 0
    total_steals: int = 0
    total_blocks: int = 0
    total_turnovers: int = 0
    total_fouls: int = 0
    total_dunks: int = 0
    total_layups: int = 0

    # Shooting
    insides_made: int = 0
    insides_attempted: int = 0
    threes_made: int = 0
    threes_attempted: int = 0

    # Ball handling time (seconds)
    ball_holding_in_play: float = 0.0
    ball_holding_out_of_play: float = 0.0

    # Points generated via assists
    total_points_per_assist: int = 0

    # Player info (populated after aggregation)
    first_name: str = ""
    last_name: str = ""
    archetype: str = ""
    rarity: str = ""
    faction: str = ""

    @property
    def total_rebounds(self) -> int:
        return self.total_offensive_rebounds + self.total_defensive_rebounds

    @property
    def win_pct(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.wins / self.games_played

    @property
    def ppg(self) -> float:
        """Points per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_points / self.games_played

    @property
    def apg(self) -> float:
        """Assists per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_assists / self.games_played

    @property
    def rpg(self) -> float:
        """Rebounds per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_rebounds / self.games_played

    @property
    def spg(self) -> float:
        """Steals per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_steals / self.games_played

    @property
    def bpg(self) -> float:
        """Blocks per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_blocks / self.games_played

    @property
    def tpg(self) -> float:
        """Turnovers per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_turnovers / self.games_played

    @property
    def fpg(self) -> float:
        """Fouls per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_fouls / self.games_played

    @property
    def orpg(self) -> float:
        """Offensive rebounds per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_offensive_rebounds / self.games_played

    @property
    def drpg(self) -> float:
        """Defensive rebounds per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_defensive_rebounds / self.games_played

    @property
    def dpg(self) -> float:
        """Dunks per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_dunks / self.games_played

    @property
    def lpg(self) -> float:
        """Layups per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_layups / self.games_played

    @property
    def fg_made(self) -> int:
        """Total field goals made (insides + threes)."""
        return self.insides_made + self.threes_made

    @property
    def fg_attempted(self) -> int:
        """Total field goals attempted."""
        return self.insides_attempted + self.threes_attempted

    @property
    def fg_pct(self) -> float:
        """Field goal percentage (all shots)."""
        if self.fg_attempted == 0:
            return 0.0
        return self.fg_made / self.fg_attempted

    @property
    def two_pt_pct(self) -> float:
        """Two-point (inside) field goal percentage."""
        if self.insides_attempted == 0:
            return 0.0
        return self.insides_made / self.insides_attempted

    @property
    def three_pt_pct(self) -> float:
        """Three-point percentage."""
        if self.threes_attempted == 0:
            return 0.0
        return self.threes_made / self.threes_attempted

    @property
    def efg_pct(self) -> float:
        """
        Effective field goal percentage.
        eFG% = (FGM + 0.5 * 3PM) / FGA
        Accounts for the extra value of three-pointers.
        """
        if self.fg_attempted == 0:
            return 0.0
        return (self.fg_made + 0.5 * self.threes_made) / self.fg_attempted

    @property
    def ts_pct(self) -> float:
        """
        True shooting percentage.
        TS% = PTS / (2 * (FGA + 0.44 * FTA))
        Since we don't have FTA, we approximate with: PTS / (2 * FGA)
        """
        if self.fg_attempted == 0:
            return 0.0
        return self.total_points / (2 * self.fg_attempted)

    @property
    def ast_to_ratio(self) -> float:
        """Assist to turnover ratio."""
        if self.total_turnovers == 0:
            return self.total_assists  # Perfect ratio
        return self.total_assists / self.total_turnovers

    @property
    def three_pt_rate(self) -> float:
        """Percentage of shots that are three-pointers."""
        if self.fg_attempted == 0:
            return 0.0
        return self.threes_attempted / self.fg_attempted

    @property
    def dunk_rate(self) -> float:
        """Percentage of inside shots that are dunks."""
        if self.insides_made == 0:
            return 0.0
        return self.total_dunks / self.insides_made

    @property
    def layup_rate(self) -> float:
        """Percentage of inside shots that are layups."""
        if self.insides_made == 0:
            return 0.0
        return self.total_layups / self.insides_made

    @property
    def ball_time_per_game(self) -> float:
        """Average seconds holding the ball per game."""
        if self.games_played == 0:
            return 0.0
        return (self.ball_holding_in_play + self.ball_holding_out_of_play) / self.games_played

    @property
    def points_created(self) -> int:
        """Total points created (own points + assisted points)."""
        return self.total_points + self.total_points_per_assist

    @property
    def points_created_per_game(self) -> float:
        """Points created per game."""
        if self.games_played == 0:
            return 0.0
        return self.points_created / self.games_played

    @property
    def efficiency_rating(self) -> float:
        """
        Custom efficiency rating (simplified PER-like metric).
        (PTS + REB + AST + STL + BLK - TO - Missed FG) / GP
        """
        if self.games_played == 0:
            return 0.0
        missed_fg = self.fg_attempted - self.fg_made
        return (
            self.total_points +
            self.total_rebounds +
            self.total_assists +
            self.total_steals +
            self.total_blocks -
            self.total_turnovers -
            missed_fg
        ) / self.games_played

    @property
    def game_score_avg(self) -> float:
        """
        Average game score (Hollinger's Game Score formula, simplified).
        GmSc = PTS + 0.4*FGM - 0.7*FGA - 0.4*(FTA-FTM) + 0.7*ORB + 0.3*DRB + STL + 0.7*AST + 0.7*BLK - 0.4*PF - TO
        Simplified without FT: PTS + 0.4*FGM - 0.7*FGA + 0.7*ORB + 0.3*DRB + STL + 0.7*AST + 0.7*BLK - 0.4*PF - TO
        """
        if self.games_played == 0:
            return 0.0
        total_game_score = (
            self.total_points +
            0.4 * self.fg_made -
            0.7 * self.fg_attempted +
            0.7 * self.total_offensive_rebounds +
            0.3 * self.total_defensive_rebounds +
            self.total_steals +
            0.7 * self.total_assists +
            0.7 * self.total_blocks -
            0.4 * self.total_fouls -
            self.total_turnovers
        )
        return total_game_score / self.games_played

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display purposes."""
        return {
            "sprite_id": self.sprite_id,
            "name": self.full_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "archetype": self.archetype,
            "rarity": self.rarity,
            "faction": self.faction,
            "games_played": self.games_played,
            "wins": self.wins,
            "losses": self.losses,
            "win_pct": self.win_pct,
            "ppg": self.ppg,
            "apg": self.apg,
            "rpg": self.rpg,
            "orpg": self.orpg,
            "drpg": self.drpg,
            "spg": self.spg,
            "bpg": self.bpg,
            "tpg": self.tpg,
            "fpg": self.fpg,
            "dpg": self.dpg,
            "lpg": self.lpg,
            "fg_pct": self.fg_pct,
            "two_pt_pct": self.two_pt_pct,
            "three_pt_pct": self.three_pt_pct,
            "efg_pct": self.efg_pct,
            "ts_pct": self.ts_pct,
            "ast_to_ratio": self.ast_to_ratio,
            "three_pt_rate": self.three_pt_rate,
            "dunk_rate": self.dunk_rate,
            "layup_rate": self.layup_rate,
            "efficiency_rating": self.efficiency_rating,
            "game_score_avg": self.game_score_avg,
            "points_created_per_game": self.points_created_per_game,
            "ball_time_per_game": self.ball_time_per_game,
            # Totals
            "total_points": self.total_points,
            "total_assists": self.total_assists,
            "total_rebounds": self.total_rebounds,
            "total_steals": self.total_steals,
            "total_blocks": self.total_blocks,
            "total_turnovers": self.total_turnovers,
            "fg_made": self.fg_made,
            "fg_attempted": self.fg_attempted,
            "threes_made": self.threes_made,
            "threes_attempted": self.threes_attempted,
        }


@dataclass
class GameRecord:
    """A single game record with all relevant info."""
    game_id: int
    play_date: str
    loaded_roster: str
    mode: int
    ballerz_score: int
    ringers_score: int
    player_slots: Dict[int, Dict[str, Any]] = field(default_factory=dict)

    @property
    def winner(self) -> str:
        if self.ballerz_score > self.ringers_score:
            return "Ballerz"
        elif self.ringers_score > self.ballerz_score:
            return "Ringers"
        return "Tie"

    @property
    def point_differential(self) -> int:
        return abs(self.ballerz_score - self.ringers_score)

    @property
    def total_points(self) -> int:
        return self.ballerz_score + self.ringers_score

    def get_team_players(self, team: str) -> List[Dict[str, Any]]:
        """Get players for a team (Ballerz = slots 0-4, Ringers = slots 5-9)."""
        if team.lower() == "ballerz":
            return [self.player_slots.get(i, {}) for i in range(5) if self.player_slots.get(i, {}).get("IsActive")]
        else:
            return [self.player_slots.get(i, {}) for i in range(5, 10) if self.player_slots.get(i, {}).get("IsActive")]


class StatsEngine:
    """
    Core engine for processing and analyzing game statistics.
    """

    def __init__(self, raw_stats: Dict[int, Dict], players_dict: Dict[int, Any]):
        """
        Initialize the stats engine.

        Args:
            raw_stats: The raw stats dictionary from data_storage.stats["Raw"]
            players_dict: Dictionary of player objects keyed by SpriteID
        """
        self._raw_stats = raw_stats
        self._players = players_dict
        self._career_stats: Dict[int, PlayerCareerStats] = {}
        self._games: List[GameRecord] = []

        self._process_stats()

    def _process_stats(self):
        """Process raw stats into usable formats."""
        self._games = []
        career_data = defaultdict(lambda: PlayerCareerStats(sprite_id=-1))

        for game_id, game_info in self._raw_stats.items():
            # Create game record
            game = GameRecord(
                game_id=game_id,
                play_date=game_info.get("PlayDate", ""),
                loaded_roster=game_info.get("LoadedRoster", ""),
                mode=game_info.get("Mode", 0),
                ballerz_score=game_info.get("BallerzScore", 0),
                ringers_score=game_info.get("RingersScore", 0),
                player_slots=game_info.get("PlayerSlots", {})
            )
            self._games.append(game)

            # Determine winning team
            winner = game.winner

            # Process each player slot
            for slot_id, slot_info in game.player_slots.items():
                if not slot_info.get("IsActive"):
                    continue

                sprite_id = slot_info.get("SpriteID", -1)
                if sprite_id is None or sprite_id < 0:
                    continue

                # Initialize career stats if needed
                if career_data[sprite_id].sprite_id == -1:
                    career_data[sprite_id].sprite_id = sprite_id

                stats = career_data[sprite_id]
                stats.games_played += 1

                # Determine win/loss
                is_ballerz = slot_id < 5
                if winner == "Ballerz" and is_ballerz:
                    stats.wins += 1
                elif winner == "Ringers" and not is_ballerz:
                    stats.wins += 1
                else:
                    stats.losses += 1

                # Accumulate stats
                stats.total_points += slot_info.get("Points", 0) or 0
                stats.total_assists += slot_info.get("AssistCount", 0) or 0
                stats.total_offensive_rebounds += slot_info.get("OffensiveRebounds", 0) or 0
                stats.total_defensive_rebounds += slot_info.get("DefensiveRebounds", 0) or 0
                stats.total_steals += slot_info.get("Steals", 0) or 0
                stats.total_blocks += slot_info.get("Blocks", 0) or 0
                stats.total_turnovers += slot_info.get("Turnovers", 0) or 0
                stats.total_fouls += slot_info.get("Fouls", 0) or 0
                stats.total_dunks += slot_info.get("Dunks", 0) or 0
                stats.total_layups += slot_info.get("Layups", 0) or 0
                stats.insides_made += slot_info.get("InsidesMade", 0) or 0
                stats.insides_attempted += slot_info.get("InsidesAttempted", 0) or 0
                stats.threes_made += slot_info.get("ThreesMade", 0) or 0
                stats.threes_attempted += slot_info.get("ThreesAttempted", 0) or 0
                stats.total_points_per_assist += slot_info.get("PointsPerAssist", 0) or 0
                stats.ball_holding_in_play += slot_info.get("BallHolding_InPlay", 0) or 0
                stats.ball_holding_out_of_play += slot_info.get("BallHolding_OutOfPlay", 0) or 0

        # Sort games by date (newest first), handling None dates
        self._games.sort(key=lambda g: g.play_date or "", reverse=True)

        # Populate player info
        for sprite_id, stats in career_data.items():
            if sprite_id in self._players:
                player = self._players[sprite_id]
                try:
                    stats.first_name = player["First_Name"] or ""
                    stats.last_name = player["Last_Name"] or ""
                    stats.archetype = player["Archetype_Name"] or ""
                    stats.rarity = player["Rarity"] or ""
                    stats.faction = player["Faction"] or ""
                except (KeyError, TypeError):
                    pass  # Player data not available

        self._career_stats = dict(career_data)

    def get_career_stats(self, sprite_id: int) -> Optional[PlayerCareerStats]:
        """Get career stats for a specific player."""
        return self._career_stats.get(sprite_id)

    def get_all_career_stats(self) -> List[PlayerCareerStats]:
        """Get all players' career stats."""
        return list(self._career_stats.values())

    def get_games(self) -> List[GameRecord]:
        """Get all games."""
        return self._games

    def get_leaderboard(
        self,
        stat: str,
        min_games: int = 1,
        limit: int = 10,
        archetype_filter: Optional[str] = None,
        rarity_filter: Optional[str] = None,
        ascending: bool = False
    ) -> List[Tuple[PlayerCareerStats, Any]]:
        """
        Get a leaderboard for a specific stat.

        Args:
            stat: The stat name (e.g., 'ppg', 'efficiency_rating')
            min_games: Minimum games played to qualify
            limit: Maximum number of results
            archetype_filter: Filter by archetype
            rarity_filter: Filter by rarity
            ascending: If True, sort ascending (for stats where lower is better)

        Returns:
            List of (PlayerCareerStats, stat_value) tuples
        """
        candidates = []

        for stats in self._career_stats.values():
            if stats.games_played < min_games:
                continue
            if archetype_filter and stats.archetype.lower() != archetype_filter.lower():
                continue
            if rarity_filter and stats.rarity.lower() != rarity_filter.lower():
                continue

            # Get the stat value
            stat_dict = stats.to_dict()
            if stat in stat_dict:
                value = stat_dict[stat]
            elif hasattr(stats, stat):
                value = getattr(stats, stat)
            else:
                continue

            candidates.append((stats, value))

        # Sort
        candidates.sort(key=lambda x: x[1] if x[1] is not None else -float('inf'), reverse=not ascending)

        return candidates[:limit]

    def get_archetype_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Get aggregate stats broken down by archetype."""
        breakdown = defaultdict(lambda: {
            "count": 0,
            "total_games": 0,
            "total_wins": 0,
            "total_points": 0,
            "total_assists": 0,
            "total_rebounds": 0,
            "total_steals": 0,
            "total_blocks": 0,
        })

        for stats in self._career_stats.values():
            if not stats.archetype:
                continue
            arch = breakdown[stats.archetype]
            arch["count"] += 1
            arch["total_games"] += stats.games_played
            arch["total_wins"] += stats.wins
            arch["total_points"] += stats.total_points
            arch["total_assists"] += stats.total_assists
            arch["total_rebounds"] += stats.total_rebounds
            arch["total_steals"] += stats.total_steals
            arch["total_blocks"] += stats.total_blocks

        # Calculate averages
        for arch, data in breakdown.items():
            if data["total_games"] > 0:
                data["ppg"] = data["total_points"] / data["total_games"]
                data["apg"] = data["total_assists"] / data["total_games"]
                data["rpg"] = data["total_rebounds"] / data["total_games"]
                data["spg"] = data["total_steals"] / data["total_games"]
                data["bpg"] = data["total_blocks"] / data["total_games"]
                data["win_pct"] = data["total_wins"] / data["total_games"]
            else:
                data["ppg"] = data["apg"] = data["rpg"] = data["spg"] = data["bpg"] = data["win_pct"] = 0

        return dict(breakdown)

    def get_rarity_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Get aggregate stats broken down by rarity."""
        breakdown = defaultdict(lambda: {
            "count": 0,
            "total_games": 0,
            "total_wins": 0,
            "total_points": 0,
            "efficiency_sum": 0.0,
        })

        for stats in self._career_stats.values():
            if not stats.rarity:
                continue
            rar = breakdown[stats.rarity]
            rar["count"] += 1
            rar["total_games"] += stats.games_played
            rar["total_wins"] += stats.wins
            rar["total_points"] += stats.total_points
            rar["efficiency_sum"] += stats.efficiency_rating * stats.games_played

        # Calculate averages
        for rar, data in breakdown.items():
            if data["total_games"] > 0:
                data["ppg"] = data["total_points"] / data["total_games"]
                data["win_pct"] = data["total_wins"] / data["total_games"]
                data["avg_efficiency"] = data["efficiency_sum"] / data["total_games"]
            else:
                data["ppg"] = data["win_pct"] = data["avg_efficiency"] = 0

        return dict(breakdown)

    def get_faction_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Get aggregate stats broken down by faction."""
        breakdown = defaultdict(lambda: {
            "count": 0,
            "total_games": 0,
            "total_wins": 0,
        })

        for stats in self._career_stats.values():
            if not stats.faction:
                continue
            fac = breakdown[stats.faction]
            fac["count"] += 1
            fac["total_games"] += stats.games_played
            fac["total_wins"] += stats.wins

        for fac, data in breakdown.items():
            if data["total_games"] > 0:
                data["win_pct"] = data["total_wins"] / data["total_games"]
            else:
                data["win_pct"] = 0

        return dict(breakdown)

    def get_global_stats(self) -> Dict[str, Any]:
        """Get global aggregate statistics."""
        total_games = len(self._games)
        total_players = len([s for s in self._career_stats.values() if s.games_played > 0])

        total_points = sum(g.total_points for g in self._games)
        total_ballerz_wins = sum(1 for g in self._games if g.winner == "Ballerz")
        total_ringers_wins = sum(1 for g in self._games if g.winner == "Ringers")

        avg_point_diff = sum(g.point_differential for g in self._games) / total_games if total_games > 0 else 0
        avg_total_points = total_points / total_games if total_games > 0 else 0

        return {
            "total_games": total_games,
            "total_players_with_stats": total_players,
            "total_points_scored": total_points,
            "ballerz_wins": total_ballerz_wins,
            "ringers_wins": total_ringers_wins,
            "avg_point_differential": avg_point_diff,
            "avg_total_points_per_game": avg_total_points,
        }

    def search_players(
        self,
        query: str = "",
        archetype: Optional[str] = None,
        rarity: Optional[str] = None,
        faction: Optional[str] = None,
        min_games: int = 0,
    ) -> List[PlayerCareerStats]:
        """Search and filter players."""
        results = []
        query_lower = query.lower()

        for stats in self._career_stats.values():
            if stats.games_played < min_games:
                continue
            if archetype and stats.archetype.lower() != archetype.lower():
                continue
            if rarity and stats.rarity.lower() != rarity.lower():
                continue
            if faction and stats.faction.lower() != faction.lower():
                continue
            if query and query_lower not in stats.full_name.lower():
                continue

            results.append(stats)

        return results

    def get_single_game_records(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all-time single game records.
        Returns a dict of stat_name -> {value, player_name, sprite_id, game_date, game_id}
        """
        records = {
            "points": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "assists": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "rebounds": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "offensive_rebounds": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "defensive_rebounds": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "steals": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "blocks": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "dunks": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "threes_made": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
            "insides_made": {"value": 0, "player_name": "", "sprite_id": -1, "game_date": "", "game_id": -1},
        }

        for game in self._games:
            for slot_id, slot_info in game.player_slots.items():
                if not slot_info.get("IsActive"):
                    continue

                sprite_id = slot_info.get("SpriteID", -1)
                if sprite_id is None or sprite_id < 0:
                    continue

                # Get player name
                player_name = "Unknown"
                if sprite_id in self._players:
                    try:
                        p = self._players[sprite_id]
                        player_name = f"{p['First_Name']} {p['Last_Name']}"
                    except:
                        pass

                def check_record(stat_key: str, value: int):
                    if value and value > records[stat_key]["value"]:
                        records[stat_key] = {
                            "value": value,
                            "player_name": player_name,
                            "sprite_id": sprite_id,
                            "game_date": game.play_date or "Unknown",
                            "game_id": game.game_id
                        }

                check_record("points", slot_info.get("Points", 0))
                check_record("assists", slot_info.get("AssistCount", 0))
                total_reb = (slot_info.get("OffensiveRebounds", 0) or 0) + (slot_info.get("DefensiveRebounds", 0) or 0)
                check_record("rebounds", total_reb)
                check_record("offensive_rebounds", slot_info.get("OffensiveRebounds", 0))
                check_record("defensive_rebounds", slot_info.get("DefensiveRebounds", 0))
                check_record("steals", slot_info.get("Steals", 0))
                check_record("blocks", slot_info.get("Blocks", 0))
                check_record("dunks", slot_info.get("Dunks", 0))
                check_record("threes_made", slot_info.get("ThreesMade", 0))
                check_record("insides_made", slot_info.get("InsidesMade", 0))

        return records

    def get_player_game_log(self, sprite_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Get game-by-game log for a specific player."""
        game_log = []

        for game in self._games:
            for slot_id, slot_info in game.player_slots.items():
                if not slot_info.get("IsActive"):
                    continue
                if slot_info.get("SpriteID") != sprite_id:
                    continue

                # Determine win/loss
                is_ballerz = slot_id < 5
                if game.winner == "Ballerz":
                    result = "W" if is_ballerz else "L"
                elif game.winner == "Ringers":
                    result = "L" if is_ballerz else "W"
                else:
                    result = "T"

                game_log.append({
                    "game_id": game.game_id,
                    "date": game.play_date or "Unknown",
                    "result": result,
                    "team": "Ballerz" if is_ballerz else "Ringers",
                    "points": slot_info.get("Points", 0) or 0,
                    "assists": slot_info.get("AssistCount", 0) or 0,
                    "rebounds": (slot_info.get("OffensiveRebounds", 0) or 0) + (slot_info.get("DefensiveRebounds", 0) or 0),
                    "steals": slot_info.get("Steals", 0) or 0,
                    "blocks": slot_info.get("Blocks", 0) or 0,
                    "turnovers": slot_info.get("Turnovers", 0) or 0,
                    "fg_made": (slot_info.get("InsidesMade", 0) or 0) + (slot_info.get("ThreesMade", 0) or 0),
                    "fg_attempted": (slot_info.get("InsidesAttempted", 0) or 0) + (slot_info.get("ThreesAttempted", 0) or 0),
                    "threes_made": slot_info.get("ThreesMade", 0) or 0,
                    "threes_attempted": slot_info.get("ThreesAttempted", 0) or 0,
                })

                if len(game_log) >= limit:
                    return game_log

        return game_log

    def get_game_superlatives(self) -> Dict[str, Dict[str, Any]]:
        """Get game-level records (closest game, biggest blowout, etc.)."""
        if not self._games:
            return {}

        superlatives = {}

        # Closest game (smallest margin, excluding ties)
        non_tie_games = [g for g in self._games if g.point_differential > 0]
        if non_tie_games:
            closest = min(non_tie_games, key=lambda g: g.point_differential)
            superlatives["closest_game"] = {
                "label": "Closest Game",
                "value": f"{closest.ballerz_score}-{closest.ringers_score}",
                "detail": f"{closest.winner} by {closest.point_differential}",
                "date": closest.play_date or "Unknown",
                "game_id": closest.game_id,
            }

        # Biggest blowout (largest margin)
        biggest = max(self._games, key=lambda g: g.point_differential)
        superlatives["biggest_blowout"] = {
            "label": "Biggest Blowout",
            "value": f"{biggest.ballerz_score}-{biggest.ringers_score}",
            "detail": f"{biggest.winner} by {biggest.point_differential}",
            "date": biggest.play_date or "Unknown",
            "game_id": biggest.game_id,
        }

        # Highest scoring game (most combined points)
        highest = max(self._games, key=lambda g: g.total_points)
        superlatives["highest_scoring"] = {
            "label": "Highest Scoring Game",
            "value": f"{highest.total_points} pts",
            "detail": f"{highest.ballerz_score}-{highest.ringers_score}",
            "date": highest.play_date or "Unknown",
            "game_id": highest.game_id,
        }

        # Lowest scoring game (fewest combined points)
        lowest = min(self._games, key=lambda g: g.total_points)
        superlatives["lowest_scoring"] = {
            "label": "Lowest Scoring Game",
            "value": f"{lowest.total_points} pts",
            "detail": f"{lowest.ballerz_score}-{lowest.ringers_score}",
            "date": lowest.play_date or "Unknown",
            "game_id": lowest.game_id,
        }

        return superlatives

    def get_career_records(self, min_games_for_pct: int = 20) -> Dict[str, Dict[str, Any]]:
        """
        Get all-time career total records (cumulative stats leaders).
        Returns a dict of stat_name -> {value, display_value, player_name, sprite_id, games_played}

        Args:
            min_games_for_pct: Minimum games played to qualify for percentage-based records
        """
        career_categories = [
            ("total_points", "total_points", False),
            ("total_rebounds", "total_rebounds", False),
            ("total_assists", "total_assists", False),
            ("threes_made", "threes_made", False),
            ("three_pt_pct", "three_pt_pct", True),
            ("wins", "wins", False),
            ("total_steals", "total_steals", False),
            ("total_blocks", "total_blocks", False),
            ("games_played", "games_played", False),
            ("total_dunks", "total_dunks", False),
            ("fg_made", "fg_made", False),
            ("total_turnovers", "total_turnovers", False),
        ]

        records = {}
        for key, attr, needs_min_games in career_categories:
            best_value = -1
            best_stats = None

            for stats in self._career_stats.values():
                if stats.games_played < 1:
                    continue
                if needs_min_games and stats.games_played < min_games_for_pct:
                    continue

                stat_dict = stats.to_dict()
                if attr in stat_dict:
                    value = stat_dict[attr]
                elif hasattr(stats, attr):
                    value = getattr(stats, attr)
                    if callable(value):
                        value = value()
                else:
                    continue

                if value is not None and value > best_value:
                    best_value = value
                    best_stats = stats

            if best_stats is not None:
                # Format display value
                if needs_min_games:
                    display_value = f"{best_value * 100:.1f}%"
                else:
                    display_value = f"{best_value:,}" if isinstance(best_value, int) else f"{best_value:.1f}"

                records[key] = {
                    "value": best_value,
                    "display_value": display_value,
                    "player_name": best_stats.full_name,
                    "sprite_id": best_stats.sprite_id,
                    "games_played": best_stats.games_played,
                }
            else:
                records[key] = {
                    "value": 0,
                    "display_value": "0",
                    "player_name": "N/A",
                    "sprite_id": -1,
                    "games_played": 0,
                }

        return records
