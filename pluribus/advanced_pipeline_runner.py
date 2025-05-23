#!/usr/bin/env python3
"""
Advanced Pipeline Runner - Integrated with Advanced PPL System
Complete Pipeline: Clustering → GPU Training → Advanced PPL Generation
"""

import subprocess
import sys
import os
import argparse
import time
from datetime import datetime
from pathlib import Path
import json

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return True, result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"STDERR:\n{e.stderr}")
        return False, None

def check_gpu_status():
    """Check if GPU is available and working"""
    print("🔍 Checking GPU status...")
    try:
        result = subprocess.run([sys.executable, "-c", 
            "import torch; print('CUDA Available:', torch.cuda.is_available()); "
            "print('GPU Count:', torch.cuda.device_count()); "
            "print('GPU Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"],
            capture_output=True, text=True, check=True)
        print(result.stdout)
        return "True" in result.stdout
    except:
        print("❌ GPU check failed")
        return False

def check_clustering_data(full_deck=True):
    """Check if required clustering data exists"""
    clustering_dir = Path("clustering_data")
    if not clustering_dir.exists():
        return False
    
    if full_deck:
        required_files = [
            "card_info_lut_2_to_14.joblib",
            "centroids_2_to_14.joblib",
            "card_combos_flop_2_to_14.joblib",
            "card_combos_turn_2_to_14.joblib",
            "ehs_river_2_to_14.joblib"
        ]
    else:
        required_files = [
            "card_info_lut_12_to_14.joblib",
            "centroids_12_to_14.joblib",
            "card_combos_flop_12_to_14.joblib",
            "card_combos_turn_12_to_14.joblib",
            "ehs_river_12_to_14.joblib"
        ]
    
    missing_files = []
    for file in required_files:
        if not (clustering_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing clustering files: {missing_files}")
        return False
    
    print("✅ Clustering data found")
    return True

def create_clustering_data(full_deck=True):
    """Create clustering data for training"""
    print("🔄 Creating clustering data...")
    
    if full_deck:
        success, _ = run_command([sys.executable, "create_clustering_gpu.py"], 
                               "Creating full deck clustering data")
    else:
        # Use existing partial deck data
        print("✅ Using existing partial deck clustering data")
        success = True
    
    return success

def run_advanced_training(preset, nickname, full_deck=True):
    """Run GPU-optimized training"""
    
    # Training presets
    presets = {
        'quick': {'iterations': 10000, 'desc': 'Quick demo'},
        'medium': {'iterations': 100000, 'desc': 'Medium training'},
        'large': {'iterations': 1000000, 'desc': 'Large scale training'},
        'massive': {'iterations': 10000000, 'desc': 'Massive production training'}
    }
    
    if preset not in presets:
        print(f"❌ Unknown preset: {preset}")
        return False, None
    
    preset_config = presets[preset]
    print(f"🎯 Running {preset_config['desc']} ({preset_config['iterations']:,} iterations)")
    
    # Prepare training command
    if full_deck:
        low_card, high_card = 2, 14
    else:
        low_card, high_card = 12, 14
    
    cmd = [
        sys.executable, "-c", f"""
import sys
sys.path.insert(0, '.')
from train_gpu_optimized import train_agent_gpu_optimized

# Run training
train_agent_gpu_optimized(
    low_card_rank={low_card},
    high_card_rank={high_card},
    n_iterations={preset_config['iterations']},
    nickname='{nickname}_{preset}',
    lut_path='./clustering_data'
)
"""
    ]
    
    success, result = run_command(cmd, f"GPU Training ({preset} preset)")
    
    if success:
        # Find the created strategy file
        strategy_file = f"{nickname}_{preset}/agent.joblib"
        if os.path.exists(strategy_file):
            return True, strategy_file
        else:
            print("❌ Strategy file not found after training")
            return False, None
    
    return False, None

def generate_advanced_ppl(strategy_file, output_dir):
    """Generate advanced PPL strategy"""
    print("\n🎯 Generating Advanced PPL Strategy...")
    
    # Import and run our advanced PPL system
    cmd = [
        sys.executable, "-c", f"""
import sys
sys.path.insert(0, '.')
from advanced_ppl_system import AdvancedPPLSystem

# Initialize advanced PPL system
system = AdvancedPPLSystem()

# Generate professional strategy
output_file = '{output_dir}/advanced_professional_strategy.ppl'
analytics_file = '{output_dir}/advanced_strategy_analytics.json'

rules = system.generate_professional_ppl_strategy(output_file)

print(f"✅ Advanced PPL strategy generated: {{output_file}}")
print(f"📊 Analytics saved: {{analytics_file}}")
"""
    ]
    
    success, _ = run_command(cmd, "Advanced PPL Generation")
    return success

def main():
    """Run the complete advanced poker AI pipeline"""
    parser = argparse.ArgumentParser(description='Advanced Poker AI Pipeline with GPU Training')
    
    # Training options
    parser.add_argument('--preset', choices=['quick', 'medium', 'large', 'massive'], 
                       default='medium', help='Training preset (default: medium)')
    parser.add_argument('--nickname', default='advanced_training', help='Training run nickname')
    
    # Pipeline options
    parser.add_argument('--skip-clustering', action='store_true', help='Skip clustering step')
    parser.add_argument('--skip-training', action='store_true', help='Skip training step')
    parser.add_argument('--strategy-file', help='Use existing strategy file')
    parser.add_argument('--full-deck', action='store_true', default=True, help='Use full deck (2-14) instead of high cards only')
    parser.add_argument('--gpu-check', action='store_true', help='Check GPU status and exit')
    
    args = parser.parse_args()
    
    if args.gpu_check:
        check_gpu_status()
        return
    
    print("🚀 ADVANCED POKER AI PIPELINE")
    print("=" * 80)
    print("🎯 Pipeline: Clustering → GPU Training → Advanced PPL")
    print(f"🔧 Preset: {args.preset}")
    print(f"🏷️  Nickname: {args.nickname}")
    print(f"🃏 Deck: {'Full (2-14)' if args.full_deck else 'High Cards (12-14)'}")
    print("-" * 80)
    
    # Check GPU status
    gpu_available = check_gpu_status()
    if not gpu_available:
        print("⚠️  GPU not detected - training will be slower")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = f"advanced_pipeline_{args.nickname}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    strategy_file = args.strategy_file
    
    # Step 1: Clustering
    if not args.skip_clustering:
        if not check_clustering_data(args.full_deck):
            print("\n🔄 Step 1: Creating clustering data")
            if not create_clustering_data(args.full_deck):
                print("❌ Pipeline failed at clustering step")
                sys.exit(1)
        else:
            print("\n✅ Step 1: Clustering data available")
    else:
        print("\n⏭️  Step 1: Clustering (skipped)")
    
    # Step 2: Training
    if not args.skip_training and not strategy_file:
        print(f"\n🔄 Step 2: GPU Training ({args.preset} preset)")
        success, strategy_file = run_advanced_training(args.preset, args.nickname, args.full_deck)
        if not success:
            print("❌ Pipeline failed at training step")
            sys.exit(1)
        print(f"✅ Training completed: {strategy_file}")
    else:
        print(f"\n⏭️  Step 2: Training (skipped, using: {strategy_file})")
    
    # Step 3: Advanced PPL Generation
    print("\n🔄 Step 3: Advanced PPL Generation")
    if not generate_advanced_ppl(strategy_file, output_dir):
        print("❌ Pipeline failed at PPL generation step")
        sys.exit(1)
    
    # Pipeline complete
    print("\n" + "="*80)
    print("🎉 ADVANCED PIPELINE COMPLETE! 🎉")
    print("="*80)
    print("✅ Step 1: Clustering data ready")
    print("✅ Step 2: GPU training completed")
    print("✅ Step 3: Advanced PPL generated")
    print()
    print("📁 Generated files:")
    if strategy_file:
        print(f"   🎲 Strategy: {strategy_file}")
    print(f"   🎯 Advanced PPL: {output_dir}/advanced_professional_strategy.ppl")
    print(f"   📊 Analytics: {output_dir}/advanced_strategy_analytics.json")
    print()
    print("🔍 Next steps:")
    print(f"   • Review PPL rules: cat {output_dir}/advanced_professional_strategy.ppl")
    print(f"   • View analytics: cat {output_dir}/advanced_strategy_analytics.json")
    if strategy_file:
        print(f"   • Load strategy: python -c \"import joblib; s=joblib.load('{strategy_file}'); print(type(s))\"")

if __name__ == "__main__":
    main() 