#!/usr/bin/env python3
"""
Strategy Analyzer for Pluribus Poker AI

This tool analyzes trained poker AI strategies and converts them to human-readable format.
It can decode information sets, extract patterns, and generate reports.
"""

import joblib
import json
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
from collections import defaultdict, Counter
import argparse
import sys


class InfoSetDecoder:
    """Decodes information set IDs to human-readable game states."""
    
    def __init__(self, card_lut_path: Optional[str] = None):
        """Initialize with optional card lookup tables."""
        self.card_lut = None
        if card_lut_path:
            try:
                self.card_lut = joblib.load(card_lut_path)
                print(f"Loaded card lookup tables from {card_lut_path}")
            except Exception as e:
                print(f"Warning: Could not load card LUT: {e}")
    
    def decode_info_set(self, info_set_id: str) -> Dict[str, Any]:
        """
        Decode an information set ID to extract game state information.
        
        This is a placeholder implementation. The actual decoding would depend
        on how the info set IDs are encoded in the specific implementation.
        """
        # For now, return the raw info set ID with basic analysis
        decoded = {
            'raw_info_set': info_set_id,
            'estimated_round': self._estimate_betting_round(info_set_id),
            'info_set_length': len(str(info_set_id)),
            'info_set_type': type(info_set_id).__name__
        }
        
        # Try to extract more information if possible
        if isinstance(info_set_id, str) and '_' in info_set_id:
            parts = info_set_id.split('_')
            decoded['info_set_parts'] = parts
            
        return decoded
    
    def _estimate_betting_round(self, info_set_id: str) -> str:
        """Estimate which betting round based on info set characteristics."""
        # This is a heuristic - actual implementation would need proper decoding
        id_str = str(info_set_id)
        if len(id_str) < 10:
            return 'pre_flop'
        elif len(id_str) < 15:
            return 'flop'
        elif len(id_str) < 20:
            return 'turn'
        else:
            return 'river'
    
    def get_card_names(self, card_ids: List[int]) -> List[str]:
        """Convert card IDs to human-readable names."""
        # Standard 52-card deck mapping
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        
        card_names = []
        for card_id in card_ids:
            if 0 <= card_id < 52:
                suit_idx = card_id // 13
                rank_idx = card_id % 13
                card_names.append(f"{ranks[rank_idx]}{suits[suit_idx]}")
            else:
                card_names.append(f"Card_{card_id}")
        
        return card_names


class StrategyAnalyzer:
    """Main strategy analysis class."""
    
    def __init__(self, decoder: Optional[InfoSetDecoder] = None):
        """Initialize the analyzer."""
        self.decoder = decoder or InfoSetDecoder()
        self.strategy_data = None
        self.analysis_results = {}
    
    def load_strategy(self, strategy_path: str) -> bool:
        """Load and parse strategy file."""
        try:
            print(f"Loading strategy from {strategy_path}...")
            self.strategy_data = joblib.load(strategy_path)
            print(f"Successfully loaded strategy data")
            
            # Analyze the structure
            self._analyze_structure()
            return True
            
        except Exception as e:
            print(f"Error loading strategy: {e}")
            return False
    
    def _analyze_structure(self):
        """Analyze the structure of the loaded strategy data."""
        if not self.strategy_data:
            return
        
        structure = {
            'type': type(self.strategy_data).__name__,
            'size': len(self.strategy_data) if hasattr(self.strategy_data, '__len__') else 'unknown'
        }
        
        if isinstance(self.strategy_data, dict):
            structure['keys'] = list(self.strategy_data.keys())
            
            # Analyze strategy section if it exists
            if 'strategy' in self.strategy_data:
                strategy_section = self.strategy_data['strategy']
                structure['strategy_info'] = {
                    'type': type(strategy_section).__name__,
                    'num_info_sets': len(strategy_section) if hasattr(strategy_section, '__len__') else 'unknown'
                }
                
                # Sample some info sets
                if hasattr(strategy_section, 'items'):
                    sample_items = list(strategy_section.items())[:5]
                    structure['sample_info_sets'] = [
                        {
                            'info_set': str(info_set)[:50] + '...' if len(str(info_set)) > 50 else str(info_set),
                            'actions': list(actions.keys()) if isinstance(actions, dict) else str(type(actions))
                        }
                        for info_set, actions in sample_items
                    ]
        
        self.analysis_results['structure'] = structure
    
    def extract_patterns(self) -> Dict[str, Any]:
        """Extract common patterns and tendencies from the strategy."""
        if not self.strategy_data:
            return {}
        
        patterns = {
            'action_frequency': defaultdict(int),
            'betting_rounds': defaultdict(int),
            'strategy_summary': {}
        }
        
        strategy_section = self._get_strategy_section()
        if not strategy_section:
            return patterns
        
        print("Analyzing strategy patterns...")
        
        # Analyze action frequencies and patterns
        total_info_sets = 0
        action_counts = defaultdict(int)
        round_counts = defaultdict(int)
        
        for info_set, actions in strategy_section.items():
            total_info_sets += 1
            
            # Estimate betting round
            betting_round = self.decoder._estimate_betting_round(str(info_set))
            round_counts[betting_round] += 1
            
            # Analyze actions
            if isinstance(actions, dict):
                for action, probability in actions.items():
                    action_counts[action] += 1
                    patterns['action_frequency'][action] += probability
        
        # Calculate averages
        for action in patterns['action_frequency']:
            patterns['action_frequency'][action] /= total_info_sets
        
        patterns['betting_rounds'] = dict(round_counts)
        patterns['total_info_sets'] = total_info_sets
        patterns['unique_actions'] = list(action_counts.keys())
        
        self.analysis_results['patterns'] = patterns
        return patterns
    
    def _get_strategy_section(self) -> Optional[Dict]:
        """Extract the strategy section from the loaded data."""
        if not self.strategy_data:
            return None
        
        if isinstance(self.strategy_data, dict):
            if 'strategy' in self.strategy_data:
                return self.strategy_data['strategy']
            else:
                # Maybe the whole file is the strategy
                return self.strategy_data
        
        return None
    
    def generate_situation_analysis(self, situation_filter: Optional[str] = None) -> Dict[str, Any]:
        """Generate analysis for specific poker situations."""
        strategy_section = self._get_strategy_section()
        if not strategy_section:
            return {}
        
        situations = {
            'pre_flop': defaultdict(list),
            'flop': defaultdict(list),
            'turn': defaultdict(list),
            'river': defaultdict(list)
        }
        
        print("Analyzing poker situations...")
        
        for info_set, actions in strategy_section.items():
            betting_round = self.decoder._estimate_betting_round(str(info_set))
            
            if situation_filter and betting_round != situation_filter:
                continue
            
            decoded_info = self.decoder.decode_info_set(info_set)
            
            situation_key = f"{betting_round}_situation"
            situations[betting_round][situation_key].append({
                'info_set': str(info_set),
                'actions': actions,
                'decoded': decoded_info
            })
        
        self.analysis_results['situations'] = situations
        return situations
    
    def generate_report(self, output_format: str = 'text', output_file: Optional[str] = None) -> str:
        """Generate human-readable strategy report."""
        if not self.strategy_data:
            return "No strategy data loaded."
        
        # Ensure we have analysis results
        if 'patterns' not in self.analysis_results:
            self.extract_patterns()
        
        if output_format == 'json':
            report = self._generate_json_report()
        else:
            report = self._generate_text_report()
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to {output_file}")
        
        return report
    
    def _generate_text_report(self) -> str:
        """Generate a human-readable text report."""
        lines = []
        lines.append("=" * 60)
        lines.append("POKER AI STRATEGY ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append("")
        
        # Structure analysis
        if 'structure' in self.analysis_results:
            structure = self.analysis_results['structure']
            lines.append("📊 STRATEGY FILE STRUCTURE")
            lines.append("-" * 30)
            lines.append(f"File type: {structure.get('type', 'Unknown')}")
            lines.append(f"File size: {structure.get('size', 'Unknown')} items")
            
            if 'keys' in structure:
                lines.append(f"Top-level keys: {structure['keys']}")
            
            if 'strategy_info' in structure:
                strategy_info = structure['strategy_info']
                lines.append(f"Number of information sets: {strategy_info.get('num_info_sets', 'Unknown')}")
            
            lines.append("")
        
        # Pattern analysis
        if 'patterns' in self.analysis_results:
            patterns = self.analysis_results['patterns']
            lines.append("🎯 STRATEGY PATTERNS")
            lines.append("-" * 30)
            lines.append(f"Total information sets analyzed: {patterns.get('total_info_sets', 0)}")
            lines.append(f"Unique actions found: {patterns.get('unique_actions', [])}")
            lines.append("")
            
            # Action frequencies
            lines.append("Action Frequencies (average probabilities):")
            action_freq = patterns.get('action_frequency', {})
            for action, freq in sorted(action_freq.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  {action}: {freq:.3f}")
            lines.append("")
            
            # Betting round distribution
            lines.append("Distribution by betting round:")
            round_dist = patterns.get('betting_rounds', {})
            total_sets = sum(round_dist.values())
            for betting_round, count in round_dist.items():
                percentage = (count / total_sets * 100) if total_sets > 0 else 0
                lines.append(f"  {betting_round}: {count} sets ({percentage:.1f}%)")
            lines.append("")
        
        # Sample strategy entries
        if 'structure' in self.analysis_results and 'sample_info_sets' in self.analysis_results['structure']:
            lines.append("📋 SAMPLE STRATEGY ENTRIES")
            lines.append("-" * 30)
            samples = self.analysis_results['structure']['sample_info_sets']
            for i, sample in enumerate(samples, 1):
                lines.append(f"Sample {i}:")
                lines.append(f"  Info Set: {sample['info_set']}")
                lines.append(f"  Actions: {sample['actions']}")
                lines.append("")
        
        lines.append("=" * 60)
        lines.append("Analysis complete. Use this data to understand AI strategy patterns.")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _generate_json_report(self) -> str:
        """Generate a JSON report."""
        return json.dumps(self.analysis_results, indent=2, default=str)


def create_sample_strategy():
    """Create a sample strategy file for testing."""
    sample_strategy = {
        'strategy': {
            'preflop_AKs_btn': {'fold': 0.05, 'call': 0.25, 'raise': 0.70},
            'preflop_22_utg': {'fold': 0.80, 'call': 0.20, 'raise': 0.00},
            'flop_AK2_toppair': {'fold': 0.10, 'call': 0.30, 'bet': 0.60},
            'turn_AK2Q_toptwo': {'fold': 0.05, 'call': 0.20, 'bet': 0.75},
            'river_AK2Q5_bluff': {'fold': 0.70, 'call': 0.10, 'bet': 0.20},
        },
        'regret': {},  # Would contain regret values
        'timestep': 1000,
        'pre_flop_strategy': {}
    }
    
    joblib.dump(sample_strategy, 'sample_strategy.joblib')
    print("Created sample_strategy.joblib for testing")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Analyze Poker AI Strategy Files')
    parser.add_argument('strategy_file', nargs='?', help='Path to strategy file (.joblib)')
    parser.add_argument('--card-lut', help='Path to card lookup table file')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--create-sample', action='store_true', help='Create a sample strategy file for testing')
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_strategy()
        return
    
    if not args.strategy_file:
        print("Please provide a strategy file path or use --create-sample")
        parser.print_help()
        return
    
    # Initialize analyzer
    decoder = InfoSetDecoder(args.card_lut)
    analyzer = StrategyAnalyzer(decoder)
    
    # Load and analyze strategy
    if not analyzer.load_strategy(args.strategy_file):
        print("Failed to load strategy file")
        return
    
    # Generate and display report
    report = analyzer.generate_report(args.format, args.output)
    
    if not args.output:
        print(report)


if __name__ == '__main__':
    main() 