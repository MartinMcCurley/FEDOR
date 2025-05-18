# FEDOR - Deep Monte Carlo CFR Poker AI

FEDOR is a next-generation poker AI for 6-player No-Limit Texas Hold'em based on Deep Monte Carlo Counterfactual Regret Minimization (Deep MCCFR).

## Project Overview

FEDOR aims to build upon the achievements of Pluribus by implementing an advanced Deep MCCFR poker agent optimized for 6-max No-Limit Hold'em. The project integrates neural network function approximation with proven game-theoretic algorithms to create a high-performance AI capable of strategic play in complex imperfect information environments.

## Technical Approach

- **Algorithm**: Deep Monte Carlo CFR with SD-CFR (Single Deep CFR) methodology
- **Implementation**: PyTorch-based neural networks for advantage/value approximation
- **Hardware Target**: Optimized for NVIDIA RTX 4070ti
- **Foundation**: Extends the pluribus-poker-AI codebase with deep learning capabilities

## Features

- Full implementation of 6-max No-Limit Hold'em game logic
- Neural network architecture optimized for poker state representation
- GPU-accelerated training pipeline with PyTorch
- Comprehensive evaluation framework for strategy assessment

## Development Roadmap

### Phase 1: Game Engine Finalization & Baseline MCCFR
- Extend pluribus-poker-AI game engine for 6-max NLH
- Implement tabular MCCFR for validation on smaller games

### Phase 2: Neural Network Integration & Deep MCCFR Prototype
- Develop PyTorch neural networks for advantage/value approximation
- Implement SD-CFR style training loop
- Conduct initial training runs on 4070ti

### Phase 3: Scaling, Optimization, and Evaluation
- GPU optimization and profiling
- Full-scale 6-max NLH training
- Implement robust evaluation methods
- Iterative refinement based on performance

## Research Background

FEDOR builds on significant research in counterfactual regret minimization, deep learning, and poker AI. The project applies techniques from:

- External Sampling MCCFR for efficient game tree traversal
- Deep CFR/SD-CFR for neural network function approximation
- Mixed-precision training and GPU optimization

## Installation

*Coming soon*

## Usage

*Coming soon*

## Advanced Research Directions

Future development may explore:
- Advanced action and state abstraction techniques
- Integration of concepts from ReBeL and DREAM
- Automated hyperparameter optimization
- Multi-agent training dynamics
- Explainability and strategy analysis
- Alternative neural architectures

## License

*TBD*

## References

For detailed information, see:
- [Research Documentation](docs/research.md)
- [Development Roadmap](docs/roadmap.md)