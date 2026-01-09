"""
Main game engine for the CS Player Guessing Game.

This module provides the core game logic, player database management,
and game orchestration functionality.
"""

import random
from pathlib import Path
from typing import List, Optional, Dict, Any
import pandas as pd

from .models import Player, GameState, GameResult, GameDifficulty
from .feedback import FeedbackGenerator


class PlayerDatabase:
    """Manages the CS player database and provides query functionality."""

    def __init__(self, csv_path: str | Path):
        """
        Initialize the player database from CSV file.

        Args:
            csv_path: Path to the players.csv file
        """
        self.csv_path = Path(csv_path)
        self.players: List[Player] = []
        self.players_by_name: Dict[str, Player] = {}
        self._load_players()

    def _load_players(self) -> None:
        """Load players from the CSV file."""
        try:
            df = pd.read_csv(self.csv_path)
            self.players = []
            self.players_by_name = {}

            for _, row in df.iterrows():
                player = Player.from_csv_row(row)
                self.players.append(player)
                # Store by lowercase name for case-insensitive lookup
                self.players_by_name[player.name.lower()] = player

            print(f"Loaded {len(self.players)} players from {self.csv_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to load players from {self.csv_path}: {e}")

    def get_player_by_name(self, name: str) -> Optional[Player]:
        """
        Get a player by name (case-insensitive).

        Args:
            name: Player name to search for

        Returns:
            Player object if found, None otherwise
        """
        return self.players_by_name.get(name.lower())

    def get_players_by_difficulty(self, difficulty: GameDifficulty) -> List[Player]:
        """
        Get players filtered by difficulty level.

        Args:
            difficulty: Game difficulty level

        Returns:
            List of players for the specified difficulty
        """
        if difficulty == GameDifficulty.EASY:
            # Top 50 players (could be based on major appearances or other criteria)
            return sorted(self.players, key=lambda p: p.major_appearances, reverse=True)[:50]
        elif difficulty == GameDifficulty.MEDIUM:
            # Top 100 players
            return sorted(self.players, key=lambda p: p.major_appearances, reverse=True)[:100]
        elif difficulty == GameDifficulty.HARD:
            # All players
            return self.players.copy()
        else:
            # Custom - return all for now
            return self.players.copy()

    def get_random_player(self, difficulty: GameDifficulty = GameDifficulty.MEDIUM) -> Player:
        """
        Get a random player for the specified difficulty.

        Args:
            difficulty: Game difficulty level

        Returns:
            Random player from the difficulty pool
        """
        players = self.get_players_by_difficulty(difficulty)
        return random.choice(players)

    def search_players(self, query: str, limit: int = 10) -> List[Player]:
        """
        Search for players by name (fuzzy matching).

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching players
        """
        query_lower = query.lower()
        matches = []

        for player in self.players:
            if query_lower in player.name.lower():
                matches.append(player)

        return matches[:limit]


class GameEngine:
    """Main game engine that orchestrates the CS player guessing game."""

    def __init__(self, player_database: PlayerDatabase):
        """
        Initialize the game engine.

        Args:
            player_database: Initialized player database
        """
        self.db = player_database
        self.feedback_generator = FeedbackGenerator()

    def create_new_game(
        self,
        difficulty: GameDifficulty = GameDifficulty.MEDIUM,
        max_guesses: int = 10,
        target_player: Optional[Player] = None
    ) -> GameState:
        """
        Create a new game with a random or specified target player.

        Args:
            difficulty: Game difficulty level
            max_guesses: Maximum number of guesses allowed
            target_player: Specific target player (if None, random selection)

        Returns:
            New GameState instance
        """
        if target_player is None:
            target_player = self.db.get_random_player(difficulty)

        return GameState(
            target_player=target_player,
            guesses=[],
            feedback_history=[],
            max_guesses=max_guesses
        )

    def make_guess(self, game_state: GameState, player_name: str) -> tuple[bool, str]:
        """
        Process a player guess and update the game state.

        Args:
            game_state: Current game state
            player_name: Name of the guessed player

        Returns:
            Tuple of (success, message)
        """
        if game_state.is_over:
            return False, "Game is already over!"

        # Find the player
        guessed_player = self.db.get_player_by_name(player_name)
        if guessed_player is None:
            # Try to find similar players
            similar_players = self.db.search_players(player_name, limit=5)
            if similar_players:
                suggestions = ", ".join([p.name for p in similar_players])
                return False, f"Player '{player_name}' not found. Did you mean: {suggestions}?"
            else:
                return False, f"Player '{player_name}' not found in database."

        # Generate feedback
        feedback = self.feedback_generator.generate_feedback(
            guessed_player, game_state.target_player
        )

        # Update game state
        game_state.add_guess(guessed_player, feedback)

        # Generate response message
        if feedback.is_correct:
            message = f"🎉 Congratulations! You guessed {game_state.target_player.name} correctly in {game_state.guess_count} guesses!"
        elif game_state.is_over:
            message = f"💀 Game over! The target player was {game_state.target_player.name}."
        else:
            message = f"Guess {game_state.guess_count}/{game_state.max_guesses} - {game_state.remaining_guesses} guesses remaining."

        return True, message

    def get_game_result(self, game_state: GameState, difficulty: str = "medium") -> GameResult:
        """
        Convert a completed game state to a game result.

        Args:
            game_state: Completed game state
            difficulty: Difficulty level string

        Returns:
            GameResult instance
        """
        return GameResult(
            target_player=game_state.target_player,
            guesses=game_state.guesses.copy(),
            feedback_history=game_state.feedback_history.copy(),
            is_won=game_state.is_won,
            guess_count=game_state.guess_count,
            difficulty=difficulty
        )

    def get_possible_players(self, game_state: GameState) -> List[Player]:
        """
        Get list of players that are still possible based on feedback history.

        Args:
            game_state: Current game state

        Returns:
            List of players that satisfy all constraints
        """
        if not game_state.feedback_history:
            return self.db.players.copy()

        constraints = self.feedback_generator.analyze_constraints(game_state.feedback_history)
        return self.feedback_generator.filter_candidates(self.db.players, constraints)

    def get_game_stats(self, game_state: GameState) -> Dict[str, Any]:
        """
        Get current game statistics and analysis.

        Args:
            game_state: Current game state

        Returns:
            Dictionary containing game statistics
        """
        possible_players = self.get_possible_players(game_state)

        stats = {
            "guesses_made": game_state.guess_count,
            "guesses_remaining": game_state.remaining_guesses,
            "possible_players_count": len(possible_players),
            "is_over": game_state.is_over,
            "is_won": game_state.is_won
        }

        if game_state.feedback_history:
            constraints = self.feedback_generator.analyze_constraints(game_state.feedback_history)
            stats["constraints"] = constraints

        return stats