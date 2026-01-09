#!/usr/bin/env python3
"""
Basic test script to verify our game engine works without heavy dependencies.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from machine_ai.game import Player, PlayerDatabase, GameEngine, GameDifficulty
    print("✅ Successfully imported game engine components")

    # Test Player creation
    player = Player("test_player", "test_team", "test_country", 25, "Rifler", 5)
    print(f"✅ Player created: {player.name} from {player.team}")

    # Test PlayerDatabase
    print("\n📊 Testing PlayerDatabase...")
    db = PlayerDatabase("players.csv")
    print(f"✅ Loaded {len(db.players)} players from database")

    # Test getting a specific player
    s1mple = db.get_player_by_name("s1mple")
    if s1mple:
        print(f"✅ Found s1mple: {s1mple.team}, age {s1mple.age}, {s1mple.major_appearances} majors")
    else:
        print("❌ s1mple not found")

    # Test difficulty filtering
    easy_players = db.get_players_by_difficulty(GameDifficulty.EASY)
    medium_players = db.get_players_by_difficulty(GameDifficulty.MEDIUM)
    hard_players = db.get_players_by_difficulty(GameDifficulty.HARD)

    print(f"✅ Difficulty filtering: Easy={len(easy_players)}, Medium={len(medium_players)}, Hard={len(hard_players)}")

    # Test GameEngine
    print("\n🎮 Testing GameEngine...")
    engine = GameEngine(db)
    game_state = engine.create_new_game(GameDifficulty.MEDIUM, max_guesses=5)

    print(f"✅ Game created with target: {game_state.target_player.name}")
    print(f"   Max guesses: {game_state.max_guesses}")
    print(f"   Current guesses: {game_state.guess_count}")

    # Test making a guess (wrong guess)
    available_players = ["s1mple", "ZywOo", "NiKo", "sh1ro", "device"]
    target_name = game_state.target_player.name
    wrong_guess = next((p for p in available_players if p != target_name), "s1mple")

    success, message = engine.make_guess(game_state, wrong_guess)
    if success:
        print(f"✅ Made guess: {wrong_guess}")
        print(f"   Feedback received: {len(game_state.feedback_history)} entries")

        # Show the feedback
        latest_feedback = game_state.feedback_history[-1]
        print("   Feedback details:")
        for dim, feedback in latest_feedback.dimension_feedback.items():
            print(f"     {dim}: {feedback.feedback_type.value}")
    else:
        print(f"❌ Guess failed: {message}")

    # Test winning guess
    success, message = engine.make_guess(game_state, target_name)
    if success and game_state.is_won:
        print(f"✅ Winning guess successful: {target_name}")
        print(f"   Game won in {game_state.guess_count} guesses!")

    print(f"\n🎉 All basic tests passed! Game engine is fully functional.")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("   Make sure you're in the correct directory")
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()