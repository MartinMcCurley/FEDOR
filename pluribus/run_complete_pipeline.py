#!/usr/bin/env python3
"""
Complete Pipeline Runner
Executes: Clustering → Training → Output → JSON → PPL
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime

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

def create_output_dir(nickname):
    """Create timestamped output directory"""
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = f"pipeline_run_{nickname}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def main():
    """Run the complete poker AI pipeline"""
    parser = argparse.ArgumentParser(description='Run Complete Poker AI Pipeline')
    
    # Training options
    parser.add_argument('--preset', choices=['quick', 'medium', 'large', 'massive'], 
                       default='quick', help='Training preset')
    parser.add_argument('--nickname', default='pipeline', help='Run nickname')
    
    # Pipeline options
    parser.add_argument('--skip-clustering', action='store_true', help='Skip clustering step')
    parser.add_argument('--skip-training', action='store_true', help='Skip training step')
    parser.add_argument('--strategy-file', help='Use existing strategy file (skips training)')
    
    # Output options
    parser.add_argument('--limit', type=int, default=50, help='Number of decisions to process')
    
    args = parser.parse_args()
    
    print("🚀 STARTING COMPLETE POKER AI PIPELINE")
    print("=" * 80)
    print("Pipeline: Clustering → Training → Output → JSON → PPL")
    print(f"Preset: {args.preset}")
    print(f"Nickname: {args.nickname}")
    print("-" * 80)
    
    # Create output directory
    output_dir = create_output_dir(args.nickname)
    print(f"📁 Output directory: {output_dir}")
    
    strategy_file = args.strategy_file
    
    # Step 1: Clustering (if not skipped and no existing clustering data)
    if not args.skip_clustering and not os.path.exists("clustering_data"):
        cmd = [
            "python", "bin/poker_ai", "cluster",
            "--low_card_rank", "12",
            "--high_card_rank", "14", 
            "--n_river_clusters", "5",
            "--n_turn_clusters", "5",
            "--n_flop_clusters", "5",
            "--n_simulations_river", "50",
            "--n_simulations_turn", "50", 
            "--n_simulations_flop", "50",
            "--save_dir", "./clustering_data"
        ]
        
        success, _ = run_command(cmd, "Step 1: Pluribus Clustering")
        if not success:
            print("❌ Pipeline failed at clustering step")
            sys.exit(1)
    else:
        print("\n✅ Step 1: Pluribus Clustering (skipped or already exists)")
    
    # Step 2: Training (if not skipped and no strategy file provided)
    if not args.skip_training and not strategy_file:
        cmd = ["python", "train_gpu_optimized.py", f"--{args.preset}", "--nickname", args.nickname]
        
        success, result = run_command(cmd, "Step 2: Pluribus Training")
        if not success:
            print("❌ Pipeline failed at training step")
            sys.exit(1)
        
        # Extract strategy file path from training output
        if result and result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Strategy saved:' in line:
                    strategy_file = line.split('Strategy saved: ')[1].strip() + '/agent.joblib'
                    break
        
        if not strategy_file:
            print("❌ Could not find strategy file from training output")
            sys.exit(1)
    else:
        print(f"\n✅ Step 2: Pluribus Training (skipped, using: {strategy_file})")
    
    print(f"\n📊 Using strategy file: {strategy_file}")
    
    # Step 3: Already completed (strategy file exists)
    print("\n✅ Step 3: Pluribus Output File (strategy.joblib created)")
    
    # Step 4: Convert to JSON
    json_file = os.path.join(output_dir, "strategy.json")
    cmd = ["python", "poker_decoder_cli.py", strategy_file, "--output-json", json_file, "--limit", str(args.limit)]
    
    success, _ = run_command(cmd, "Step 4: Convert to JSON")
    if not success:
        print("❌ Pipeline failed at JSON conversion step")
        sys.exit(1)
    
    # Step 5: Convert to PPL
    ppl_file = os.path.join(output_dir, "strategy.ppl")
    cmd = ["python", "json_to_ppl.py", json_file, "--output", ppl_file]
    
    success, _ = run_command(cmd, "Step 5: Convert to PPL")
    if not success:
        print("❌ Pipeline failed at PPL conversion step")
        sys.exit(1)
    
    # Pipeline complete
    print("\n" + "="*80)
    print("🎉 PIPELINE COMPLETE! 🎉")
    print("="*80)
    print("✅ Step 1: Pluribus clustering")
    print("✅ Step 2: Pluribus training")
    print("✅ Step 3: Pluribus output file")
    print("✅ Step 4: Convert to JSON")
    print("✅ Step 5: Convert to PPL language")
    print()
    print("📁 Generated files:")
    print(f"   📊 Strategy: {strategy_file}")
    print(f"   📋 JSON: {json_file}")
    print(f"   🎯 PPL: {ppl_file}")
    print()
    print("🔍 Next steps:")
    print(f"   • Review PPL rules: cat {ppl_file}")
    print(f"   • Analyze strategy: python poker_decoder_cli.py {strategy_file} --analysis")
    print(f"   • Query specific hands: python poker_decoder_cli.py {strategy_file} --hand-type 'AA'")

if __name__ == "__main__":
    main() 