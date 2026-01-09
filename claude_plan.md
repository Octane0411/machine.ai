# Claude's AI Agent Development Plan

## Current Status Assessment

✅ **Data Collection Phase Complete**
- Successfully collected CS player data with all 6 required dimensions
- Dataset: 202+ players with complete information
- Schema: `name,team,nationality,age,role,major_appearances,source_url`
- Data quality: High accuracy with Liquipedia source validation

✅ **Project Foundation Established**
- Documentation: README.md (bilingual), CLAUDE.md, project plan
- Repository structure: Clean git history with MIT license
- Domain knowledge: Comprehensive understanding of CS player guessing mechanics

## Next Phase: AI Agent Development

### Phase 1: Game Simulation Engine (Foundation)

**Objective**: Build the core game mechanics to replicate blast.tv's Counter-Strikle

#### 1.1 Core Game Engine Implementation
```
src/game/
├── engine.py          # Main game logic
├── feedback.py        # Dimension comparison and feedback generation
├── player_db.py       # Player database interface
└── game_state.py      # Game state management
```

**Key Components**:
- **Player Selection**: Random target player selection with difficulty levels
- **Guess Validation**: Input validation and player name matching
- **Feedback System**: 6-dimension comparison logic (✅❌⬆️⬇️)
- **Game State**: Track guesses, feedback history, and win conditions

#### 1.2 Feedback Logic Implementation
```python
class FeedbackGenerator:
    def compare_dimensions(self, guess_player: Player, target_player: Player) -> GameFeedback:
        return {
            'name': self._exact_match(guess_player.name, target_player.name),
            'team': self._exact_match(guess_player.team, target_player.team),
            'nationality': self._exact_match(guess_player.nationality, target_player.nationality),
            'age': self._numeric_compare(guess_player.age, target_player.age),
            'role': self._exact_match(guess_player.role, target_player.role),
            'major_appearances': self._numeric_compare(guess_player.major_appearances, target_player.major_appearances)
        }
```

#### 1.3 Game Modes and Difficulty
- **Easy Mode**: Top 50 most famous players
- **Medium Mode**: Top 100 players
- **Hard Mode**: Full dataset (202+ players)
- **Custom Mode**: Filter by team, nationality, or role

### Phase 2: AI Agent Architecture (Core Intelligence)

**Objective**: Develop intelligent guessing strategies that outperform humans

#### 2.1 Agent Framework Design
```
src/agents/
├── base_agent.py      # Abstract agent interface
├── heuristic_agent.py # Rule-based baseline agent
├── ml_agent.py        # Machine learning agent
├── ensemble_agent.py  # Combined strategy agent
└── strategies/        # Individual strategy implementations
```

#### 2.2 Strategy Implementation Hierarchy

**Level 1: Heuristic Strategies (Baseline)**
```python
class HeuristicAgent:
    def __init__(self):
        self.strategies = [
            PopularPlayerStrategy(),    # Start with famous players
            TeamClusterStrategy(),      # Use team information efficiently
            AgeRangeStrategy(),        # Exploit age distribution
            NationalityStrategy(),     # Geographic clustering
            RoleBasedStrategy(),       # Position-specific logic
            MajorCountStrategy()       # Tournament experience patterns
        ]
```

**Level 2: Information Theory Approach**
- **Entropy Calculation**: Choose guesses that maximize information gain
- **Dimension Weighting**: Prioritize dimensions with highest discriminative power
- **Probability Estimation**: Maintain probability distributions over remaining candidates

**Level 3: Machine Learning Agent**
- **Feature Engineering**: Game state representation
- **Model Architecture**: Decision transformer or Q-learning
- **Training Data**: Simulated optimal gameplay and human expert games

#### 2.3 Strategy Examples

**Popular Player First Strategy**:
```python
def get_initial_guess(self, game_state: GameState) -> str:
    # Start with statistically most likely players
    famous_players = ["s1mple", "ZywOo", "NiKo", "sh1ro", "device"]
    return random.choice(famous_players)
```

**Information Gain Strategy**:
```python
def calculate_information_gain(self, candidate: str, remaining_players: List[Player]) -> float:
    # Calculate expected information gain for each dimension
    expected_entropy = 0
    for dimension in ['team', 'nationality', 'age', 'role', 'major_appearances']:
        entropy = self._calculate_dimension_entropy(candidate, remaining_players, dimension)
        expected_entropy += entropy
    return expected_entropy
```

### Phase 3: Training and Optimization

#### 3.1 Simulation Environment
```python
class TrainingEnvironment:
    def __init__(self, player_database: PlayerDB):
        self.db = player_database
        self.game_engine = GameEngine(player_database)

    def run_episode(self, agent: Agent, difficulty: str = "medium") -> EpisodeResult:
        # Run complete game simulation
        # Return: guess_count, success, feedback_history, strategy_decisions
        pass

    def batch_evaluation(self, agent: Agent, num_games: int = 1000) -> PerformanceMetrics:
        # Evaluate agent performance across many games
        pass
```

#### 3.2 Performance Metrics
- **Primary**: Average guesses to solution
- **Success Rate**: Percentage solved within N guesses (N=6, 8, 10)
- **Efficiency**: Information gain per guess
- **Robustness**: Performance across different difficulty levels
- **Human Comparison**: vs expert human baseline

#### 3.3 Training Pipeline
```python
class AgentTrainer:
    def train_ml_agent(self, training_games: int = 10000):
        # 1. Generate training data through simulation
        # 2. Extract optimal decision patterns
        # 3. Train neural network on game states -> optimal guesses
        # 4. Validate on held-out test set
        pass

    def optimize_heuristics(self, validation_games: int = 1000):
        # 1. Grid search over strategy parameters
        # 2. Evolutionary optimization of strategy weights
        # 3. Cross-validation across different player pools
        pass
```

### Phase 4: Advanced Features and SOTA Achievement

#### 4.1 Advanced Strategies
- **Dynamic Strategy Selection**: Adapt strategy based on game progress
- **Meta-Learning**: Learn from previous games to improve future performance
- **Ensemble Methods**: Combine multiple agents for robust performance
- **Adversarial Training**: Train against difficult scenarios

#### 4.2 Model Fine-tuning Approach
```python
class CS_PlayerGuessingModel:
    def __init__(self, base_model: str = "microsoft/DialoGPT-medium"):
        # Fine-tune language model for CS domain
        # Input: Game state + feedback history
        # Output: Next optimal guess with confidence
        pass

    def generate_guess(self, game_context: str) -> Tuple[str, float]:
        # Context: "Previous guesses: [s1mple: age↑, team✗, ...] Target characteristics: ..."
        # Output: ("ZywOo", 0.85)  # player_name, confidence
        pass
```

#### 4.3 SOTA Benchmarking
- **Human Expert Baseline**: Recruit CS experts for comparison
- **Existing Solutions**: Compare against any existing guessing game bots
- **Theoretical Optimal**: Calculate information-theoretic lower bounds
- **Cross-validation**: Test on unseen player data and game variants

## Implementation Timeline

### Week 1-2: Foundation
- [x] Data collection and validation ✅
- [ ] Game engine implementation
- [ ] Basic feedback system
- [ ] Simple CLI interface for testing

### Week 3-4: Baseline Agents
- [ ] Heuristic strategy implementations
- [ ] Random baseline for comparison
- [ ] Performance evaluation framework
- [ ] Initial benchmarking

### Week 5-6: Advanced Intelligence
- [ ] Information theory approach
- [ ] ML agent architecture
- [ ] Training data generation
- [ ] Model fine-tuning experiments

### Week 7-8: Optimization and SOTA
- [ ] Ensemble methods
- [ ] Performance optimization
- [ ] Human expert comparison
- [ ] Final benchmarking and validation

## Critical Success Factors

### Technical Requirements
1. **Game Accuracy**: Perfect replication of original game mechanics
2. **Performance**: Agent decisions in <100ms
3. **Scalability**: Handle full player database efficiently
4. **Robustness**: Graceful handling of edge cases and data inconsistencies

### Performance Targets
1. **Primary Goal**: Average <4 guesses for medium difficulty
2. **Human Baseline**: Outperform 95% of human players
3. **Consistency**: <10% variance across different player pools
4. **Speed**: Real-time decision making for interactive gameplay

### Research Contributions
1. **Novel Strategies**: Information-theoretic approach to guessing games
2. **Domain Adaptation**: CS-specific knowledge integration
3. **Benchmarking**: Establish standardized evaluation metrics
4. **Open Source**: Reproducible research with public codebase

## Risk Mitigation

### Technical Risks
- **Data Drift**: Player transfers and roster changes
  - *Solution*: Automated data updates and validation
- **Model Overfitting**: Memorizing specific players
  - *Solution*: Cross-validation and unseen player testing
- **Performance Bottlenecks**: Slow decision making
  - *Solution*: Profiling and optimization, caching strategies

### Research Risks
- **Limited Novelty**: Existing solutions already achieve SOTA
  - *Solution*: Focus on interpretable strategies and domain insights
- **Evaluation Challenges**: Difficulty comparing to humans
  - *Solution*: Multiple evaluation metrics and expert validation
- **Reproducibility**: Complex training pipelines
  - *Solution*: Comprehensive documentation and containerization

## Validation Plan

### Automated Testing
```python
def test_suite():
    # Unit tests: Individual component functionality
    test_feedback_generation()
    test_player_database_queries()
    test_agent_decision_logic()

    # Integration tests: End-to-end gameplay
    test_complete_game_simulation()
    test_multi_agent_comparison()

    # Performance tests: Efficiency and scalability
    test_decision_speed()
    test_memory_usage()
    test_concurrent_games()
```

### Human Evaluation
- **Expert Validation**: CS community experts test the system
- **Comparative Study**: Side-by-side human vs AI performance
- **Usability Testing**: Feedback on game interface and experience

### Continuous Integration
- **Daily Benchmarks**: Automated performance tracking
- **Data Validation**: Regular player database updates and checks
- **Regression Testing**: Ensure improvements don't break existing functionality

## Next Immediate Actions

1. **Setup Project Structure**: Create the planned directory structure
2. **Implement Game Engine**: Start with core game mechanics
3. **Build Testing Framework**: Establish evaluation pipeline
4. **Develop Baseline Agent**: Simple heuristic for initial comparison

This plan builds directly on your excellent data collection work and provides a clear path to achieving SOTA performance in CS player guessing through systematic development and rigorous evaluation.