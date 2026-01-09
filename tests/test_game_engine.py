"""
Tests for the game engine components.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile

from machine_ai.game import (
    Player, GameEngine, PlayerDatabase, GameDifficulty,
    FeedbackGenerator, FeedbackType
)


@pytest.fixture
def sample_players_csv():
    """Create a temporary CSV file with sample player data."""
    data = {
        "name": ["s1mple", "ZywOo", "NiKo", "sh1ro", "device"],
        "team": ["NAVI", "Vitality", "G2", "C9", "Astralis"],
        "nationality": ["Ukraine", "France", "Bosnia", "Russia", "Denmark"],
        "age": [27, 24, 28, 23, 33],
        "role": ["AWPer", "AWPer", "Rifler", "Rifler", "AWPer"],
        "major_appearances": [14, 8, 10, 2, 15],
        "source_url": ["url1", "url2", "url3", "url4", "url5"]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df = pd.DataFrame(data)
        df.to_csv(f.name, index=False)
        yield f.name

    # Cleanup
    Path(f.name).unlink()


@pytest.fixture
def player_db(sample_players_csv):
    """Create a PlayerDatabase instance with sample data."""
    return PlayerDatabase(sample_players_csv)


@pytest.fixture
def game_engine(player_db):
    """Create a GameEngine instance."""
    return GameEngine(player_db)


class TestPlayer:
    """Test Player model functionality."""

    def test_player_creation(self):
        """Test creating a Player instance."""
        player = Player(
            name="test_player",
            team="test_team",
            nationality="test_country",
            age=25,
            role="Rifler",
            major_appearances=5
        )

        assert player.name == "test_player"
        assert player.team == "test_team"
        assert player.nationality == "test_country"
        assert player.age == 25
        assert player.role == "Rifler"
        assert player.major_appearances == 5

    def test_player_from_csv_row(self):
        """Test creating Player from pandas Series."""
        row_data = {
            "name": "s1mple",
            "team": "NAVI",
            "nationality": "Ukraine",
            "age": 27,
            "role": "AWPer",
            "major_appearances": 14,
            "source_url": "test_url"
        }
        row = pd.Series(row_data)
        player = Player.from_csv_row(row)

        assert player.name == "s1mple"
        assert player.team == "NAVI"
        assert player.nationality == "Ukraine"
        assert player.age == 27
        assert player.role == "AWPer"
        assert player.major_appearances == 14
        assert player.source_url == "test_url"

    def test_get_dimension_value(self):
        """Test getting dimension values from a player."""
        player = Player("test", "team", "country", 25, "Rifler", 5)

        assert player.get_dimension_value("name") == "test"
        assert player.get_dimension_value("team") == "team"
        assert player.get_dimension_value("nationality") == "country"
        assert player.get_dimension_value("age") == 25
        assert player.get_dimension_value("role") == "Rifler"
        assert player.get_dimension_value("major_appearances") == 5


class TestPlayerDatabase:
    """Test PlayerDatabase functionality."""

    def test_database_loading(self, player_db):
        """Test that the database loads players correctly."""
        assert len(player_db.players) == 5
        assert len(player_db.players_by_name) == 5

    def test_get_player_by_name(self, player_db):
        """Test retrieving players by name."""
        player = player_db.get_player_by_name("s1mple")
        assert player is not None
        assert player.name == "s1mple"
        assert player.team == "NAVI"

        # Test case insensitive
        player = player_db.get_player_by_name("S1MPLE")
        assert player is not None
        assert player.name == "s1mple"

        # Test non-existent player
        player = player_db.get_player_by_name("nonexistent")
        assert player is None

    def test_get_players_by_difficulty(self, player_db):
        """Test filtering players by difficulty."""
        easy_players = player_db.get_players_by_difficulty(GameDifficulty.EASY)
        medium_players = player_db.get_players_by_difficulty(GameDifficulty.MEDIUM)
        hard_players = player_db.get_players_by_difficulty(GameDifficulty.HARD)

        # Easy should be top 50 (but we only have 5 total)
        assert len(easy_players) == 5
        # Medium should be top 100 (but we only have 5 total)
        assert len(medium_players) == 5
        # Hard should be all players
        assert len(hard_players) == 5

        # Players should be sorted by major appearances (descending)
        assert easy_players[0].major_appearances >= easy_players[-1].major_appearances

    def test_search_players(self, player_db):
        """Test player search functionality."""
        results = player_db.search_players("s1", limit=5)
        assert len(results) == 1
        assert results[0].name == "s1mple"

        results = player_db.search_players("nonexistent", limit=5)
        assert len(results) == 0


class TestFeedbackGenerator:
    """Test FeedbackGenerator functionality."""

    def test_exact_match_feedback(self):
        """Test feedback when guess exactly matches target."""
        generator = FeedbackGenerator()

        guess = Player("s1mple", "NAVI", "Ukraine", 27, "AWPer", 14)
        target = Player("s1mple", "NAVI", "Ukraine", 27, "AWPer", 14)

        feedback = generator.generate_feedback(guess, target)

        assert feedback.is_correct is True
        for dim_feedback in feedback.dimension_feedback.values():
            assert dim_feedback.feedback_type == FeedbackType.CORRECT

    def test_numeric_dimension_feedback(self):
        """Test feedback for numeric dimensions (age, major_appearances)."""
        generator = FeedbackGenerator()

        # Target is older and has more majors
        guess = Player("player1", "team", "country", 25, "Rifler", 5)
        target = Player("player2", "team", "country", 30, "Rifler", 10)

        feedback = generator.generate_feedback(guess, target)

        assert feedback.dimension_feedback["age"].feedback_type == FeedbackType.HIGHER
        assert feedback.dimension_feedback["major_appearances"].feedback_type == FeedbackType.HIGHER

        # Target is younger and has fewer majors
        guess = Player("player1", "team", "country", 30, "Rifler", 10)
        target = Player("player2", "team", "country", 25, "Rifler", 5)

        feedback = generator.generate_feedback(guess, target)

        assert feedback.dimension_feedback["age"].feedback_type == FeedbackType.LOWER
        assert feedback.dimension_feedback["major_appearances"].feedback_type == FeedbackType.LOWER

    def test_categorical_dimension_feedback(self):
        """Test feedback for categorical dimensions."""
        generator = FeedbackGenerator()

        guess = Player("player1", "TeamA", "CountryA", 25, "AWPer", 5)
        target = Player("player2", "TeamB", "CountryB", 25, "Rifler", 5)

        feedback = generator.generate_feedback(guess, target)

        assert feedback.dimension_feedback["name"].feedback_type == FeedbackType.WRONG
        assert feedback.dimension_feedback["team"].feedback_type == FeedbackType.WRONG
        assert feedback.dimension_feedback["nationality"].feedback_type == FeedbackType.WRONG
        assert feedback.dimension_feedback["role"].feedback_type == FeedbackType.WRONG
        assert feedback.dimension_feedback["age"].feedback_type == FeedbackType.CORRECT
        assert feedback.dimension_feedback["major_appearances"].feedback_type == FeedbackType.CORRECT


class TestGameEngine:
    """Test GameEngine functionality."""

    def test_create_new_game(self, game_engine):
        """Test creating a new game."""
        game_state = game_engine.create_new_game()

        assert game_state.target_player is not None
        assert len(game_state.guesses) == 0
        assert len(game_state.feedback_history) == 0
        assert game_state.max_guesses == 10
        assert game_state.is_won is False
        assert game_state.is_over is False

    def test_make_guess_valid_player(self, game_engine):
        """Test making a guess with a valid player."""
        game_state = game_engine.create_new_game()
        success, message = game_engine.make_guess(game_state, "s1mple")

        assert success is True
        assert len(game_state.guesses) == 1
        assert len(game_state.feedback_history) == 1
        assert game_state.guesses[0].name == "s1mple"

    def test_make_guess_invalid_player(self, game_engine):
        """Test making a guess with an invalid player."""
        game_state = game_engine.create_new_game()
        success, message = game_engine.make_guess(game_state, "nonexistent_player")

        assert success is False
        assert "not found" in message.lower()
        assert len(game_state.guesses) == 0
        assert len(game_state.feedback_history) == 0

    def test_game_win_condition(self, game_engine):
        """Test winning the game."""
        game_state = game_engine.create_new_game()
        target_name = game_state.target_player.name

        success, message = game_engine.make_guess(game_state, target_name)

        assert success is True
        assert game_state.is_won is True
        assert game_state.is_over is True
        assert "congratulations" in message.lower() or "🎉" in message

    def test_game_loss_condition(self, game_engine):
        """Test losing the game by exceeding max guesses."""
        game_state = game_engine.create_new_game(max_guesses=2)
        target_name = game_state.target_player.name

        # Make wrong guesses until max is reached
        available_players = ["s1mple", "ZywOo", "NiKo", "sh1ro", "device"]
        wrong_players = [p for p in available_players if p != target_name]

        for i in range(2):
            success, message = game_engine.make_guess(game_state, wrong_players[i])
            assert success is True

        assert game_state.is_over is True
        assert game_state.is_won is False

    def test_get_possible_players(self, game_engine):
        """Test filtering possible players based on feedback."""
        game_state = game_engine.create_new_game()

        # Initially all players are possible
        possible = game_engine.get_possible_players(game_state)
        assert len(possible) == 5

        # Make a wrong guess
        target_name = game_state.target_player.name
        available_players = ["s1mple", "ZywOo", "NiKo", "sh1ro", "device"]
        wrong_player = next(p for p in available_players if p != target_name)

        game_engine.make_guess(game_state, wrong_player)

        # Now fewer players should be possible
        possible_after = game_engine.get_possible_players(game_state)
        assert len(possible_after) <= len(possible)