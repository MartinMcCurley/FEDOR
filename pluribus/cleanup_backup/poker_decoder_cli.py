#!/usr/bin/env python3
"""
Poker Strategy Decoder CLI - Command-line interface
Part of the complete pipeline: Clustering → Training → Output → JSON → PPL
"""

import argparse
import sys
from poker_decoder_core import PokerStrategyDecoder
from poker_decoder_analysis import PokerStrategyAnalyzer

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(
        description='Decode Poker AI Strategy to Human-Readable Format\n'
                   'Pipeline: Clustering → Training → Output → JSON → PPL'
    )
    
    # Required arguments
    parser.add_argument('strategy_file', help='Path to strategy file (.joblib)')
    
    # Optional arguments
    parser.add_argument('--card-lut', help='Path to card lookup table file')
    parser.add_argument('--limit', type=int, default=10, help='Number of decisions to show')
    
    # Filtering options
    parser.add_argument('--hand-type', help='Analyze specific hand type (e.g., "AA", "AK", "pairs")')
    parser.add_argument('--position', help='Filter by position (e.g., "BTN", "early")')
    parser.add_argument('--street', help='Filter by street (e.g., "pre-flop", "flop")')
    
    # Output options
    parser.add_argument('--output-json', help='Export to JSON file for pipeline step 4')
    parser.add_argument('--analysis', action='store_true', help='Show detailed analysis')
    parser.add_argument('--stats', action='store_true', help='Show summary statistics')
    
    args = parser.parse_args()
    
    try:
        # Initialize decoder
        print("🔄 Initializing poker strategy decoder...")
        decoder = PokerStrategyDecoder(args.strategy_file, args.card_lut)
        analyzer = PokerStrategyAnalyzer(decoder)
        
        # Handle JSON export for pipeline step 4
        if args.output_json:
            print(f"📤 Exporting to JSON format for pipeline step 4...")
            if args.hand_type or args.position or args.street:
                analyzer.export_filtered_json(args.output_json, args.hand_type, args.position, args.street)
            else:
                json_data = decoder.to_json_format()
                import json
                with open(args.output_json, 'w') as f:
                    json.dump(json_data, f, indent=2)
                print(f"✅ Exported {len(json_data['decisions'])} decisions to {args.output_json}")
            return
        
        # Handle specific analysis requests
        if args.hand_type:
            analyzer.analyze_hand_type(args.hand_type)
        elif args.analysis:
            print("🔍 Performing comprehensive analysis...")
            analyzer.print_summary_stats()
            analyzer.print_position_analysis()
            analyzer.print_street_analysis()
        elif args.stats:
            analyzer.print_summary_stats()
        else:
            # Default: show human-readable strategy
            decoder.print_readable_strategy(args.limit)
        
        # Show pipeline progress
        print("\n" + "="*80)
        print("🔧 PIPELINE PROGRESS:")
        print("✅ Step 1: Pluribus clustering (completed)")
        print("✅ Step 2: Pluribus training (completed)")
        print("✅ Step 3: Pluribus output file (completed)")
        print("✅ Step 4: Convert to JSON (available with --output-json)")
        print("⏳ Step 5: Convert to PPL language (next step)")
        
        print("\n🔍 EXAMPLE QUERIES:")
        print(f"python {sys.argv[0]} {args.strategy_file} --hand-type 'AA'")
        print(f"python {sys.argv[0]} {args.strategy_file} --position 'BTN' --street 'pre-flop'")
        print(f"python {sys.argv[0]} {args.strategy_file} --output-json strategy.json")
        print(f"python {sys.argv[0]} {args.strategy_file} --analysis")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find strategy file '{args.strategy_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 