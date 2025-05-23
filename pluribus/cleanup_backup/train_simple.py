#!/usr/bin/env python3
"""
Simple training script that bypasses multiprocessing issues on Windows.
This directly calls the single-process training function.
"""

import sys
import os
sys.path.insert(0, '.')

# Set environment to avoid multiprocessing issues
os.environ["TESTING_SUITE"] = "1"

import logging
from pathlib import Path
import yaml

from poker_ai.ai.singleprocess.train import simple_search
from poker_ai import utils

def train_agent(
    low_card_rank=12,
    high_card_rank=14,
    n_iterations=1000,
    n_players=3,
    lut_path="./clustering_data",
    dump_iteration=50,
    strategy_interval=50,
    nickname="simple_training"
):
    """
    Train a poker AI agent using single-process mode.
    
    Parameters:
    -----------
    low_card_rank : int
        Lowest card rank to include (12 = Queen)
    high_card_rank : int  
        Highest card rank to include (14 = Ace)
    n_iterations : int
        Number of training iterations
    n_players : int
        Number of players in the game
    lut_path : str
        Path to clustering lookup tables
    dump_iteration : int
        Save strategy every N iterations
    strategy_interval : int
        Update strategy every N iterations  
    nickname : str
        Name for this training session
    """
    
    print(f"🚀 Starting Poker AI Training: {nickname}")
    print(f"📊 Parameters:")
    print(f"   Card Range: {low_card_rank}-{high_card_rank}")
    print(f"   Iterations: {n_iterations:,}")
    print(f"   Players: {n_players}")
    print(f"   LUT Path: {lut_path}")
    print("=" * 60)
    
    # Setup configuration
    config = {
        'low_card_rank': low_card_rank,
        'high_card_rank': high_card_rank,
        'strategy_interval': strategy_interval,
        'n_iterations': n_iterations,
        'lcfr_threshold': 400,
        'discount_interval': 400,
        'prune_threshold': 400,
        'c': -20000,
        'n_players': n_players,
        'dump_iteration': dump_iteration,
        'update_threshold': 400,
        'lut_path': lut_path,
        'pickle_dir': False,
        'single_process': True,
        'nickname': nickname
    }
    
    # Create save directory
    save_path = utils.io.create_dir(nickname)
    print(f"💾 Saving results to: {save_path}")
    
    # Save config
    with open(save_path / "config.yaml", "w") as f:
        yaml.dump(config, f)
    
    # Prepare include_ranks
    include_ranks = list(range(low_card_rank, high_card_rank + 1))
    print(f"🃏 Using card ranks: {include_ranks}")
    
    try:
        # Run training
        simple_search(
            config=config,
            save_path=save_path,
            lut_path=lut_path,
            pickle_dir=False,
            strategy_interval=strategy_interval,
            n_iterations=n_iterations,
            lcfr_threshold=400,
            discount_interval=400,
            prune_threshold=400,
            c=-20000,
            n_players=n_players,
            dump_iteration=dump_iteration,
            update_threshold=400,
            include_ranks=include_ranks,
        )
        
        print("✅ Training completed successfully!")
        print(f"📁 Results saved in: {save_path}")
        print(f"🎯 Strategy file: {save_path}/agent.joblib")
        print("\n🔍 To analyze the trained strategy, run:")
        print(f"python strategy_analyzer.py {save_path}/agent.joblib --card-lut ./clustering_data/card_info_lut_{low_card_rank}_to_{high_card_rank}.joblib")
        
    except Exception as e:
        print(f"❌ Training failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Poker AI Training')
    parser.add_argument('--low-card-rank', type=int, default=12, help='Lowest card rank (default: 12)')
    parser.add_argument('--high-card-rank', type=int, default=14, help='Highest card rank (default: 14)')
    parser.add_argument('--n-iterations', type=int, default=1000, help='Number of iterations (default: 1000)')
    parser.add_argument('--n-players', type=int, default=3, help='Number of players (default: 3)')
    parser.add_argument('--lut-path', default="./clustering_data", help='Path to clustering data')
    parser.add_argument('--dump-iteration', type=int, default=50, help='Save every N iterations')
    parser.add_argument('--strategy-interval', type=int, default=50, help='Update strategy every N iterations')
    parser.add_argument('--nickname', default="simple_training", help='Training session name')
    
    args = parser.parse_args()
    
    success = train_agent(
        low_card_rank=args.low_card_rank,
        high_card_rank=args.high_card_rank,
        n_iterations=args.n_iterations,
        n_players=args.n_players,
        lut_path=args.lut_path,
        dump_iteration=args.dump_iteration,
        strategy_interval=args.strategy_interval,
        nickname=args.nickname
    )
    
    sys.exit(0 if success else 1) 