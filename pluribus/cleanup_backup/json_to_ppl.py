#!/usr/bin/env python3
"""
JSON to PPL Converter - Convert JSON strategy to Policy Programming Language
Part of the complete pipeline: Clustering → Training → Output → JSON → PPL
"""

import json
import argparse
from typing import Dict, List

class PPLConverter:
    """Convert JSON strategy format to Policy Programming Language (PPL)"""
    
    def __init__(self):
        """Initialize the PPL converter"""
        self.ppl_rules = []
        
    def convert_decision_to_ppl(self, decision: Dict) -> str:
        """Convert a single decision to PPL format"""
        hand = decision.get('hand', 'Unknown')
        position = decision.get('position', 'Unknown')
        street = decision.get('street', 'Unknown') 
        situation = decision.get('situation', 'Unknown')
        actions = decision.get('actions', [])
        
        if not actions:
            return ""
        
        # PPL rule format: WHEN [conditions] THEN [action] [probability]
        conditions = []
        
        # Add hand condition
        if 'Premium Pairs' in hand:
            conditions.append("hand IN [AA, KK]")
        elif 'High Pairs' in hand:
            conditions.append("hand IN [QQ, JJ]")
        elif 'Ace-High' in hand:
            conditions.append("hand IN [AK, AQ]")
        elif 'pairs' in hand.lower():
            conditions.append("hand_type = PAIR")
        else:
            conditions.append(f"hand_cluster = '{hand}'")
        
        # Add position condition
        if 'Early' in position:
            conditions.append("position IN [UTG, UTG+1, MP]")
        elif 'Middle' in position:
            conditions.append("position IN [MP+1, CO]")
        elif 'Late' in position:
            conditions.append("position IN [BTN, SB, BB]")
        else:
            conditions.append(f"position = '{position}'")
        
        # Add street condition
        conditions.append(f"street = {street.upper()}")
        
        # Add situation condition if specific
        if 'Facing' in situation:
            conditions.append(f"facing_action = '{situation}'")
        
        # Create PPL rule
        condition_str = " AND ".join(conditions)
        
        # Add primary action
        primary_action, primary_prob = actions[0]
        ppl_rule = f"WHEN {condition_str} THEN {primary_action.upper()} ({primary_prob:.1%})"
        
        # Add alternative actions if significant
        alternatives = []
        for action, prob in actions[1:3]:  # Top 3 actions
            if prob > 0.15:  # Only include if >15% probability
                alternatives.append(f"OR {action.upper()} ({prob:.1%})")
        
        if alternatives:
            ppl_rule += " " + " ".join(alternatives)
        
        return ppl_rule
    
    def load_json_strategy(self, json_file: str) -> Dict:
        """Load strategy from JSON file"""
        with open(json_file, 'r') as f:
            return json.load(f)
    
    def convert_to_ppl(self, json_file: str) -> List[str]:
        """Convert entire JSON strategy to PPL format"""
        strategy_data = self.load_json_strategy(json_file)
        decisions = strategy_data.get('decisions', [])
        
        ppl_rules = []
        for decision in decisions:
            ppl_rule = self.convert_decision_to_ppl(decision)
            if ppl_rule:
                ppl_rules.append(ppl_rule)
        
        return ppl_rules
    
    def generate_ppl_header(self, metadata: Dict) -> str:
        """Generate PPL file header with metadata"""
        header = f"""# Poker Policy Programming Language (PPL)
# Generated from Pluribus AI Training Pipeline
# Source: {metadata.get('source', 'unknown')}
# Total Information Sets: {metadata.get('total_info_sets', 0)}
# Training Timestep: {metadata.get('timestep', 0)}
# Format Version: {metadata.get('format_version', '1.0')}

# PPL Syntax:
# WHEN [conditions] THEN [action] ([probability]) [OR [alternative_action] ([probability])]
# Conditions: hand, position, street, facing_action
# Actions: FOLD, CALL, RAISE, CHECK

"""
        return header
    
    def export_ppl(self, json_file: str, output_file: str):
        """Export complete PPL strategy file"""
        strategy_data = self.load_json_strategy(json_file)
        metadata = strategy_data.get('metadata', {})
        
        # Generate PPL content
        header = self.generate_ppl_header(metadata)
        ppl_rules = self.convert_to_ppl(json_file)
        
        # Write PPL file
        with open(output_file, 'w') as f:
            f.write(header)
            f.write("# STRATEGY RULES\n")
            f.write("# " + "="*50 + "\n\n")
            
            for i, rule in enumerate(ppl_rules, 1):
                f.write(f"RULE_{i:03d}: {rule}\n")
        
        print(f"✅ Exported {len(ppl_rules)} PPL rules to {output_file}")
    
    def print_ppl_sample(self, json_file: str, limit: int = 10):
        """Print sample PPL rules to console"""
        ppl_rules = self.convert_to_ppl(json_file)
        
        print("🎯 POLICY PROGRAMMING LANGUAGE (PPL) SAMPLE")
        print("=" * 80)
        print("Pipeline Step 5: JSON → PPL Conversion Complete")
        print("-" * 80)
        
        for i, rule in enumerate(ppl_rules[:limit], 1):
            print(f"RULE_{i:03d}: {rule}")
        
        if len(ppl_rules) > limit:
            print(f"\n... and {len(ppl_rules) - limit} more rules")
        
        print(f"\nTotal PPL rules generated: {len(ppl_rules)}")

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(
        description='Convert JSON strategy to Policy Programming Language (PPL)\n'
                   'Final step: Clustering → Training → Output → JSON → PPL'
    )
    
    parser.add_argument('json_file', help='Path to JSON strategy file')
    parser.add_argument('--output', '-o', help='Output PPL file path')
    parser.add_argument('--sample', action='store_true', help='Show sample PPL rules')
    parser.add_argument('--limit', type=int, default=10, help='Number of sample rules to show')
    
    args = parser.parse_args()
    
    try:
        converter = PPLConverter()
        
        if args.output:
            print("🔄 Converting JSON to PPL format...")
            converter.export_ppl(args.json_file, args.output)
            
            # Also show sample
            print("\n📋 Sample PPL rules:")
            converter.print_ppl_sample(args.json_file, 5)
        else:
            # Just show sample by default
            converter.print_ppl_sample(args.json_file, args.limit)
        
        print("\n🎉 PIPELINE COMPLETE!")
        print("✅ Step 1: Pluribus clustering")
        print("✅ Step 2: Pluribus training") 
        print("✅ Step 3: Pluribus output file")
        print("✅ Step 4: Convert to JSON")
        print("✅ Step 5: Convert to PPL language")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find JSON file '{args.json_file}'")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 