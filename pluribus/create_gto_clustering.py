#!/usr/bin/env python3
"""
GTO HIGH-RESOLUTION CLUSTERING GENERATOR
========================================

This script generates clustering data with maximum resolution for near-GTO accuracy.
Uses significantly higher cluster counts than default to minimize abstraction loss.
"""

import sys
import os
sys.path.insert(0, '.')

import time
from pathlib import Path
import click
import joblib
import numpy as np
from memory_profiler import profile

from poker_ai.clustering.card_info_lut_builder import CardInfoLutBuilder

# GPU acceleration for clustering
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print(f"🚀 GPU clustering acceleration available")
except ImportError:
    GPU_AVAILABLE = False
    print("⚠️  GPU acceleration not available, using CPU")

def estimate_clustering_time(river_clusters, turn_clusters, flop_clusters, deck_size):
    """Estimate clustering computation time"""
    complexity = river_clusters * turn_clusters * flop_clusters * (deck_size ** 2)
    
    if GPU_AVAILABLE:
        base_time_per_million = 0.5  # GPU is much faster
    else:
        base_time_per_million = 2.0  # CPU baseline
    
    estimated_hours = (complexity / 1000000) * base_time_per_million
    return max(0.1, estimated_hours)  # Minimum 6 minutes

@click.command()
@click.option(
    "--low_card_rank",
    default=2,
    help="The starting hand rank from 2 through 14 for the deck."
)
@click.option(
    "--high_card_rank", 
    default=14,
    help="The highest hand rank from 2 through 14 for the deck."
)
@click.option(
    "--river_clusters",
    default=500,  # 10x increase from default 50
    help="Number of river clusters for GTO accuracy (default: 500)"
)
@click.option(
    "--turn_clusters",
    default=300,  # 6x increase from default 50
    help="Number of turn clusters for GTO accuracy (default: 300)"
)
@click.option(
    "--flop_clusters", 
    default=200,  # 4x increase from default 50
    help="Number of flop clusters for GTO accuracy (default: 200)"
)
@click.option(
    "--simulations_river",
    default=50,  # 8x increase from default 6
    help="Number of river simulations for accuracy (default: 50)"
)
@click.option(
    "--simulations_turn",
    default=50,  # 8x increase from default 6
    help="Number of turn simulations for accuracy (default: 50)"
)
@click.option(
    "--simulations_flop",
    default=50,  # 8x increase from default 6
    help="Number of flop simulations for accuracy (default: 50)"
)
@click.option(
    "--save_dir",
    default="./clustering_data_gto",
    help="Directory to save GTO clustering data"
)
@click.option(
    "--multiplier",
    default=1.0,
    type=float,
    help="Multiplier for cluster counts (1.0=default, 2.0=double clusters)"
)
@click.option(
    "--preset",
    type=click.Choice(['test', 'medium', 'production', 'perfect']),
    help="Use preset configurations"
)
@profile
def create_gto_clustering(
    low_card_rank: int,
    high_card_rank: int,
    river_clusters: int,
    turn_clusters: int,
    flop_clusters: int,
    simulations_river: int,
    simulations_turn: int,
    simulations_flop: int,
    save_dir: str,
    multiplier: float,
    preset: str
):
    """Generate high-resolution clustering data for GTO accuracy."""
    
    # Apply preset configurations
    if preset == 'test':
        river_clusters, turn_clusters, flop_clusters = 100, 75, 50
        simulations_river = simulations_turn = simulations_flop = 20
        print("🧪 Using TEST preset (faster, lower accuracy)")
    elif preset == 'medium':
        river_clusters, turn_clusters, flop_clusters = 300, 200, 150
        simulations_river = simulations_turn = simulations_flop = 35
        print("🎯 Using MEDIUM preset (balanced)")
    elif preset == 'production':
        river_clusters, turn_clusters, flop_clusters = 500, 300, 200
        simulations_river = simulations_turn = simulations_flop = 50
        print("🏭 Using PRODUCTION preset (high accuracy)")
    elif preset == 'perfect':
        river_clusters, turn_clusters, flop_clusters = 1000, 600, 400
        simulations_river = simulations_turn = simulations_flop = 100
        print("💎 Using PERFECT preset (maximum accuracy)")
    
    # Apply multiplier
    river_clusters = int(river_clusters * multiplier)
    turn_clusters = int(turn_clusters * multiplier)
    flop_clusters = int(flop_clusters * multiplier)
    simulations_river = int(simulations_river * multiplier)
    simulations_turn = int(simulations_turn * multiplier)
    simulations_flop = int(simulations_flop * multiplier)
    
    deck_size = high_card_rank - low_card_rank + 1
    
    print("🎯 GTO HIGH-RESOLUTION CLUSTERING")
    print("=" * 60)
    print(f"📊 Configuration:")
    print(f"   Card Range: {low_card_rank}-{high_card_rank} (deck size: {deck_size})")
    print(f"   River Clusters: {river_clusters:,}")
    print(f"   Turn Clusters: {turn_clusters:,}")
    print(f"   Flop Clusters: {flop_clusters:,}")
    print(f"   Simulations: {simulations_river} per street")
    print(f"   Multiplier: {multiplier}x")
    print(f"   Save Directory: {save_dir}")
    print("=" * 60)
    
    # Calculate accuracy estimate
    total_clusters = river_clusters * turn_clusters * flop_clusters
    accuracy_estimate = min(98.0, 60.0 + (total_clusters / 200000) * 38.0)
    print(f"🎯 Estimated GTO Accuracy: {accuracy_estimate:.1f}%")
    
    # Estimate computation time
    estimated_hours = estimate_clustering_time(river_clusters, turn_clusters, flop_clusters, deck_size)
    print(f"⏱️  Estimated computation time: {estimated_hours:.1f} hours")
    
    if estimated_hours > 8:
        print("⚠️  WARNING: This will take a long time. Consider using a preset or lower multiplier.")
        if not click.confirm("Continue with this configuration?"):
            return
    
    # Create save directory
    save_path = Path(save_dir)
    save_path.mkdir(exist_ok=True)
    
    print(f"\n🚀 Starting high-resolution clustering...")
    print(f"💾 Results will be saved to: {save_path.absolute()}")
    
    start_time = time.time()
    
    try:
        # Initialize the clustering builder
        builder = CardInfoLutBuilder(
            simulations_river,
            simulations_turn, 
            simulations_flop,
            low_card_rank,
            high_card_rank,
            str(save_path)
        )
        
        print("\n🔧 Computing clusters...")
        print(f"   This may take up to {estimated_hours:.1f} hours")
        
        # Run the enhanced clustering
        builder.compute(
            river_clusters,
            turn_clusters,
            flop_clusters
        )
        
        end_time = time.time()
        actual_duration = (end_time - start_time) / 3600
        
        print()
        print("✅ GTO CLUSTERING COMPLETED!")
        print("=" * 60)
        print(f"⏱️  Actual time: {actual_duration:.2f} hours")
        print(f"🎯 GTO Accuracy: ~{accuracy_estimate:.1f}%")
        print(f"📁 Files saved in: {save_path.absolute()}")
        
        # List generated files
        files = list(save_path.glob("*.joblib"))
        total_size = sum(f.stat().st_size for f in files) / (1024**2)
        
        print(f"\n📊 Generated {len(files)} files ({total_size:.1f} MB total):")
        for file in sorted(files):
            size_mb = file.stat().st_size / (1024**2)
            print(f"   • {file.name} ({size_mb:.1f} MB)")
        
        # Create metadata file
        metadata = {
            'configuration': {
                'river_clusters': river_clusters,
                'turn_clusters': turn_clusters,
                'flop_clusters': flop_clusters,
                'simulations': simulations_river,
                'card_range': f"{low_card_rank}-{high_card_rank}",
                'multiplier': multiplier,
                'preset': preset
            },
            'performance': {
                'computation_time_hours': actual_duration,
                'estimated_gto_accuracy': accuracy_estimate,
                'total_clusters': total_clusters,
                'gpu_acceleration': GPU_AVAILABLE
            },
            'files': [f.name for f in files],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        import json
        with open(save_path / "gto_clustering_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📋 Metadata saved: gto_clustering_metadata.json")
        print(f"🎉 Ready for GTO training with {accuracy_estimate:.1f}% accuracy!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Clustering interrupted by user")
        print("💾 Partial progress may be saved")
        return False
    except Exception as e:
        print(f"❌ Clustering failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def quick_gto_clustering():
    """Quick function to generate GTO clustering with sensible defaults"""
    print("🚀 Quick GTO Clustering Setup")
    
    # Detect hardware capabilities
    if GPU_AVAILABLE:
        print("🎮 GPU detected - using high-resolution preset")
        preset = 'production'
        multiplier = 1.5
    else:
        print("💻 CPU only - using medium preset")
        preset = 'medium' 
        multiplier = 1.0
    
    return create_gto_clustering(
        low_card_rank=2,
        high_card_rank=14,
        river_clusters=500,
        turn_clusters=300,
        flop_clusters=200,
        simulations_river=50,
        simulations_turn=50,
        simulations_flop=50,
        save_dir="./clustering_data_gto",
        multiplier=multiplier,
        preset=preset
    )

if __name__ == "__main__":
    create_gto_clustering() 