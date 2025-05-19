# FEDOR: A Solver-Based Shanky Profile for 5-Max No-Limit Texas Hold'em (2-30bb)

FEDOR is a computational project to develop a production-ready, solver-based Shanky/OpenHoldem profile for 5-max No-Limit Texas Hold'em, optimized for effective stack depths of 2bb to 30bb.

## Project Overview

The project leverages both public GTO resources and custom neural network training to create a comprehensive poker strategy. Key components include:

- Asset inventory of public GTO resources
- Bet-sizing menu with recursive structure
- Board abstraction using k-means clustering
- Deep Monte Carlo Counterfactual Regret Minimization (MCCFR)
- Strategy merging and quantisation to OpenPPL format
- Custom C/C++ helper DLLs for enhanced functionality

## Current Status

### Milestone 1: Foundations & Preflop Data Acquisition (Complete)
- ✅ Git repository initialized
- ✅ Python environment set up with required packages
- ✅ Project structure established
- ✅ Initial parsing framework created for GTO chart data
- ✅ OpenHoldem development environment setup script

### Milestone 2: Bet Tree Design & Initial Board Abstraction Features (Pending)
- 🔄 Designing bet-tree generation algorithm 
- 🔄 Researching board abstraction features

## Setup Instructions

### Environment Setup

1. Create and activate a Python virtual environment:
```
python -m venv fedor-env
fedor-env\Scripts\activate  # Windows
source fedor-env/bin/activate  # Linux/Mac
```

2. Install required packages:
```
pip install -r requirements.txt
```

### OpenHoldem Development Environment

The project requires an OpenHoldem development environment for testing and deploying the final PPL profile.

1. Download OpenHoldem from the official source
2. Run the setup script to configure the environment:
```
python scripts/setup_openholdem.py --oh-path=<path-to-openholdem>
```

## Testing

Run unit tests for the parsing framework:
```
python -m unittest discover src/parsing/tests
```

## Project Structure

```
FEDOR/
├── data/                           # Data files
│   ├── raw_gto_charts/             # Raw GTO data sources
│   ├── parsed_gto_data/            # Processed GTO data
│   ├── board_abstraction_models/   # Board clustering models
│   └── mccfr_solver_outputs/       # Neural network strategies
├── src/                            # Source code
│   ├── parsing/                    # GTO data parsers
│   ├── abstraction/                # Board abstraction
│   ├── mccfr_training/             # MCCFR training
│   ├── merging_quantisation/       # Strategy processing
│   ├── ppl_generation/             # OpenPPL generation
│   └── cpp_dll/                    # Helper DLL code
├── profiles/                       # OpenPPL profiles
├── notebooks/                      # Analysis notebooks
└── scripts/                        # Utility scripts
```

## License

See the [LICENSE](LICENSE) file for details. 