#!/usr/bin/env python3"""Poker Strategy Decoder - DEPRECATED - Use poker_decoder_cli.py insteadThis file is kept for backward compatibilityRedirects to the new modular system with <200 line files"""print("⚠️  DEPRECATED: poker_strategy_decoder.py")print("🔄 Please use the new modular system:")print("   python poker_decoder_cli.py [strategy_file] [options]")print()print("📁 New file structure (all <200 lines):")print("   • poker_decoder_core.py - Core decoding functionality")print("   • poker_decoder_analysis.py - Analysis and filtering")print("   • poker_decoder_cli.py - Command-line interface")print("   • json_to_ppl.py - JSON to PPL conversion")print("   • run_complete_pipeline.py - Full pipeline runner")print()# Import and redirect to new systemimport sysimport subprocessif len(sys.argv) > 1:    print("🔄 Redirecting to poker_decoder_cli.py...")    cmd = ["python", "poker_decoder_cli.py"] + sys.argv[1:]    subprocess.run(cmd)else:    print("Usage: python poker_decoder_cli.py [strategy_file] [options]")sys.exit(0)# Keep original imports for any remaining importsimport joblibimport jsonfrom collections import defaultdict, Counterfrom typing import Dict, List, Tuple, Any

class PokerStrategyDecoder:
    """Decode poker AI strategies into human-readable format"""
    
    def __init__(self, strategy_file: str, card_lut_file: str = None):
        """Initialize the decoder with strategy and optional card lookup tables"""
        self.data = joblib.load(strategy_file)
        self.strategy = self.data.get('strategy', {})
        self.card_lut = None
        
        if card_lut_file:
            try:
                self.card_lut = joblib.load(card_lut_file)
                print(f"✅ Loaded card lookup tables from {card_lut_file}")
            except Exception as e:
                print(f"⚠️  Could not load card LUT: {e}")
        
        # Bet size mappings (these might need adjustment based on actual game setup)
        self.bet_size_map = {
            'call': 'call',
            'fold': 'fold',
            'raise': 'raise 1x',
            'raise:lv2': 'raise 2.5x',
            'raise:lv5': 'raise 5x', 
            'raise:lv50': 'raise 50x (all-in)',
            'check': 'check'
        }
        
        # Card rank mappings
        self.rank_map = {
            2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
            10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'
        }
        
        self.suit_map = ['♠', '♥', '♦', '♣']
        
    def decode_card_cluster(self, cluster_id: int) -> str:
        """Decode card cluster to human-readable cards"""
        if self.card_lut and cluster_id in range(10):  # Assuming clusters 0-9 for simplicity
            # Map clusters to representative hands
            cluster_hands = {
                0: "AA/KK (Premium Pairs)",
                1: "QQ/JJ (High Pairs)", 
                2: "TT-22 (Medium/Low Pairs)",
                3: "AK/AQ (Ace-High)",
                4: "AJ/AT (Ace-Medium)",
                5: "KQ/KJ (King-High)",
                6: "QJ/QT (Queen-High)",
                7: "JT/J9 (Jack-High)",
                8: "T9/98 (Suited Connectors)",
                9: "Random/Weak Hands"
            }
            return cluster_hands.get(cluster_id, f"Cluster {cluster_id}")
        else:
            return f"Hand Cluster {cluster_id}"
    
    def decode_betting_action(self, action: str) -> str:
        """Convert action codes to human-readable betting actions"""
        return self.bet_size_map.get(action, action)
    
    def get_position_from_history(self, history: List[Dict]) -> str:
        """Infer position from betting history"""
        if not history:
            return "Unknown Position"
        
        pre_flop = history[0].get('pre_flop', [])
        action_count = len(pre_flop)
        
        # Rough position mapping based on action order
        position_map = {
            0: "UTG", 1: "UTG+1", 2: "MP", 3: "MP+1", 
            4: "CO", 5: "BTN", 6: "SB", 7: "BB"
        }
        
        # This is a simplified heuristic
        if action_count <= 3:
            return "Early Position (UTG/MP)"
        elif action_count <= 5:
            return "Middle Position (MP/CO)"
        else:
            return "Late Position (BTN/Blinds)"
    
    def get_street_name(self, history: List[Dict]) -> str:
        """Determine current betting street"""
        if len(history) == 1:
            return "Pre-flop"
        elif len(history) == 2:
            return "Flop"
        elif len(history) == 3:
            return "Turn"
        elif len(history) == 4:
            return "River"
        else:
            return f"Street {len(history)}"
    
    def decode_situation(self, info_set_str: str) -> Dict[str, Any]:
        """Decode a complete poker situation from info set"""
        try:
            info_set = json.loads(info_set_str)
        except:
            return {"error": "Could not parse info set"}
        
        # Extract key information
        cards_cluster = info_set.get('cards_cluster', 0)
        history = info_set.get('history', [])
        
        # Decode components
        hand_description = self.decode_card_cluster(cards_cluster)
        position = self.get_position_from_history(history)
        street = self.get_street_name(history)
        
        # Analyze betting action
        current_action = "Facing action"
        if history:
            last_street = history[-1]
            for street_name, actions in last_street.items():
                if actions:
                    last_action = actions[-1]
                    if last_action.startswith('raise'):
                        current_action = f"Facing {self.decode_betting_action(last_action)}"
                    elif last_action == 'call':
                        current_action = "Facing call"
                    elif last_action == 'fold':
                        current_action = "After fold"
        
        return {
            'hand': hand_description,
            'position': position,
            'street': street,
            'situation': current_action,
            'raw_history': history
        }
    
    def get_readable_decisions(self, limit: int = 20) -> List[Dict]:
        """Get human-readable poker decisions"""
        decisions = []
        
        for i, (info_set_str, actions) in enumerate(list(self.strategy.items())[:limit]):
            # Decode the situation
            situation = self.decode_situation(info_set_str)
            
            # Convert actions to probabilities
            total = sum(actions.values())
            if total > 0:
                action_probs = {
                    self.decode_betting_action(action): prob/total 
                    for action, prob in actions.items()
                    if prob > 0  # Only show actions with positive probability
                }
                
                # Sort by probability
                sorted_actions = sorted(action_probs.items(), key=lambda x: x[1], reverse=True)
                
                decision = {
                    'hand': situation['hand'],
                    'position': situation['position'],
                    'street': situation['street'],
                    'situation': situation['situation'],
                    'actions': sorted_actions,
                    'top_action': sorted_actions[0] if sorted_actions else ('fold', 0.0)
                }
                
                decisions.append(decision)
        
        return decisions
    
    def print_readable_strategy(self, limit: int = 10):
        """Print human-readable strategy decisions"""
        print("🃏 POKER AI STRATEGY DECISIONS")
        print("=" * 80)
        print("Format: Hand | Position | Street | Situation → Decision (probability)")
        print("-" * 80)
        
        decisions = self.get_readable_decisions(limit)
        
        for i, decision in enumerate(decisions, 1):
            print(f"\n{i}. {decision['hand']}")
            print(f"   Position: {decision['position']}")
            print(f"   Street: {decision['street']}")
            print(f"   Situation: {decision['situation']}")
            print(f"   Decision: ", end="")
            
            # Show top 3 actions
            for j, (action, prob) in enumerate(decision['actions'][:3]):
                if j > 0:
                    print(", ", end="")
                print(f"{action} ({prob:.1%})", end="")
            print()
    
    def find_specific_situations(self, hand_type: str = None, position: str = None, street: str = None) -> List[Dict]:
        """Find specific poker situations matching criteria"""
        all_decisions = self.get_readable_decisions(limit=1000)
        
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


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Decode Poker AI Strategy to Human-Readable Format')
    parser.add_argument('strategy_file', help='Path to strategy file (.joblib)')
    parser.add_argument('--card-lut', help='Path to card lookup table file')
    parser.add_argument('--limit', type=int, default=10, help='Number of decisions to show')
    parser.add_argument('--hand-type', help='Analyze specific hand type (e.g., "AA", "AK", "pairs")')
    parser.add_argument('--position', help='Filter by position (e.g., "BTN", "early")')
    parser.add_argument('--street', help='Filter by street (e.g., "pre-flop", "flop")')
    
    args = parser.parse_args()
    
    # Initialize decoder
    decoder = PokerStrategyDecoder(args.strategy_file, args.card_lut)
    
    if args.hand_type:
        decoder.analyze_hand_type(args.hand_type)
    else:
        decoder.print_readable_strategy(args.limit)
    
    # Show examples of specific queries
    print("\n" + "="*80)
    print("🔍 EXAMPLE QUERIES:")
    print("python poker_strategy_decoder.py strategy.joblib --hand-type 'AA'")
    print("python poker_strategy_decoder.py strategy.joblib --position 'BTN' --street 'pre-flop'")
    print("python poker_strategy_decoder.py strategy.joblib --hand-type 'pairs' --limit 20")


if __name__ == "__main__":
    main() 