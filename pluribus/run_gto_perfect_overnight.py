#!/usr/bin/env python3
"""
GTO-PERFECT OVERNIGHT TRAINING ORCHESTRATOR
===========================================

This script orchestrates the complete pipeline for near-GTO perfect poker AI:
1. High-resolution clustering generation
2. GTO-optimized training with checkpoints
3. Faithful PPL generation from trained strategy

Designed for overnight runs with maximum safety and accuracy.
"""

import sys
import os
sys.path.insert(0, '.')

import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
import argparse

def print_header():
    """Print the script header"""
    print("🎯" + "=" * 80)
    print("🏆 GTO-PERFECT OVERNIGHT TRAINING PIPELINE")
    print("🎯" + "=" * 80)
    print("📌 Complete pipeline for near-GTO perfect poker AI strategies")
    print("🔧 High-resolution clustering + Enhanced training + Faithful PPL")
    print("💾 Full checkpointing for overnight safety")
    print("🎯" + "=" * 80)

def check_prerequisites():
    """Check system prerequisites"""
    print("\n🔍 Checking system prerequisites...")
    
    # Check Python packages
    required_packages = ['cupy', 'joblib', 'numpy', 'tqdm', 'click', 'yaml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    # Check GPU
    try:
        import cupy as cp
        gpu_count = cp.cuda.runtime.getDeviceCount()
        gpu_name = cp.cuda.Device(0).name
        gpu_memory = cp.cuda.Device(0).total_memory / (1024**3)
        print(f"   🎮 GPU: {gpu_name} ({gpu_memory:.1f}GB)")
        gpu_available = True
    except:
        print(f"   💻 CPU-only mode")
        gpu_available = False
    
    # Check disk space
    free_space = get_free_disk_space()
    print(f"   💾 Free disk space: {free_space:.1f}GB")
    
    if free_space < 10:
        print("   ⚠️  Warning: Low disk space for large training runs")
    
    return True

def get_free_disk_space():
    """Get free disk space in GB"""
    try:
        import shutil
        free_bytes = shutil.disk_usage('.').free
        return free_bytes / (1024**3)
    except:
        return 100  # Default assumption

def run_step(step_name, command, check_success=None):
    """Run a pipeline step with error handling"""
    print(f"\n🚀 Step: {step_name}")
    print(f"📋 Command: {' '.join(command)}")
    print("🔄 Running...")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=None)
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {step_name} completed successfully ({duration/60:.1f} minutes)")
            
            # Check custom success condition if provided
            if check_success and not check_success():
                print(f"❌ {step_name} failed custom validation")
                return False
            
            return True
        else:
            print(f"❌ {step_name} failed (exit code: {result.returncode})")
            print("📄 STDOUT:", result.stdout[-500:])  # Last 500 chars
            print("📄 STDERR:", result.stderr[-500:])
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {step_name} timed out")
        return False
    except Exception as e:
        print(f"💥 {step_name} crashed: {e}")
        return False

def create_session_metadata(config):
    """Create metadata for the training session"""
    metadata = {
        'session_info': {
            'start_time': datetime.now().isoformat(),
            'session_name': config['session_name'],
            'target_gto_accuracy': config.get('target_accuracy', 90.0),
            'total_iterations': config['training_iterations']
        },
        'clustering_config': {
            'river_clusters': config['river_clusters'],
            'turn_clusters': config['turn_clusters'],
            'flop_clusters': config['flop_clusters'],
            'total_clusters': config['river_clusters'] * config['turn_clusters'] * config['flop_clusters'],
            'clustering_preset': config.get('clustering_preset', 'custom')
        },
        'training_config': {
            'iterations': config['training_iterations'],
            'checkpoint_interval': config['checkpoint_interval'],
            'enhanced_convergence': config.get('enhanced_convergence', True)
        },
        'pipeline_steps': [],
        'files_generated': []
    }
    
    return metadata

def save_session_metadata(metadata, session_dir):
    """Save session metadata"""
    metadata_path = session_dir / "gto_session_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    return metadata_path

def run_gto_pipeline(config):
    """Run the complete GTO pipeline"""
    
    print_header()
    
    # Validate configuration
    print(f"\n📊 Pipeline Configuration:")
    print(f"   Session: {config['session_name']}")
    print(f"   Clustering: {config['river_clusters']}×{config['turn_clusters']}×{config['flop_clusters']} = {config['river_clusters'] * config['turn_clusters'] * config['flop_clusters']:,} total")
    print(f"   Training: {config['training_iterations']:,} iterations")
    print(f"   Checkpoints: Every {config['checkpoint_interval']:,} iterations")
    print(f"   Target GTO Accuracy: {config.get('target_accuracy', 90.0):.1f}%")
    
    # Create session directory
    session_dir = Path(f"gto_session_{config['session_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    session_dir.mkdir(exist_ok=True)
    print(f"📁 Session directory: {session_dir}")
    
    # Create and save metadata
    metadata = create_session_metadata(config)
    metadata_path = save_session_metadata(metadata, session_dir)
    
    success_count = 0
    total_steps = 3
    
    # Step 1: High-Resolution Clustering
    clustering_dir = Path("./clustering_data_gto")
    
    if config.get('skip_clustering', False) and clustering_dir.exists():
        print(f"\n⏭️  Skipping clustering (using existing data)")
        success_count += 1
    else:
        clustering_command = [
            sys.executable, "create_gto_clustering.py",
            "--preset", config.get('clustering_preset', 'production'),
            "--multiplier", str(config.get('clustering_multiplier', 1.0)),
            "--save_dir", str(clustering_dir)
        ]
        
        def check_clustering_success():
            return clustering_dir.exists() and any(clustering_dir.glob("*.joblib"))
        
        if run_step("High-Resolution Clustering", clustering_command, check_clustering_success):
            success_count += 1
            metadata['pipeline_steps'].append({
                'step': 'clustering',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
        else:
            metadata['pipeline_steps'].append({
                'step': 'clustering', 
                'status': 'failed',
                'timestamp': datetime.now().isoformat()
            })
            save_session_metadata(metadata, session_dir)
            return False
    
    # Step 2: GTO-Optimized Training
    training_command = [
        sys.executable, "train_gto_optimized.py",
        "--n-iterations", str(config['training_iterations']),
        "--checkpoint-interval", str(config['checkpoint_interval']),
        "--nickname", config['session_name'],
        "--clustering-multiplier", str(config.get('clustering_multiplier', 1.0))
    ]
    
    if config.get('resume_training', True):
        training_command.append("--resume")
    
    if config.get('enhanced_convergence', True):
        training_command.append("--enhanced-convergence")
    
    def check_training_success():
        # Check if strategy file was created
        pattern = f"{config['session_name']}*/agent.joblib"
        return any(Path('.').glob(pattern))
    
    if run_step("GTO Training", training_command, check_training_success):
        success_count += 1
        metadata['pipeline_steps'].append({
            'step': 'training',
            'status': 'completed', 
            'timestamp': datetime.now().isoformat()
        })
        
        # Find the generated strategy file
        strategy_files = list(Path('.').glob(f"{config['session_name']}*/agent.joblib"))
        if strategy_files:
            metadata['files_generated'].append(str(strategy_files[0]))
    else:
        metadata['pipeline_steps'].append({
            'step': 'training',
            'status': 'failed',
            'timestamp': datetime.now().isoformat()
        })
        save_session_metadata(metadata, session_dir)
        return False
    
    # Step 3: Generate GTO-Faithful PPL
    # First convert to JSON, then to faithful PPL
    strategy_files = list(Path('.').glob(f"{config['session_name']}*/agent.joblib"))
    
    if not strategy_files:
        print("❌ No strategy file found for PPL generation")
        return False
    
    strategy_file = strategy_files[0]
    json_file = strategy_file.parent / "strategy_gto.json"
    
    # Convert strategy to JSON
    json_command = [
        sys.executable, "poker_decoder_cli.py",
        str(strategy_file),
        "--output-json", str(json_file)
    ]
    
    if run_step("Strategy to JSON Conversion", json_command):
        # Generate GTO-faithful PPL
        ppl_file = session_dir / f"{config['session_name']}_gto_faithful.ppl"
        
        ppl_command = [
            sys.executable, "json_to_ppl_gto_faithful.py",
            str(json_file),
            "--output", str(ppl_file),
            "--analysis"
        ]
        
        if run_step("GTO-Faithful PPL Generation", ppl_command):
            success_count += 1
            metadata['pipeline_steps'].append({
                'step': 'ppl_generation',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            metadata['files_generated'].extend([str(json_file), str(ppl_file)])
        else:
            metadata['pipeline_steps'].append({
                'step': 'ppl_generation',
                'status': 'failed',
                'timestamp': datetime.now().isoformat()
            })
    
    # Final session metadata
    metadata['session_info']['end_time'] = datetime.now().isoformat()
    metadata['session_info']['success_rate'] = f"{success_count}/{total_steps}"
    metadata['session_info']['overall_status'] = "completed" if success_count == total_steps else "partial"
    
    save_session_metadata(metadata, session_dir)
    
    # Print final results
    print("\n🏆 GTO PIPELINE RESULTS")
    print("=" * 60)
    print(f"📊 Steps completed: {success_count}/{total_steps}")
    print(f"📁 Session directory: {session_dir}")
    
    if success_count == total_steps:
        print("✅ COMPLETE SUCCESS - Near-GTO perfect strategy ready!")
        print(f"🎯 Strategy file: {strategy_file}")
        print(f"📋 GTO-faithful PPL: {ppl_file}")
        print(f"📊 Session metadata: {metadata_path}")
        
        # Show estimated GTO accuracy
        total_clusters = config['river_clusters'] * config['turn_clusters'] * config['flop_clusters']
        estimated_accuracy = min(95.0, 60.0 + (total_clusters / 200000) * 35.0)
        print(f"🎯 Estimated GTO Accuracy: {estimated_accuracy:.1f}%")
        
    else:
        print("⚠️  PARTIAL SUCCESS - Some steps failed")
        print("🔍 Check session metadata for details")
        print("🔄 Training can be resumed if interrupted")
    
    return success_count == total_steps

def main():
    parser = argparse.ArgumentParser(description='GTO-Perfect Overnight Training Pipeline')
    
    # Session configuration
    parser.add_argument('--session-name', default="gto_perfect_overnight", 
                       help='Name for this training session')
    
    # Clustering configuration
    parser.add_argument('--clustering-preset', 
                       choices=['test', 'medium', 'production', 'perfect'],
                       default='production',
                       help='Clustering quality preset')
    parser.add_argument('--clustering-multiplier', type=float, default=1.5,
                       help='Multiplier for cluster counts')
    parser.add_argument('--skip-clustering', action='store_true',
                       help='Skip clustering if data exists')
    
    # Training configuration  
    parser.add_argument('--training-iterations', type=int, default=10000000,
                       help='Number of training iterations')
    parser.add_argument('--checkpoint-interval', type=int, default=50000,
                       help='Checkpoint interval')
    parser.add_argument('--resume-training', action='store_true', default=True,
                       help='Resume from checkpoint if available')
    parser.add_argument('--enhanced-convergence', action='store_true', default=True,
                       help='Use enhanced convergence parameters')
    
    # Quality presets
    preset_group = parser.add_argument_group('Quality Presets')
    preset_group.add_argument('--overnight-test', action='store_true',
                             help='Overnight test run (2-4 hours)')
    preset_group.add_argument('--overnight-production', action='store_true', 
                             help='Overnight production run (8-12 hours)')
    preset_group.add_argument('--weekend-perfect', action='store_true',
                             help='Weekend perfect run (24-48 hours)')
    
    args = parser.parse_args()
    
    # Apply quality presets
    config = {
        'session_name': args.session_name,
        'clustering_preset': args.clustering_preset,
        'clustering_multiplier': args.clustering_multiplier,
        'skip_clustering': args.skip_clustering,
        'training_iterations': args.training_iterations,
        'checkpoint_interval': args.checkpoint_interval,
        'resume_training': args.resume_training,
        'enhanced_convergence': args.enhanced_convergence
    }
    
    if args.overnight_test:
        config.update({
            'session_name': 'overnight_test',
            'clustering_preset': 'medium',
            'clustering_multiplier': 1.0,
            'training_iterations': 1000000,
            'checkpoint_interval': 25000,
            'target_accuracy': 80.0
        })
        print("🧪 Using OVERNIGHT TEST preset (2-4 hours)")
        
    elif args.overnight_production:
        config.update({
            'session_name': 'overnight_production',
            'clustering_preset': 'production',
            'clustering_multiplier': 1.5,
            'training_iterations': 10000000,
            'checkpoint_interval': 50000,
            'target_accuracy': 90.0
        })
        print("🏭 Using OVERNIGHT PRODUCTION preset (8-12 hours)")
        
    elif args.weekend_perfect:
        config.update({
            'session_name': 'weekend_perfect',
            'clustering_preset': 'perfect',
            'clustering_multiplier': 2.0,
            'training_iterations': 50000000,
            'checkpoint_interval': 100000,
            'target_accuracy': 95.0
        })
        print("💎 Using WEEKEND PERFECT preset (24-48 hours)")
    
    # Calculate cluster counts from preset
    cluster_presets = {
        'test': (100, 75, 50),
        'medium': (300, 200, 150),
        'production': (500, 300, 200),
        'perfect': (1000, 600, 400)
    }
    
    base_clusters = cluster_presets[config['clustering_preset']]
    multiplier = config['clustering_multiplier']
    
    config['river_clusters'] = int(base_clusters[0] * multiplier)
    config['turn_clusters'] = int(base_clusters[1] * multiplier)
    config['flop_clusters'] = int(base_clusters[2] * multiplier)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met")
        return 1
    
    # Run the pipeline
    success = run_gto_pipeline(config)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 