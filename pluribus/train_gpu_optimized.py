#!/usr/bin/env python3
"""
GPU-Optimized Training Script for Poker AI
Designed for training with millions of iterations using RTX 4070 Ti
"""

import sys
import os
sys.path.insert(0, '.')

# Set environment to avoid multiprocessing issues
os.environ["TESTING_SUITE"] = "1"

import logging
from pathlib import Path
import yaml
import time
import psutil
import gc

from poker_ai.ai.singleprocess.train import simple_search
from poker_ai import utils

# GPU Memory monitoring
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print(f"🚀 GPU detected: {cp.cuda.runtime.getDeviceCount()} devices")
    print(f"🎮 GPU Name: {cp.cuda.Device(0).name}")
    # Get total GPU memory
    mempool = cp.get_default_memory_pool()
    total_bytes = cp.cuda.Device(0).total_memory
    print(f"💾 Total GPU Memory: {total_bytes / 1024**3:.1f} GB")
except ImportError:
    GPU_AVAILABLE = False
    print("⚠️  CuPy not available, using CPU only")

def monitor_resources():
    """Monitor CPU and GPU memory usage"""
    # CPU Memory
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    cpu_memory_gb = memory.used / 1024**3
    cpu_memory_percent = memory.percent
    
    print(f"💻 CPU: {cpu_percent:.1f}% | RAM: {cpu_memory_gb:.1f}GB ({cpu_memory_percent:.1f}%)")
    
    # GPU Memory if available
    if GPU_AVAILABLE:
        try:
            mempool = cp.get_default_memory_pool()
            gpu_memory_used = mempool.used_bytes() / 1024**3
            gpu_memory_total = cp.cuda.Device(0).total_memory / 1024**3
            gpu_percent = (gpu_memory_used / gpu_memory_total) * 100
            print(f"🎮 GPU Memory: {gpu_memory_used:.1f}GB / {gpu_memory_total:.1f}GB ({gpu_percent:.1f}%)")
        except Exception as e:
            print(f"GPU memory check failed: {e}")

def cleanup_memory():
    """Clean up memory between training phases"""
    gc.collect()
    if GPU_AVAILABLE:
        try:
            mempool = cp.get_default_memory_pool()
            mempool.free_all_blocks()
            print("🧹 GPU memory cleaned")
        except:
            pass

def train_agent_gpu_optimized(
    low_card_rank=2,
    high_card_rank=14,
    n_iterations=1000000,  # Default to 1 million iterations
    n_players=6,
    lut_path="./clustering_data",
    dump_iteration=1000,  # Save more frequently for large training
    strategy_interval=1000,
    nickname="million_hands_training",
    checkpoint_interval=10000  # Create checkpoints every 10k iterations
):
    """
    Train a poker AI agent optimized for GPU and large-scale training.
    
    Parameters:
    -----------
    low_card_rank : int
        Lowest card rank to include (2 = Two, 14 = Ace)
    high_card_rank : int  
        Highest card rank to include (2 = Two, 14 = Ace)
    n_iterations : int
        Number of training iterations (default: 1 million)
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
    checkpoint_interval : int
        Create checkpoint saves every N iterations
    """
    
    print("🔥 GPU-OPTIMIZED POKER AI TRAINING")
    print("=" * 60)
    print(f"🎯 Training Session: {nickname}")
    print(f"📊 Parameters:")
    print(f"   Card Range: {low_card_rank}-{high_card_rank} ({'Full Deck' if low_card_rank == 2 and high_card_rank == 14 else 'Partial Deck'})")
    print(f"   Iterations: {n_iterations:,}")
    print(f"   Players: {n_players}")
    print(f"   LUT Path: {lut_path}")
    print(f"   Save Frequency: Every {dump_iteration:,} iterations")
    print(f"   Checkpoint Frequency: Every {checkpoint_interval:,} iterations")
    print("=" * 60)
    
    # Estimate training time
    deck_size = high_card_rank - low_card_rank + 1
    complexity_factor = deck_size * n_players * 0.01  # Rough estimate
    estimated_hours = (n_iterations * complexity_factor) / 3600
    print(f"⏱️  Estimated training time: {estimated_hours:.1f} hours")
    print(f"💾 Expected strategy file size: {n_iterations * 0.001:.1f} MB - {n_iterations * 0.01:.1f} MB")
    print()
    
    # Initial resource check
    print("🔍 Initial Resource Check:")
    monitor_resources()
    print()
    
    # Setup configuration
    config = {
        'low_card_rank': low_card_rank,
        'high_card_rank': high_card_rank,
        'strategy_interval': strategy_interval,
        'n_iterations': n_iterations,
        'lcfr_threshold': max(400, n_iterations // 10),  # Scale with training size
        'discount_interval': max(400, n_iterations // 10),
        'prune_threshold': max(400, n_iterations // 10),
        'c': -20000,
        'n_players': n_players,
        'dump_iteration': dump_iteration,
        'update_threshold': max(400, n_iterations // 10),
        'lut_path': lut_path,
        'pickle_dir': False,
        'single_process': True,
        'nickname': nickname,
        'gpu_optimized': True,
        'checkpoint_interval': checkpoint_interval
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
    print()
    
    start_time = time.time()
    
    try:
        print("🚀 Starting training...")
        print("📈 Progress will be shown below:")
        print()
        
        # Run training with periodic resource monitoring
        simple_search(
            config=config,
            save_path=save_path,
            lut_path=lut_path,
            pickle_dir=False,
            strategy_interval=strategy_interval,
            n_iterations=n_iterations,
            lcfr_threshold=config['lcfr_threshold'],
            discount_interval=config['discount_interval'],
            prune_threshold=config['prune_threshold'],
            c=-20000,
            n_players=n_players,
            dump_iteration=dump_iteration,
            update_threshold=config['update_threshold'],
            include_ranks=include_ranks,
        )
        
        end_time = time.time()
        training_duration = end_time - start_time
        
        print()
        print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"⏱️  Total training time: {training_duration / 3600:.2f} hours")
        print(f"🎯 Iterations per second: {n_iterations / training_duration:.2f}")
        print(f"📁 Results saved in: {save_path}")
        print(f"🎲 Strategy file: {save_path}/agent.joblib")
        print()
        
        # Final resource check
        print("📊 Final Resource Usage:")
        monitor_resources()
        print()
        
        # Cleanup
        cleanup_memory()
        
        print("🔍 To analyze the trained strategy, run:")
        print(f"python strategy_analyzer.py {save_path}/agent.joblib --card-lut ./clustering_data/card_info_lut_{low_card_rank}_to_{high_card_rank}.joblib --format json --output {nickname}_analysis.json")
        print()
        print("🌟 Ready for human-readable strategy analysis!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Training interrupted by user")
        print("💾 Progress has been saved in intermediate dumps")
        return False
    except Exception as e:
        print(f"❌ Training failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='GPU-Optimized Poker AI Training for Million+ Hands')
    parser.add_argument('--low-card-rank', type=int, default=2, help='Lowest card rank (2=Two, 14=Ace)')
    parser.add_argument('--high-card-rank', type=int, default=14, help='Highest card rank (2=Two, 14=Ace)')
    parser.add_argument('--n-iterations', type=int, default=1000000, help='Number of iterations (default: 1M)')
    parser.add_argument('--n-players', type=int, default=6, help='Number of players (default: 6)')
    parser.add_argument('--lut-path', default="./clustering_data", help='Path to clustering data')
    parser.add_argument('--dump-iteration', type=int, default=1000, help='Save every N iterations')
    parser.add_argument('--strategy-interval', type=int, default=1000, help='Update strategy every N iterations')
    parser.add_argument('--checkpoint-interval', type=int, default=10000, help='Checkpoint every N iterations')
    parser.add_argument('--nickname', default="million_hands_training", help='Training session name')
    
    # Preset configurations
    preset_group = parser.add_argument_group('Preset Configurations')
    preset_group.add_argument('--quick', action='store_true', help='Quick test (1K iterations)')
    preset_group.add_argument('--medium', action='store_true', help='Medium training (100K iterations)')
    preset_group.add_argument('--large', action='store_true', help='Large training (1M iterations)')
    preset_group.add_argument('--massive', action='store_true', help='Massive training (10M iterations)')
    
    args = parser.parse_args()
    
    # Apply presets
    if args.quick:
        args.n_iterations = 1000
        args.nickname = "quick_test_gpu"
        args.dump_iteration = 100
        args.checkpoint_interval = 500
    elif args.medium:
        args.n_iterations = 100000
        args.nickname = "medium_training_gpu"
        args.dump_iteration = 1000
        args.checkpoint_interval = 5000
    elif args.large:
        args.n_iterations = 1000000
        args.nickname = "large_training_gpu"
        args.dump_iteration = 5000
        args.checkpoint_interval = 25000
    elif args.massive:
        args.n_iterations = 10000000
        args.nickname = "massive_training_gpu"
        args.dump_iteration = 10000
        args.checkpoint_interval = 100000
    
    success = train_agent_gpu_optimized(
        low_card_rank=args.low_card_rank,
        high_card_rank=args.high_card_rank,
        n_iterations=args.n_iterations,
        n_players=args.n_players,
        lut_path=args.lut_path,
        dump_iteration=args.dump_iteration,
        strategy_interval=args.strategy_interval,
        checkpoint_interval=args.checkpoint_interval,
        nickname=args.nickname
    )
    
    sys.exit(0 if success else 1) 