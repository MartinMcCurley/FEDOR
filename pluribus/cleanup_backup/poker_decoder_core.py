#!/usr/bin/env python3
"""
Poker Strategy Decoder Core - Core functionality for decoding AI strategies
Part of the complete pipeline: Clustering → Training → Output → JSON → PPL
"""

import joblib
import json
from typing import Dict, List, Any

class PokerStrategyDecoder:
    """Core decoder for poker AI strategies into human-readable format"""
    
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
        
        # Bet size mappings (adjustable based on game setup)
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
        if self.card_lut and cluster_id in range(10):
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
        
        # Simplified position mapping based on action order
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
    
    def to_json_format(self, limit: int = None) -> Dict:
        """Convert strategy to JSON format for pipeline step 4"""
        decisions = self.get_readable_decisions(limit or len(self.strategy))
        
        return {
            "pipeline_step": "json_conversion", 
            "source": "pluribus_training",
            "decisions": decisions,
            "metadata": {
                "total_info_sets": len(self.strategy),
                "timestep": self.data.get('timestep', 0),
                "format_version": "1.0"
            }
        }
    
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