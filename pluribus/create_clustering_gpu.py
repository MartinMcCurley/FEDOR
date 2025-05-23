#!/usr/bin/env python3
"""
Quick Clustering Data Generator for GPU Training
Creates minimal clustering data for full deck (2-14)
"""

import joblib
import numpy as np
import os
from pathlib import Path

def create_clustering_data():
    """Create minimal clustering data for full deck"""
    
    print("🔄 Creating clustering data for full deck (2-14)...")
    
    # Create clustering directory
    clustering_dir = Path("clustering_data")
    clustering_dir.mkdir(exist_ok=True)
    
    # Generate card info lookup table for full deck
    print("• Creating card_info_lut_2_to_14.joblib...")
    
    # Create a basic card lookup table
    card_info_lut = {}
    card_ranks = list(range(2, 15))  # 2 through 14 (Ace)
    card_count = 0
    
    # Generate card combinations (simplified)
    for rank1 in card_ranks:
        for suit1 in range(4):
            for rank2 in card_ranks:
                for suit2 in range(4):
                    if rank1 == rank2 and suit1 == suit2:
                        continue  # Same card
                    card_info_lut[(rank1, suit1, rank2, suit2)] = card_count
                    card_count += 1
    
    # Save card info LUT
    joblib.dump(card_info_lut, clustering_dir / "card_info_lut_2_to_14.joblib")
    print(f"  ✅ Saved card_info_lut_2_to_14.joblib ({len(card_info_lut)} entries)")
    
    # Create centroids file (simplified)
    print("• Creating centroids_2_to_14.joblib...")
    centroids = {
        'flop': np.random.rand(5, 10),  # 5 clusters, 10 features
        'turn': np.random.rand(5, 10),  # 5 clusters, 10 features  
        'river': np.random.rand(5, 10)  # 5 clusters, 10 features
    }
    joblib.dump(centroids, clustering_dir / "centroids_2_to_14.joblib")
    print("  ✅ Saved centroids_2_to_14.joblib")
    
    # Create card combinations for each street
    print("• Creating card combinations...")
    
    # Flop combinations
    flop_combos = [(i, j, k) for i in range(13) for j in range(13) for k in range(13)]
    joblib.dump(flop_combos[:1000], clustering_dir / "card_combos_flop_2_to_14.joblib")
    print("  ✅ Saved card_combos_flop_2_to_14.joblib")
    
    # Turn combinations
    turn_combos = [(i, j, k, l) for i in range(13) for j in range(13) for k in range(13) for l in range(13)]
    joblib.dump(turn_combos[:1000], clustering_dir / "card_combos_turn_2_to_14.joblib") 
    print("  ✅ Saved card_combos_turn_2_to_14.joblib")
    
    # River EHS
    river_ehs = np.random.rand(1000)  # Random hand strengths
    joblib.dump(river_ehs, clustering_dir / "ehs_river_2_to_14.joblib")
    print("  ✅ Saved ehs_river_2_to_14.joblib")
    
    print("\n✅ Clustering data created successfully!")
    print(f"📁 Data saved in: {clustering_dir.absolute()}")
    
    # List files
    files = list(clustering_dir.glob("*_2_to_14.joblib"))
    print(f"📊 Created {len(files)} files:")
    for file in files:
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  • {file.name} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    create_clustering_data() 