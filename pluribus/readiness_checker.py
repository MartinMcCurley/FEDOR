#!/usr/bin/env python3
"""
Readiness Checker - Verify Advanced Pipeline is Ready for Training
Checks: GPU, Dependencies, Clustering Data, Advanced PPL System
"""

import sys
import os
import subprocess
from pathlib import Path
import importlib.util

def check_component(name, check_func):
    """Check a component and report status"""
    print(f"🔍 Checking {name}...")
    try:
        status, details = check_func()
        if status:
            print(f"✅ {name}: {details}")
        else:
            print(f"❌ {name}: {details}")
        return status
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False

def check_gpu():
    """Check GPU availability and CUDA support"""
    try:
        # Check PyTorch CUDA
        result = subprocess.run([sys.executable, "-c", 
            "import torch; print(torch.cuda.is_available(), torch.cuda.device_count(), "
            "torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"],
            capture_output=True, text=True, check=True)
        
        output = result.stdout.strip()
        parts = output.split()
        
        if parts[0] == "True":
            return True, f"PyTorch CUDA detected - {parts[1]} GPU(s) - {' '.join(parts[2:])}"
        else:
            return False, "PyTorch CUDA not available"
    except:
        return False, "PyTorch not installed or GPU check failed"

def check_cupy():
    """Check CuPy availability"""
    try:
        result = subprocess.run([sys.executable, "-c", 
            "import cupy as cp; print(cp.cuda.runtime.getDeviceCount(), 'GPUs detected')"],
            capture_output=True, text=True, check=True)
        return True, f"CuPy available - {result.stdout.strip()}"
    except:
        return False, "CuPy not available"

def check_dependencies():
    """Check all required Python dependencies"""
    required_packages = [
        'torch', 'numpy', 'joblib', 'sklearn', 'scipy', 
        'fastapi', 'uvicorn', 'pydantic', 'yaml', 'psutil'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        return False, f"Missing packages: {', '.join(missing)}"
    else:
        return True, f"All {len(required_packages)} required packages available"

def check_clustering_data():
    """Check clustering data availability"""
    clustering_dir = Path("clustering_data")
    if not clustering_dir.exists():
        return False, "clustering_data directory not found"
    
    # Check for both full deck and partial deck data
    full_deck_files = [
        "card_info_lut_2_to_14.joblib",
        "centroids_2_to_14.joblib", 
        "card_combos_flop_2_to_14.joblib",
        "card_combos_turn_2_to_14.joblib",
        "ehs_river_2_to_14.joblib"
    ]
    
    partial_deck_files = [
        "card_info_lut_12_to_14.joblib",
        "centroids_12_to_14.joblib",
        "card_combos_flop_12_to_14.joblib", 
        "card_combos_turn_12_to_14.joblib",
        "ehs_river_12_to_14.joblib"
    ]
    
    full_deck_available = all((clustering_dir / f).exists() for f in full_deck_files)
    partial_deck_available = all((clustering_dir / f).exists() for f in partial_deck_files)
    
    if full_deck_available:
        return True, "Full deck clustering data (2-14) available"
    elif partial_deck_available:
        return True, "Partial deck clustering data (12-14) available"
    else:
        missing_full = [f for f in full_deck_files if not (clustering_dir / f).exists()]
        return False, f"Clustering data incomplete. Missing: {missing_full[:3]}..."

def check_training_script():
    """Check if GPU training script is available and functional"""
    script_path = Path("train_gpu_optimized.py")
    if not script_path.exists():
        return False, "train_gpu_optimized.py not found"
    
    # Quick syntax check
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        compile(content, script_path, 'exec')
        return True, "GPU training script available and syntax valid"
    except SyntaxError as e:
        return False, f"Syntax error in training script: {e}"
    except Exception as e:
        return False, f"Error checking training script: {e}"

def check_advanced_ppl_system():
    """Check if advanced PPL system is available and functional"""
    script_path = Path("advanced_ppl_system.py")
    if not script_path.exists():
        return False, "advanced_ppl_system.py not found"
    
    # Quick functionality check
    try:
        result = subprocess.run([sys.executable, "-c", 
            "from advanced_ppl_system import AdvancedPPLSystem; "
            "s = AdvancedPPLSystem(); print('System initialized successfully')"],
            capture_output=True, text=True, check=True)
        return True, "Advanced PPL system available and functional"
    except Exception as e:
        return False, f"Advanced PPL system error: {e}"

def check_pipeline_runner():
    """Check if the advanced pipeline runner is available"""
    script_path = Path("advanced_pipeline_runner.py")
    if not script_path.exists():
        return False, "advanced_pipeline_runner.py not found"
    
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        compile(content, script_path, 'exec')
        return True, "Advanced pipeline runner available"
    except Exception as e:
        return False, f"Pipeline runner error: {e}"

def check_poker_ai_core():
    """Check if poker AI core modules are available"""
    try:
        result = subprocess.run([sys.executable, "-c", 
            "from poker_ai.ai.singleprocess.train import simple_search; "
            "print('Core poker AI modules available')"],
            capture_output=True, text=True, check=True)
        return True, "Poker AI core modules available"
    except Exception as e:
        return False, f"Poker AI core modules error: {e}"

def main():
    """Run comprehensive readiness check"""
    print("🚀 ADVANCED POKER AI PIPELINE READINESS CHECK")
    print("=" * 80)
    print("🎯 Checking all components for advanced training readiness")
    print("-" * 80)
    
    checks = [
        ("GPU Support (PyTorch CUDA)", check_gpu),
        ("CuPy GPU Acceleration", check_cupy),
        ("Python Dependencies", check_dependencies),
        ("Poker AI Core Modules", check_poker_ai_core),
        ("Clustering Data", check_clustering_data),
        ("GPU Training Script", check_training_script),
        ("Advanced PPL System", check_advanced_ppl_system),
        ("Pipeline Runner", check_pipeline_runner),
    ]
    
    results = []
    for name, check_func in checks:
        result = check_component(name, check_func)
        results.append((name, result))
        print()
    
    # Summary
    print("=" * 80)
    print("📊 READINESS SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ READY" if result else "❌ NOT READY"
        print(f"{status:<12} {name}")
    
    print("-" * 80)
    print(f"Overall: {passed}/{total} components ready")
    
    if passed == total:
        print("\n🎉 SYSTEM FULLY READY FOR TRAINING!")
        print("✅ All components verified and functional")
        print("🚀 You can proceed with medium training using:")
        print("   python advanced_pipeline_runner.py --preset medium")
        print()
        print("🎯 For quick test:")
        print("   python advanced_pipeline_runner.py --preset quick")
        print()
        print("⚡ For large scale training:")
        print("   python advanced_pipeline_runner.py --preset large")
        return True
    else:
        print(f"\n⚠️  SYSTEM NOT FULLY READY")
        print(f"❌ {total - passed} component(s) need attention")
        print("\n🔧 Next steps:")
        
        for name, result in results:
            if not result:
                if "GPU" in name:
                    print(f"   • Fix {name}: Install CUDA-enabled PyTorch")
                elif "Dependencies" in name:
                    print(f"   • Fix {name}: pip install missing packages")
                elif "Clustering" in name:
                    print(f"   • Fix {name}: Run python create_clustering_gpu.py")
                else:
                    print(f"   • Fix {name}: Check file exists and is functional")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 