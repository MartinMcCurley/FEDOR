#!/usr/bin/env python
"""
GTO Chart Processing Script

This script processes GTO chart files (PDF, HTML, etc.) from the raw_gto_charts directory
and generates standardized CSV output in the parsed_gto_data directory.

Usage:
  python process_charts.py [--charts-dir=<charts-dir>] [--output-dir=<output-dir>]
"""
import os
import sys
import argparse
import pandas as pd
from pathlib import Path
import glob
from typing import List, Dict, Any

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from src.parsing.parser_factory import ParserFactory


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process GTO chart files")
    parser.add_argument(
        "--charts-dir",
        default="data/raw_gto_charts",
        help="Directory containing raw GTO charts to process"
    )
    parser.add_argument(
        "--output-dir",
        default="data/parsed_gto_data",
        help="Directory for parsed output"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()


def find_chart_files(charts_dir: str) -> Dict[str, List[str]]:
    """
    Find all chart files in the specified directory and subdirectories.
    
    Args:
        charts_dir: Directory containing raw GTO charts
        
    Returns:
        Dictionary mapping chart types to lists of file paths
    """
    # Create dictionary to store file paths by type
    chart_files = {
        "preflop": [],
        "push_fold": [],
        "other": []
    }
    
    # Get absolute path
    base_dir = Path(charts_dir).absolute()
    
    # Find all supported file types
    supported_exts = ParserFactory.get_supported_extensions()
    for ext in supported_exts:
        # Check preflop directory
        preflop_files = glob.glob(str(base_dir / "preflop" / f"*{ext}"))
        chart_files["preflop"].extend(preflop_files)
        
        # Check push_fold directory
        push_fold_files = glob.glob(str(base_dir / "push_fold" / f"*{ext}"))
        chart_files["push_fold"].extend(push_fold_files)
        
        # Check any files directly in the charts directory
        other_files = glob.glob(str(base_dir / f"*{ext}"))
        chart_files["other"].extend(other_files)
    
    return chart_files


def process_chart_files(chart_files: Dict[str, List[str]], output_dir: str, verbose: bool = False) -> Dict[str, pd.DataFrame]:
    """
    Process all chart files and generate standardized DataFrames.
    
    Args:
        chart_files: Dictionary mapping chart types to lists of file paths
        output_dir: Directory for parsed output
        verbose: Whether to print verbose output
        
    Returns:
        Dictionary mapping chart types to DataFrames
    """
    results = {}
    
    # Process each chart type
    for chart_type, file_paths in chart_files.items():
        if not file_paths:
            if verbose:
                print(f"No {chart_type} chart files found.")
            continue
        
        # Process each file
        dfs = []
        for file_path in file_paths:
            if verbose:
                print(f"Processing {file_path}...")
            
            try:
                # Use ParserFactory to select appropriate parser
                parser = ParserFactory.create_parser(file_path)
                df = parser.parse(file_path)
                
                # Add source file information
                df["source_file"] = os.path.basename(file_path)
                
                dfs.append(df)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        if dfs:
            # Combine DataFrames
            combined_df = pd.concat(dfs, ignore_index=True)
            results[chart_type] = combined_df
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Save to CSV
            output_path = os.path.join(output_dir, f"{chart_type}_compiled.csv")
            combined_df.to_csv(output_path, index=False)
            if verbose:
                print(f"Saved {len(combined_df)} rows to {output_path}")
    
    return results


def main():
    """Main function."""
    args = parse_args()
    
    print(f"Looking for chart files in {args.charts_dir}...")
    chart_files = find_chart_files(args.charts_dir)
    
    # Count total files
    total_files = sum(len(files) for files in chart_files.values())
    if total_files == 0:
        print(f"No chart files found in {args.charts_dir}")
        print("Please add GTO chart files to the following directories:")
        print(f"  - {Path(args.charts_dir) / 'preflop'}")
        print(f"  - {Path(args.charts_dir) / 'push_fold'}")
        return 1
    
    print(f"Found {total_files} chart files to process.")
    
    # Process charts
    results = process_chart_files(chart_files, args.output_dir, args.verbose)
    
    # Print summary
    print("\nProcessing complete!")
    for chart_type, df in results.items():
        print(f"  - {chart_type}: {len(df)} rows")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 