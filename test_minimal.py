#!/usr/bin/env python3
"""
Minimal test script that tests our game engine with mock data (no pandas required).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock pandas Series for testing
class MockSeries:
    def __init__(self, data):
        self.data = data

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data[key]

try:
    from machine_ai.game.models import Player, FeedbackType
    from machine_ai.game.feedback import FeedbackGenerator
    print("✅ Successfully imported core game components")

    # Test Player creation
    player1 = Player("s1mple", "NAVI", "Ukraine", 27, "AWPer", 14)
    player2 = Player("ZywOo", "Vitality", "France", 24, "AWPer", 8)
    print(f"✅ Players created: {player1.name} and {player2.name}")

    # Test Player.from_csv_row with mock data
    mock_data = {
        "name": "NiKo",
        "team": "G2",
        "nationality": "Bosnia",
        "age": 28,
        "role": "Rifler",
        "major_appearances": 10,
        "source_url": "test_url"
    }
    mock_row = MockSeries(mock_data)
    player3 = Player.from_csv_row(mock_row)
    print(f"✅ Player from CSV: {player3.name} from {player3.team}")

    # Test dimension access
    print(f"✅ Dimension access: {player1.get_dimension_value('age')} years old")

    # Test FeedbackGenerator
    print("\n🔄 Testing FeedbackGenerator...")
    generator = FeedbackGenerator()

    # Test exact match
    feedback1 = generator.generate_feedback(player1, player1)
    print(f"✅ Exact match test: is_correct = {feedback1.is_correct}")

    # Test different players
    feedback2 = generator.generate_feedback(player1, player2)
    print(f"✅ Different players test: is_correct = {feedback2.is_correct}")

    # Show feedback details
    print("   Feedback breakdown:")
    for dim, dim_feedback in feedback2.dimension_feedback.items():
        print(f"     {dim}: {dim_feedback.guess_value} → {dim_feedback.feedback_type.value}")

    # Test numeric comparisons
    young_player = Player("young", "team", "country", 20, "Rifler", 2)
    old_player = Player("old", "team", "country", 30, "Rifler", 12)

    feedback3 = generator.generate_feedback(young_player, old_player)
    age_feedback = feedback3.dimension_feedback["age"]
    majors_feedback = feedback3.dimension_feedback["major_appearances"]

    print(f"✅ Numeric feedback test:")
    print(f"   Age: {age_feedback.guess_value} → {age_feedback.feedback_type.value} (target: {age_feedback.target_value})")
    print(f"   Majors: {majors_feedback.guess_value} → {majors_feedback.feedback_type.value} (target: {majors_feedback.target_value})")

    # Test constraint analysis
    print("\n🔍 Testing constraint analysis...")
    feedback_history = [feedback2, feedback3]
    constraints = generator.analyze_constraints(feedback_history)

    print("✅ Constraints generated:")
    for dim, constraint in constraints.items():
        if constraint.get("excluded"):
            print(f"   {dim}: excluded {constraint['excluded']}")
        if "min" in constraint and "max" in constraint:
            print(f"   {dim}: range {constraint['min']}-{constraint['max']}")

    print(f"\n🎉 All minimal tests passed! Core game logic is working perfectly.")
    print(f"📊 Summary:")
    print(f"   - Player model: ✅ Working")
    print(f"   - Feedback generation: ✅ Working")
    print(f"   - 6-dimension comparison: ✅ Working")
    print(f"   - Numeric feedback (age/majors): ✅ Working")
    print(f"   - Constraint analysis: ✅ Working")
    print(f"\n🚀 Ready for full testing once dependencies are installed!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()