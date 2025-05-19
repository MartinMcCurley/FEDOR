#!/usr/bin/env python
"""
OpenHoldem Development Environment Setup Script

This script helps set up a development environment for OpenHoldem integration,
including creating necessary directories and placeholders for:
1. OpenPPL profile directories
2. DLL interfaces
3. Test configurations

Usage:
  python setup_openholdem.py --oh-path=<path-to-openholdem> [--force]
"""
import os
import sys
import argparse
import shutil
from pathlib import Path

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Setup OpenHoldem development environment")
    parser.add_argument(
        "--oh-path", 
        required=True, 
        help="Path to OpenHoldem installation directory"
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force overwrite existing files"
    )
    return parser.parse_args()

def create_dir(path, force=False):
    """Create directory if it doesn't exist."""
    if os.path.exists(path) and not force:
        print(f"Directory already exists: {path}")
        return False
    
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")
    return True

def create_file(path, content="", force=False):
    """Create file with given content if it doesn't exist."""
    if os.path.exists(path) and not force:
        print(f"File already exists: {path}")
        return False
    
    with open(path, "w") as f:
        f.write(content)
    print(f"Created file: {path}")
    return True

def main():
    """Main function."""
    args = parse_args()
    
    # Validate OpenHoldem path
    oh_path = Path(args.oh_path)
    if not oh_path.exists() or not oh_path.is_dir():
        print(f"Error: OpenHoldem directory not found: {oh_path}")
        return 1
    
    # Expected OH executable
    oh_exe = oh_path / "OpenHoldem.exe"
    if not oh_exe.exists():
        print(f"Error: OpenHoldem.exe not found in {oh_path}")
        print("Please provide the correct path to OpenHoldem installation.")
        return 1
    
    print(f"OpenHoldem found at: {oh_path}")
    
    # Create directories in the OpenHoldem folder
    profiles_dir = oh_path / "profiles"
    create_dir(profiles_dir, args.force)
    
    # Create placeholder for the FEDOR profile
    fedor_profile = profiles_dir / "FEDOR.txt"
    fedor_content = """##OpenPPL##
##4. Preflop##

WHEN hand$AA RaiseMax FORCE
WHEN hand$KK RaiseMax FORCE
WHEN hand$QQ RaiseMax FORCE
WHEN hand$AKs RaiseMax FORCE
WHEN Others Fold FORCE

##5. Flop##
WHEN Others Fold FORCE

##6. Turn##
WHEN Others Fold FORCE

##7. River##
WHEN Others Fold FORCE
"""
    create_file(fedor_profile, fedor_content, args.force)
    
    # Create DLL directory if needed
    dll_dir = oh_path / "dll"
    create_dir(dll_dir, args.force)
    
    # Create a placeholder for the helper DLL
    # In a real setup, you would copy the actual DLL here
    helper_dll_path = dll_dir / "README.txt"
    helper_dll_content = """
FEDOR helper DLL should be placed in this directory.
The DLL will be developed in the FEDOR/src/cpp_dll directory.
Once compiled, copy FEDOR_Helpers.dll to this directory.
"""
    create_file(helper_dll_path, helper_dll_content, args.force)
    
    # Create a symbolic link from the project to the OpenHoldem profiles
    project_root = Path(__file__).parent.parent
    project_profiles = project_root / "profiles"
    
    # Create a test profile in the project
    test_profile = project_profiles / "test_profile.txt"
    create_file(test_profile, fedor_content, args.force)
    
    print("\nOpenHoldem development environment setup complete!")
    print(f"OpenHoldem Path: {oh_path}")
    print(f"Profiles Directory: {profiles_dir}")
    print(f"Project Test Profile: {test_profile}")
    print("\nNext steps:")
    print("1. Develop and test profiles in the project's profiles/ directory")
    print("2. Create C++ helper DLL in src/cpp_dll/ directory")
    print("3. Use the unit tests to verify parsing functionality")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 