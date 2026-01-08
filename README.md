# CS Player Guessing Game AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[中文版本](#中文版本) | [English Version](#english-version)

---

## English Version

### Overview

This project develops a state-of-the-art AI agent for the CS (Counter-Strike) player guessing game, inspired by [blast.tv's Counter-Strikle](https://blast.tv/counter-strikle/multiplayer). The AI agent learns to efficiently guess professional CS players based on multi-dimensional feedback across various player attributes.

### Game Mechanics

The guessing game operates on the following principle:
1. **Input**: Player makes a guess (CS player name)
2. **Feedback**: System provides clues across six dimensions:
   - **Name**: Player's in-game name
   - **Team**: Current team affiliation
   - **Nationality**: Player's country of origin
   - **Age**: Player's current age
   - **Role**: Playing position (IGL, AWPer, Entry Fragger, Support, Lurker)
   - **Major Appearances**: Number of major tournament participations

3. **Feedback Types**:
   - ✅ **Correct**: Exact match
   - ❌ **Wrong**: Incorrect value
   - ⬆️ **Higher**: Target value is greater
   - ⬇️ **Lower**: Target value is smaller

### Project Goals

- **Primary Objective**: Achieve state-of-the-art performance in CS player guessing
- **Learning Focus**: Explore AI agent development and model fine-tuning techniques
- **Performance Target**: Consistently outperform human experts in guess efficiency
- **Research Contribution**: Advance game-specific AI methodologies

### Key Features

- 🎯 **Intelligent Guessing Strategy**: AI-powered optimal player selection
- 📊 **Comprehensive Player Database**: Extensive CS professional player dataset
- 🎮 **Game Simulation Environment**: Accurate recreation of the original game mechanics
- 🧠 **Fine-tuned Models**: Custom-trained models for domain-specific performance
- 📈 **Performance Analytics**: Detailed evaluation and benchmarking tools
- 🔄 **Continuous Learning**: Adaptive strategies based on game outcomes

### Architecture

```
machine.ai/
├── data/                    # Player datasets and game data
├── src/                     # Source code
│   ├── agents/             # AI agent implementations
│   ├── game/               # Game simulation engine
│   ├── models/             # ML model definitions
│   └── utils/              # Utility functions
├── tests/                  # Test suites
├── docs/                   # Documentation
└── experiments/            # Training and evaluation scripts
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/machine.ai.git
cd machine.ai

# Install dependencies
pip install -r requirements.txt

# Run the game simulation
python src/game/simulator.py

# Train the AI agent
python experiments/train_agent.py

# Evaluate performance
python experiments/evaluate.py
```

### Development Roadmap

- [x] **Phase 1**: Project foundation and data collection
- [ ] **Phase 2**: Game simulation implementation
- [ ] **Phase 3**: Baseline AI agent development
- [ ] **Phase 4**: Model fine-tuning and optimization
- [ ] **Phase 5**: Performance evaluation and benchmarking

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

### Research and Citations

This project explores the intersection of game AI and domain-specific knowledge representation. If you use this work in your research, please consider citing:

```bibtex
@software{cs_player_ai_agent,
  title={CS Player Guessing Game AI Agent},
  author={Your Name},
  year={2026},
  url={https://github.com/your-username/machine.ai}
}
```

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 中文版本

### 项目概述

本项目致力于开发一个针对CS（反恐精英）选手猜测游戏的先进AI智能体，灵感来源于[blast.tv的Counter-Strikle游戏](https://blast.tv/counter-strikle/multiplayer)。该AI智能体通过学习多维度反馈信息，高效地猜测职业CS选手。

### 游戏机制

猜测游戏的运行原理如下：
1. **输入**：玩家进行猜测（CS选手名字）
2. **反馈**：系统在六个维度上提供线索：
   - **姓名**：选手的游戏内名称
   - **战队**：当前所属战队
   - **国籍**：选手的国家/地区
   - **年龄**：选手当前年龄
   - **位置**：游戏角色（指挥、狙击手、突破手、辅助、游走）
   - **Major参赛次数**：参加Major级别赛事的次数

3. **反馈类型**：
   - ✅ **正确**：完全匹配
   - ❌ **错误**：数值不正确
   - ⬆️ **更高**：目标值更大
   - ⬇️ **更低**：目标值更小

### 项目目标

- **主要目标**：在CS选手猜测领域达到最先进的性能水平
- **学习重点**：探索AI智能体开发和模型微调技术
- **性能目标**：在猜测效率上持续超越人类专家
- **研究贡献**：推进游戏特定AI方法学的发展

### 核心特性

- 🎯 **智能猜测策略**：基于AI的最优选手选择
- 📊 **全面选手数据库**：广泛的CS职业选手数据集
- 🎮 **游戏模拟环境**：精确重现原始游戏机制
- 🧠 **微调模型**：针对特定领域性能的定制训练模型
- 📈 **性能分析**：详细的评估和基准测试工具
- 🔄 **持续学习**：基于游戏结果的自适应策略

### 架构设计

```
machine.ai/
├── data/                    # 选手数据集和游戏数据
├── src/                     # 源代码
│   ├── agents/             # AI智能体实现
│   ├── game/               # 游戏模拟引擎
│   ├── models/             # 机器学习模型定义
│   └── utils/              # 工具函数
├── tests/                  # 测试套件
├── docs/                   # 文档
└── experiments/            # 训练和评估脚本
```

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/your-username/machine.ai.git
cd machine.ai

# 安装依赖
pip install -r requirements.txt

# 运行游戏模拟
python src/game/simulator.py

# 训练AI智能体
python experiments/train_agent.py

# 评估性能
python experiments/evaluate.py
```

### 开发路线图

- [x] **阶段1**：项目基础和数据收集
- [ ] **阶段2**：游戏模拟实现
- [ ] **阶段3**：基线AI智能体开发
- [ ] **阶段4**：模型微调和优化
- [ ] **阶段5**：性能评估和基准测试

### 贡献指南

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解如何开始参与项目。

### 研究与引用

本项目探索了游戏AI与领域特定知识表示的交叉领域。如果您在研究中使用了这项工作，请考虑引用：

```bibtex
@software{cs_player_ai_agent,
  title={CS Player Guessing Game AI Agent},
  author={Your Name},
  year={2026},
  url={https://github.com/your-username/machine.ai}
}
```

### 许可证

本项目采用MIT许可证 - 详情请查看[LICENSE](LICENSE)文件。