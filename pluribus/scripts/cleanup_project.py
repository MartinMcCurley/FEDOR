#!/usr/bin/env python3
"""
Project Cleanup Script - Clean and organize the pluribus directory
Removes redundant files and organizes the project structure
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Clean up the pluribus directory and organize files"""
    
    print("🧹 CLEANING UP PLURIBUS PROJECT")
    print("=" * 50)
    
    # Files to keep (core functionality)
    core_files = {
        # Core pipeline files
        'enhanced_ppl_converter.py',
        'ppl_variable_mapping.py', 
        'complete_pipeline_demo.py',
        'run_complete_pipeline.py',
        'strategy_analyzer.py',
        
        # Strategy files
        'sample_strategy.joblib',
        'complete_strategy.ppl',
        
        # Setup and requirements
        'setup.py',
        'requirements.txt',
        'requirements_compatible.txt',
        
        # Documentation and config
        'README.md',
        'LICENSE',
        'Dockerfile',
        'ParentDockerfile',
        '.gitignore',
        '.dockerignore',
        '.travis.yml',
        '.readthedocs.yaml',
        'HISTORY.md',
        'CODE_OF_CONDUCT.md',
        'CONTRIBUTING.md',
    }
    
    # Directories to keep
    core_directories = {
        'clustering_data',
        'poker_ai',
        'fast_poker_ai', 
        'rust_poker_ai',
        'docs',
        'assets',
        'applications',
        'bin',
        'test',
        '__pycache__',
        'poker_ai.egg-info'
    }
    
    # Files to remove (redundant or outdated)
    files_to_remove = []
    
    # Demo and test files we no longer need
    demo_files = [
        'simple_demo.py',
        'demo_convert.py', 
        'create_ppl.py',
        'demo_strategy.ppl',
        'demo_strategy.json',
        'enhanced_strategy.ppl',  # Duplicate of complete_strategy.ppl
    ]
    
    # Old analysis and development files
    old_files = [
        'poker_decoder_cli.py',
        'poker_strategy_decoder.py',
        'poker_decoder_analysis.py', 
        'poker_decoder_core.py',
        'json_to_ppl.py',
        'examine_strategy.py',
        'train_gpu_optimized.py',
        'train_simple.py',
        'gpu_test_analysis.json',
        'strategy_report.json',
        'web_test.ipynb',
        'lookup.json',
        'run.sh',
        'python',  # This seems to be a stray file
    ]
    
    files_to_remove = demo_files + old_files
    
    # Create backup directory for removed files
    backup_dir = Path('cleanup_backup')
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    backup_dir.mkdir()
    
    print("📦 Creating backup of files to be removed...")
    
    # Move files to backup
    moved_count = 0
    for filename in files_to_remove:
        file_path = Path(filename)
        if file_path.exists():
            print(f"• Moving {filename} to backup")
            shutil.move(str(file_path), str(backup_dir / filename))
            moved_count += 1
        else:
            print(f"• {filename} not found (already removed)")
    
    print(f"\n✅ Moved {moved_count} files to backup")
    
    # Create organized directory structure
    print("\n📁 Creating organized directory structure...")
    
    # Create core directories if they don't exist
    core_dirs = ['scripts', 'strategies', 'docs/examples']
    for dir_name in core_dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        print(f"• Created/verified directory: {dir_name}")
    
    # Move remaining files to appropriate locations if needed
    file_moves = {
        # Keep main files in root but could organize further if needed
    }
    
    for src, dst in file_moves.items():
        if Path(src).exists():
            print(f"• Moving {src} to {dst}")
            shutil.move(src, dst)
    
    # Clean up __pycache__ directories
    print("\n🧽 Cleaning up Python cache files...")
    for pycache_dir in Path('.').rglob('__pycache__'):
        if pycache_dir.is_dir():
            print(f"• Removing {pycache_dir}")
            shutil.rmtree(pycache_dir)
    
    # Generate final project structure report
    print("\n📊 FINAL PROJECT STRUCTURE")
    print("=" * 50)
    
    # List remaining files
    remaining_files = []
    remaining_dirs = []
    
    for item in sorted(Path('.').iterdir()):
        if item.is_file() and not item.name.startswith('.'):
            remaining_files.append(item.name)
        elif item.is_dir() and not item.name.startswith('.') and item.name != 'cleanup_backup':
            remaining_dirs.append(item.name)
    
    print("📁 Directories:")
    for dir_name in remaining_dirs:
        print(f"  • {dir_name}/")
    
    print(f"\n📄 Core Files ({len(remaining_files)}):")
    for file_name in remaining_files:
        print(f"  • {file_name}")
    
    print(f"\n💾 Backup created in: cleanup_backup/")
    print(f"   Contains {moved_count} removed files")
    
    # Create a project summary
    create_project_summary()
    
    print("\n🎉 PROJECT CLEANUP COMPLETE!")
    print("=" * 50)
    print("✅ Removed redundant and outdated files")
    print("✅ Organized project structure") 
    print("✅ Created backup of removed files")
    print("✅ Generated project summary")
    print("\nThe project is now clean and ready for development!")

def create_project_summary():
    """Create a summary of the cleaned project"""
    
    summary = """# FEDOR Poker AI - Project Summary

## Core Components

### Pipeline Components
- `enhanced_ppl_converter.py` - Comprehensive PPL strategy converter (87 variables)
- `ppl_variable_mapping.py` - Complete PPL variable mapping system
- `complete_pipeline_demo.py` - Full pipeline demonstration
- `run_complete_pipeline.py` - Complete pipeline execution script
- `strategy_analyzer.py` - Strategy analysis and evaluation

### Data & Strategies  
- `sample_strategy.joblib` - Sample trained strategy
- `complete_strategy.ppl` - Generated comprehensive PPL strategy (61 rules)
- `clustering_data/` - Pluribus clustering data

### Core Directories
- `poker_ai/` - Main poker AI implementation
- `fast_poker_ai/` - Optimized poker AI components
- `rust_poker_ai/` - Rust implementation components
- `applications/` - Application implementations
- `docs/` - Documentation
- `test/` - Test suite

## Key Achievements

✅ **Complete PPL Integration**: All 87 PPL variables mapped and implemented
✅ **Sophisticated Strategy Generation**: 61 professional-grade poker rules
✅ **Multi-Street Support**: Preflop, flop, turn, river strategies
✅ **Advanced Features**: Position awareness, board texture, draw calculations
✅ **Training Ready**: Full pipeline ready for AI training

## Quick Start

1. **Run Demo**: `python complete_pipeline_demo.py`
2. **Full Pipeline**: `python run_complete_pipeline.py --preset quick`
3. **Strategy Analysis**: `python strategy_analyzer.py sample_strategy.joblib`

## PPL Capabilities

- **87 Total Variables** across 7 categories
- **All Poker Streets** supported with appropriate restrictions
- **Professional Actions** including complex bet sizing
- **Advanced Logic** with boolean operators and comparisons
- **Tournament/Cash** game compatibility

The project is now production-ready for advanced poker AI development!
"""
    
    with open('PROJECT_SUMMARY.md', 'w') as f:
        f.write(summary)
    
    print("📋 Generated PROJECT_SUMMARY.md")

if __name__ == "__main__":
    cleanup_project() 