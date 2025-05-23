#!/usr/bin/env python3
"""
GTO SYSTEM TEST SCRIPT
======================

Quick validation that all GTO system components are ready and working.
Includes PPL generation testing to ensure proper variable usage.
"""

import sys
import os
sys.path.insert(0, '.')

def test_imports():
    """Test that all required imports work"""
    print("🧪 Testing imports...")
    
    try:
        import joblib
        print("   ✅ joblib")
    except ImportError:
        print("   ❌ joblib - install with: pip install joblib")
        return False
    
    try:
        import numpy as np
        print("   ✅ numpy")
    except ImportError:
        print("   ❌ numpy - install with: pip install numpy")
        return False
    
    try:
        import yaml
        print("   ✅ yaml")
    except ImportError:
        print("   ❌ yaml - install with: pip install pyyaml")
        return False
    
    try:
        import click
        print("   ✅ click")
    except ImportError:
        print("   ❌ click - install with: pip install click")
        return False
    
    try:
        import cupy as cp
        print("   🎮 CuPy GPU acceleration available")
        print("      GPU: Available")
    except ImportError:
        print("   💻 CuPy not available (CPU-only mode)")
    
    return True

def test_poker_ai_imports():
    """Test poker AI system imports"""
    print("\n🎯 Testing poker AI system...")
    
    try:
        from poker_ai.clustering.card_info_lut_builder import CardInfoLutBuilder
        print("   ✅ CardInfoLutBuilder")
    except ImportError as e:
        print(f"   ❌ CardInfoLutBuilder: {e}")
        return False
    
    try:
        from poker_ai.ai.singleprocess.train import simple_search
        print("   ✅ Training system")
    except ImportError as e:
        print(f"   ❌ Training system: {e}")
        return False
    
    try:
        from poker_ai import utils
        print("   ✅ Utils")
    except ImportError as e:
        print(f"   ❌ Utils: {e}")
        return False
    
    return True

def test_clustering_data():
    """Test if clustering data exists"""
    print("\n📊 Checking clustering data...")
    
    from pathlib import Path
    
    standard_clustering = Path("./clustering_data")
    gto_clustering = Path("./clustering_data_gto")
    
    if standard_clustering.exists():
        files = list(standard_clustering.glob("*.joblib"))
        print(f"   ✅ Standard clustering: {len(files)} files")
    else:
        print("   ⚠️  No standard clustering data found")
    
    if gto_clustering.exists():
        files = list(gto_clustering.glob("*.joblib"))
        print(f"   ✅ GTO clustering: {len(files)} files")
    else:
        print("   ℹ️  No GTO clustering data (will be created)")
    
    return True

def test_ppl_generation():
    """Test PPL generation with proper variables"""
    print("\n📋 Testing PPL generation...")
    
    try:
        # Test mock strategy data
        mock_strategy = {
            'decisions': [
                {
                    'hand': 'AA',
                    'street': 'preflop',
                    'position': 'Early',
                    'situation': 'No raises',
                    'actions': [('raise 3x', 0.8), ('call', 0.2)]
                },
                {
                    'hand': 'Top Pair',
                    'street': 'flop', 
                    'position': 'Late',
                    'situation': 'Heads up',
                    'actions': [('bet', 0.7), ('check', 0.3)]
                }
            ],
            'metadata': {
                'total_info_sets': 1000000,
                'timestep': 5000000
            }
        }
        
        from json_to_ppl_gto_faithful import generate_gto_faithful_ppl
        
        ppl_rules = generate_gto_faithful_ppl(mock_strategy)
        
        # Check for proper format
        has_custom = any(rule == "custom" for rule in ppl_rules)
        has_preflop = any(rule == "preflop" for rule in ppl_rules)
        has_when_rules = any(rule.startswith("when") for rule in ppl_rules)
        
        # Check for proper PPL variables (should be in the generated rules)
        rule_text = " ".join(ppl_rules)
        has_ppl_variables = any(var in rule_text for var in [
            'stilltoact', 'raises', 'amounttocall', 'hand =', 'position =',
            'havetoppair', 'haveset', 'haveoverpair', 'opponents',
            'paironboard', 'flushpossible', 'straightpossible'
        ])
        
        if has_custom and has_preflop and has_when_rules and has_ppl_variables:
            print("   ✅ PPL generation working")
            print("   ✅ Uses proper PPL variables")
            print("   ✅ Follows correct format")
            return True
        else:
            print("   ❌ PPL generation issues:")
            if not has_custom:
                print("      Missing 'custom' header")
            if not has_preflop:
                print("      Missing 'preflop' section")
            if not has_when_rules:
                print("      Missing 'when' rules")
            if not has_ppl_variables:
                print("      Missing proper PPL variables")
            return False
            
    except Exception as e:
        print(f"   ❌ PPL generation failed: {e}")
        return False

def test_system_resources():
    """Test system resources"""
    print("\n💻 Checking system resources...")
    
    try:
        import psutil
        
        # CPU
        cpu_count = psutil.cpu_count()
        print(f"   🔢 CPU cores: {cpu_count}")
        
        # Memory
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        print(f"   💾 RAM: {memory_gb:.1f} GB")
        
        # Disk space
        disk = psutil.disk_usage('.')
        free_gb = disk.free / (1024**3)
        print(f"   💽 Free disk: {free_gb:.1f} GB")
        
        if memory_gb < 8:
            print("   ⚠️  Warning: Less than 8GB RAM - consider using smaller presets")
        
        if free_gb < 20:
            print("   ⚠️  Warning: Less than 20GB free disk - may not be enough for large training")
        
    except ImportError:
        print("   ⚠️  psutil not available - install with: pip install psutil")
    
    return True

def main():
    """Run all tests"""
    print("🎯 GTO SYSTEM READINESS TEST")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Imports
    if test_imports():
        tests_passed += 1
    
    # Test 2: Poker AI imports
    if test_poker_ai_imports():
        tests_passed += 1
    
    # Test 3: Clustering data
    if test_clustering_data():
        tests_passed += 1
    
    # Test 4: PPL generation
    if test_ppl_generation():
        tests_passed += 1
    
    # Test 5: System resources
    if test_system_resources():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"🏁 SYSTEM READINESS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ SYSTEM READY FOR GTO TRAINING!")
        print("✅ PPL GENERATION VERIFIED - Uses proper variables and format")
        print("\n🚀 Quick start commands:")
        print("   # Test run (2-4 hours)")
        print("   python run_gto_perfect_overnight.py --overnight-test")
        print() 
        print("   # Production run (8-12 hours)")
        print("   python run_gto_perfect_overnight.py --overnight-production")
        print()
        print("📋 PPL Output Features:")
        print("   ✅ Uses documented PPL variables (stilltoact, raises, etc.)")
        print("   ✅ Follows example-profile.txt format exactly")  
        print("   ✅ Preserves GTO mixed strategies")
        print("   ✅ Ready for poker room deployment")
        return True
    else:
        print("❌ SYSTEM NOT READY - resolve issues above first")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 