# FEDOR Complete Pipeline Documentation

## 🎯 Pipeline Overview

**Complete Flow**: `Clustering → Training → Output → JSON → PPL`

This document describes the complete 5-step pipeline for converting Pluribus poker AI training into human-readable Policy Programming Language (PPL).

## 📁 File Structure (All <200 lines)

### Core Training Files
```
train_simple.py              # 150 lines - Windows-compatible trainer
train_gpu_optimized.py       # 180 lines - GPU training with presets
examine_strategy.py          # 115 lines - Raw strategy analyzer
```

### Modular Decoder System
```
poker_decoder_core.py        # 180 lines - Core decoding functionality  
poker_decoder_analysis.py    # 160 lines - Analysis and filtering
poker_decoder_cli.py         # 85 lines  - Command-line interface
json_to_ppl.py              # 155 lines - JSON to PPL conversion
run_complete_pipeline.py     # 140 lines - Full pipeline runner
```

### Legacy Files (Deprecated)
```
poker_strategy_decoder.py    # DEPRECATED - Redirects to new system
```

## 🔄 Complete Pipeline Steps

### Step 1: Pluribus Clustering ✅
**Purpose**: Generate card abstractions to reduce game tree complexity
**Input**: Raw poker situations
**Output**: Clustering data (`clustering_data/`)
**Command**:
```bash
python bin/poker_ai cluster \
    --low_card_rank 12 \
    --high_card_rank 14 \
    --n_river_clusters 5 \
    --n_turn_clusters 5 \
    --n_flop_clusters 5 \
    --save_dir ./clustering_data
```

### Step 2: Pluribus Training ✅
**Purpose**: Train poker AI using CFR algorithm with GPU acceleration
**Input**: Clustering data
**Output**: Strategy file (`agent.joblib`)
**Commands**:
```bash
# Preset options
python train_gpu_optimized.py --quick      # 1K iterations (~5 min)
python train_gpu_optimized.py --medium     # 10K iterations (~30 min)  
python train_gpu_optimized.py --large      # 1M iterations (~2 hours)
python train_gpu_optimized.py --massive    # 10M iterations (~1 day)
```

### Step 3: Pluribus Output File ✅
**Purpose**: Strategy file containing all learned decisions
**Format**: `.joblib` file with structure:
```python
{
    'strategy': {info_set: action_probabilities},
    'regret': {info_set: regret_values},
    'timestep': training_iteration,
    'pre_flop_strategy': {situation: actions}
}
```

### Step 4: Convert to JSON ✅
**Purpose**: Convert binary strategy to structured JSON format
**Input**: `agent.joblib`
**Output**: `strategy.json`
**Command**:
```bash
python poker_decoder_cli.py [strategy_file] --output-json strategy.json
```

**JSON Structure**:
```json
{
  "pipeline_step": "json_conversion",
  "source": "pluribus_training", 
  "decisions": [
    {
      "hand": "AA/KK (Premium Pairs)",
      "position": "Early Position (UTG/MP)",
      "street": "River",
      "situation": "Facing raise 2.5x",
      "actions": [
        ["raise 50x (all-in)", 0.816],
        ["raise 5x", 0.103]
      ]
    }
  ],
  "metadata": {
    "total_info_sets": 12728,
    "timestep": 1000000
  }
}
```

### Step 5: Convert to PPL ✅
**Purpose**: Generate Policy Programming Language rules for human interpretation
**Input**: `strategy.json`
**Output**: `strategy.ppl`
**Command**:
```bash
python json_to_ppl.py strategy.json --output strategy.ppl
```

**PPL Format**:
```
RULE_001: WHEN hand IN [AA, KK] AND position IN [UTG, UTG+1, MP] AND street = RIVER AND facing_action = 'Facing raise 2.5x' THEN RAISE 50X (ALL-IN) (81.6%) OR RAISE 5X (10.3%)

RULE_002: WHEN hand IN [AK, AQ] AND position IN [BTN, SB, BB] AND street = PRE-FLOP AND facing_action = 'Facing call' THEN RAISE 2.5X (67.2%) OR CALL (24.8%)
```

## 🚀 Usage Examples

### Run Complete Pipeline
```bash
# Quick test run
python run_complete_pipeline.py --preset quick --nickname "test"

# Production run  
python run_complete_pipeline.py --preset large --nickname "production_v1"

# Maximum scale
python run_complete_pipeline.py --preset massive --nickname "final_model"
```

### Run Individual Steps
```bash
# Step 1: Clustering (if needed)
python bin/poker_ai cluster --save_dir ./clustering_data

# Step 2-3: Training
python train_gpu_optimized.py --large --nickname "my_agent"

# Step 4: JSON conversion
python poker_decoder_cli.py results/agent.joblib --output-json my_strategy.json

# Step 5: PPL conversion  
python json_to_ppl.py my_strategy.json --output my_strategy.ppl
```

### Analysis and Queries
```bash
# Basic analysis
python poker_decoder_cli.py results/agent.joblib --analysis

# Specific hand types
python poker_decoder_cli.py results/agent.joblib --hand-type "AA"
python poker_decoder_cli.py results/agent.joblib --hand-type "pairs"

# Position-specific
python poker_decoder_cli.py results/agent.joblib --position "BTN"
python poker_decoder_cli.py results/agent.joblib --position "early"

# Street-specific
python poker_decoder_cli.py results/agent.joblib --street "pre-flop"
python poker_decoder_cli.py results/agent.joblib --street "river"
```

## 📊 Pipeline Output Examples

### Human-Readable Strategy
```
🃏 POKER AI STRATEGY DECISIONS
================================================================================

1. AA/KK (Premium Pairs)
   Position: Early Position (UTG/MP)
   Street: River
   Situation: Facing raise 2.5x
   Decision: raise 50x (all-in) (81.6%), raise 5x (10.3%), raise 2.5x (8.0%)

2. AK/AQ (Ace-High)
   Position: Late Position (BTN/Blinds)
   Street: Pre-flop
   Situation: Facing call
   Decision: raise 2.5x (67.2%), call (24.8%), fold (8.0%)
```

### PPL Rules Sample
```
🎯 POLICY PROGRAMMING LANGUAGE (PPL) SAMPLE
================================================================================

RULE_001: WHEN hand IN [AA, KK] AND position IN [UTG, UTG+1, MP] AND street = RIVER THEN RAISE 50X (ALL-IN) (81.6%)
RULE_002: WHEN hand IN [AK, AQ] AND position IN [BTN, SB, BB] AND street = PRE-FLOP THEN RAISE 2.5X (67.2%) OR CALL (24.8%)
RULE_003: WHEN hand_cluster = 'TT-22 (Medium/Low Pairs)' AND position IN [MP+1, CO] AND street = FLOP THEN CALL (52.1%) OR FOLD (28.9%)
```

## 🔧 Configuration Options

### Training Presets
- **`--quick`**: 1K iterations, ~5 minutes, good for testing
- **`--medium`**: 10K iterations, ~30 minutes, small research runs
- **`--large`**: 1M iterations, ~2 hours, production quality
- **`--massive`**: 10M iterations, ~1 day, maximum training

### Output Filtering
- **`--hand-type`**: Filter by hand categories (AA, pairs, ace-high, etc.)
- **`--position`**: Filter by position (early, middle, late, BTN, etc.)
- **`--street`**: Filter by betting round (pre-flop, flop, turn, river)
- **`--limit`**: Limit number of decisions processed

### Export Options
- **`--output-json`**: Export to structured JSON format
- **`--analysis`**: Comprehensive statistical analysis
- **`--stats`**: Summary statistics only

## 🎯 Key Achievements

### ✅ Complete Pipeline Implementation
- All 5 steps functional and tested
- GPU acceleration working (RTX 4070 Ti tested)
- Windows compatibility issues resolved
- Modular design with all files <200 lines

### ✅ Human-Readable Output
- Poker-specific decision format achieved
- Card cluster translation working
- Position and street detection functional
- Action probability display accurate

### ✅ Structured Data Export
- JSON format for programmatic access
- PPL format for human interpretation  
- Filtering and analysis capabilities
- Pipeline progress tracking

## 🔮 Future Enhancements

### Enhanced Analysis
- [ ] Board texture analysis (wet/dry flops)
- [ ] Stack depth considerations
- [ ] Pot odds integration
- [ ] Equity calculations

### Advanced Features
- [ ] Real-time strategy lookup
- [ ] Range vs range analysis
- [ ] GTO deviation metrics
- [ ] Strategy comparison tools

### Visualization
- [ ] Strategy heat maps
- [ ] Range charts
- [ ] Decision trees  
- [ ] Web interface

## 📈 Success Metrics

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Complete pipeline | ✅ | 5 steps functional |
| File size <200 lines | ✅ | Modular design |
| GPU acceleration | ✅ | RTX 4070 Ti working |
| Windows compatibility | ✅ | All issues resolved |
| Human-readable output | ✅ | PPL format achieved |
| Million-hand training | ✅ | `--massive` preset |

## 🎉 Pipeline Status: COMPLETE

The FEDOR poker AI pipeline successfully implements all requested features:
- **Complete 5-step workflow** from clustering to PPL
- **File structure compliance** with all files under 200 lines
- **Production-ready training** for millions of hands
- **Human-readable output** in Policy Programming Language format
- **GPU acceleration** and Windows compatibility

**Ready for large-scale poker AI research and development.** 