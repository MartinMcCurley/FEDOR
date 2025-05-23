#!/usr/bin/env python3
"""Simple demo conversion script without emoji characters"""

import json
from poker_decoder_core import PokerStrategyDecoder

def main():
    print("Converting sample strategy to JSON...")
    
    # Step 4: Convert to JSON
    decoder = PokerStrategyDecoder('sample_strategy.joblib')
    json_data = decoder.to_json_format()
    
    with open('demo_strategy.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"Exported {len(json_data['decisions'])} decisions to demo_strategy.json")
    
    # Step 5: Convert to PPL
    print("Converting JSON to PPL...")
    
    from json_to_ppl import convert_json_to_ppl
    convert_json_to_ppl('demo_strategy.json', 'demo_strategy.ppl')
    
    print("Generated demo_strategy.ppl")
    print("\nPipeline complete!")
    print("Files generated:")
    print("- demo_strategy.json")
    print("- demo_strategy.ppl")

if __name__ == "__main__":
    main() 