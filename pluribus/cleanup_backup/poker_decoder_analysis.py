#!/usr/bin/env python3
"""
Poker Strategy Decoder Analysis - Analysis and filtering functionality
Part of the complete pipeline: Clustering → Training → Output → JSON → PPL
"""

from collections import defaultdict
from typing import Dict, List
from poker_decoder_core import PokerStrategyDecoder

class PokerStrategyAnalyzer:
    """Analysis and filtering tools for poker strategies"""
    
    def __init__(self, decoder: PokerStrategyDecoder):
        """Initialize with a core decoder instance"""
        self.decoder = decoder
    
    def find_specific_situations(self, hand_type: str = None, position: str = None, street: str = None) -> List[Dict]:
        """Find specific poker situations matching criteria"""
        all_decisions = self.decoder.get_readable_decisions(limit=1000)
        
        filtered = []
        for decision in all_decisions:
            match = True
            
            if hand_type and hand_type.lower() not in decision['hand'].lower():
                match = False
            if position and position.lower() not in decision['position'].lower():
                match = False
            if street and street.lower() != decision['street'].lower():
                match = False
                
            if match:
                filtered.append(decision)
        
        return filtered
    
    def analyze_hand_type(self, hand_type: str):
        """Analyze strategy for a specific hand type"""
        situations = self.find_specific_situations(hand_type=hand_type)
        
        print(f"\n🎯 STRATEGY ANALYSIS FOR: {hand_type.upper()}")
        print("=" * 60)
        
        if not situations:
            print("No situations found for this hand type.")
            return
        
        # Group by street and position
        by_street = defaultdict(list)
        for situation in situations:
            by_street[situation['street']].append(situation)
        
        for street, street_situations in by_street.items():
            print(f"\n📊 {street}:")
            for situation in street_situations[:5]:  # Show top 5
                top_action, prob = situation['top_action']
                print(f"  {situation['position']}: {top_action} ({prob:.1%})")
    
    def get_position_analysis(self) -> Dict[str, Dict]:
        """Analyze strategy by position"""
        all_decisions = self.decoder.get_readable_decisions(limit=500)
        
        position_stats = defaultdict(lambda: defaultdict(int))
        position_actions = defaultdict(lambda: defaultdict(float))
        
        for decision in all_decisions:
            position = decision['position']
            top_action = decision['top_action'][0]
            prob = decision['top_action'][1]
            
            position_stats[position]['count'] += 1
            position_actions[position][top_action] += prob
        
        # Normalize probabilities
        for position in position_actions:
            total = sum(position_actions[position].values())
            if total > 0:
                for action in position_actions[position]:
                    position_actions[position][action] /= total
        
        return dict(position_actions)
    
    def get_street_analysis(self) -> Dict[str, Dict]:
        """Analyze strategy by street"""
        all_decisions = self.decoder.get_readable_decisions(limit=500)
        
        street_stats = defaultdict(lambda: defaultdict(float))
        street_counts = defaultdict(int)
        
        for decision in all_decisions:
            street = decision['street']
            top_action = decision['top_action'][0]
            prob = decision['top_action'][1]
            
            street_counts[street] += 1
            street_stats[street][top_action] += prob
        
        # Normalize probabilities
        for street in street_stats:
            if street_counts[street] > 0:
                for action in street_stats[street]:
                    street_stats[street][action] /= street_counts[street]
        
        return dict(street_stats)
    
    def print_position_analysis(self):
        """Print analysis of strategies by position"""
        print("\n📍 POSITION ANALYSIS")
        print("=" * 50)
        
        position_analysis = self.get_position_analysis()
        
        for position, actions in position_analysis.items():
            print(f"\n{position}:")
            sorted_actions = sorted(actions.items(), key=lambda x: x[1], reverse=True)
            for action, freq in sorted_actions[:3]:
                print(f"  {action}: {freq:.1%}")
    
    def print_street_analysis(self):
        """Print analysis of strategies by street"""
        print("\n🎰 STREET ANALYSIS")
        print("=" * 50)
        
        street_analysis = self.get_street_analysis()
        
        for street, actions in street_analysis.items():
            print(f"\n{street}:")
            sorted_actions = sorted(actions.items(), key=lambda x: x[1], reverse=True)
            for action, freq in sorted_actions[:3]:
                print(f"  {action}: {freq:.1%}")
    
    def export_filtered_json(self, output_file: str, hand_type: str = None, 
                           position: str = None, street: str = None):
        """Export filtered strategy to JSON format"""
        import json
        
        filtered_decisions = self.find_specific_situations(hand_type, position, street)
        
        output_data = {
            "pipeline_step": "filtered_json_conversion",
            "source": "pluribus_training",
            "filters": {
                "hand_type": hand_type,
                "position": position, 
                "street": street
            },
            "decisions": filtered_decisions,
            "metadata": {
                "total_filtered": len(filtered_decisions),
                "filter_applied": True,
                "format_version": "1.0"
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✅ Exported {len(filtered_decisions)} filtered decisions to {output_file}")
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics of the strategy"""
        all_decisions = self.decoder.get_readable_decisions(limit=None)
        
        stats = {
            "total_decisions": len(all_decisions),
            "unique_hands": len(set(d['hand'] for d in all_decisions)),
            "unique_positions": len(set(d['position'] for d in all_decisions)),
            "unique_streets": len(set(d['street'] for d in all_decisions)),
            "most_common_action": None,
            "action_distribution": defaultdict(int)
        }
        
        # Count action frequencies
        for decision in all_decisions:
            top_action = decision['top_action'][0]
            stats["action_distribution"][top_action] += 1
        
        # Find most common action
        if stats["action_distribution"]:
            stats["most_common_action"] = max(
                stats["action_distribution"].items(), 
                key=lambda x: x[1]
            )
        
        return stats
    
    def print_summary_stats(self):
        """Print summary statistics"""
        stats = self.get_summary_stats()
        
        print("\n📊 STRATEGY SUMMARY STATISTICS")
        print("=" * 50)
        print(f"Total decisions: {stats['total_decisions']}")
        print(f"Unique hand types: {stats['unique_hands']}")
        print(f"Unique positions: {stats['unique_positions']}")
        print(f"Unique streets: {stats['unique_streets']}")
        
        if stats['most_common_action']:
            action, count = stats['most_common_action']
            pct = count / stats['total_decisions'] * 100
            print(f"Most common action: {action} ({count} times, {pct:.1f}%)")
        
        print("\nAction distribution:")
        sorted_actions = sorted(stats["action_distribution"].items(), 
                              key=lambda x: x[1], reverse=True)
        for action, count in sorted_actions[:5]:
            pct = count / stats['total_decisions'] * 100
            print(f"  {action}: {count} ({pct:.1f}%)") 