#!/usr/bin/env python3
"""
Script to examine strategy data and show what poker decisions are available
"""

import joblib
import json
from collections import defaultdict

def examine_strategy(strategy_file):
    """Examine the strategy file to understand its structure"""
    
    print("🔍 EXAMINING STRATEGY DATA STRUCTURE")
    print("=" * 60)
    
    # Load the strategy
    data = joblib.load(strategy_file)
    print(f"📁 File: {strategy_file}")
    print(f"📊 Top-level keys: {list(data.keys())}")
    print()
    
    # Examine strategy section
    if 'strategy' in data:
        strategy = data['strategy']
        print(f"🎯 Number of information sets: {len(strategy)}")
        print()
        
        # Sample some information sets
        print("📋 SAMPLE INFORMATION SETS:")
        print("-" * 40)
        
        for i, (info_set, actions) in enumerate(list(strategy.items())[:10]):
            print(f"Info Set {i+1}:")
            print(f"  Raw: {str(info_set)[:80]}...")
            
            # Try to parse if it's JSON
            if isinstance(info_set, str) and info_set.startswith('{'):
                try:
                    parsed = json.loads(info_set)
                    print(f"  Parsed: {parsed}")
                except:
                    print(f"  (Could not parse as JSON)")
            
            # Show actions and probabilities
            if isinstance(actions, dict):
                print(f"  Actions: {list(actions.keys())}")
                # Show probabilities if they exist
                total = sum(actions.values())
                if total > 0:
                    probs = {action: prob/total for action, prob in actions.items()}
                    print(f"  Probabilities: {probs}")
            else:
                print(f"  Actions type: {type(actions)}")
            print()
        
        # Analyze action types
        print("🎲 ACTION ANALYSIS:")
        print("-" * 40)
        all_actions = set()
        for actions in strategy.values():
            if isinstance(actions, dict):
                all_actions.update(actions.keys())
        
        print(f"Unique actions found: {sorted(all_actions)}")
        print()
        
        # Try to find patterns
        print("🔍 PATTERN ANALYSIS:")
        print("-" * 40)
        
        # Look for different types of information sets
        card_patterns = defaultdict(int)
        for info_set in list(strategy.keys())[:100]:  # Sample first 100
            info_str = str(info_set)
            if 'cards_cluster' in info_str:
                card_patterns['cards_cluster'] += 1
            if 'history' in info_str:
                card_patterns['history'] += 1
            if 'pre_flop' in info_str:
                card_patterns['pre_flop'] += 1
            if 'flop' in info_str:
                card_patterns['flop'] += 1
            if 'turn' in info_str:
                card_patterns['turn'] += 1
            if 'river' in info_str:
                card_patterns['river'] += 1
        
        print("Pattern frequency in sample:")
        for pattern, count in card_patterns.items():
            print(f"  {pattern}: {count}")
        print()
    
    # Check if there's pre-flop strategy
    if 'pre_flop_strategy' in data:
        pre_flop = data['pre_flop_strategy']
        print(f"🃏 PRE-FLOP STRATEGY:")
        print("-" * 40)
        print(f"Number of pre-flop situations: {len(pre_flop)}")
        
        # Sample pre-flop decisions
        for i, (situation, actions) in enumerate(list(pre_flop.items())[:5]):
            print(f"Pre-flop {i+1}: {str(situation)[:60]}...")
            if isinstance(actions, dict):
                total = sum(actions.values())
                if total > 0:
                    probs = {action: prob/total for action, prob in actions.items()}
                    print(f"  Actions: {probs}")
            print()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        examine_strategy(sys.argv[1])
    else:
        print("Usage: python examine_strategy.py <strategy_file.joblib>") 