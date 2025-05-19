#!/usr/bin/env python
"""
PokerRL Setup Script

This script checks for PokerRL installation and helps set it up for the FEDOR project.
PokerRL is a reinforcement learning framework for poker games, used for MCCFR training.

Usage:
  python setup_pokerrl.py [--install]
"""
import os
import sys
import argparse
import subprocess
import importlib.util
from pathlib import Path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Setup PokerRL")
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install PokerRL if not already installed"
    )
    parser.add_argument(
        "--source-install",
        action="store_true",
        help="Install PokerRL from source (GitHub)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reinstallation even if already installed"
    )
    return parser.parse_args()


def check_pokerrl_installed():
    """
    Check if PokerRL is installed.
    
    Returns:
        bool: True if installed, False otherwise
    """
    try:
        import PokerRL
        print(f"PokerRL is installed (version: {PokerRL.__version__ if hasattr(PokerRL, '__version__') else 'unknown'})")
        return True
    except ImportError:
        print("PokerRL is not installed")
        return False


def run_command(command_list):
    """
    Run a command and return result.
    
    Args:
        command_list: List of command and arguments
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"Running: {' '.join(command_list)}")
    try:
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error: Command failed with code {process.returncode}")
            print(f"STDERR: {stderr}")
            return False
        
        print(stdout)
        return True
    except Exception as e:
        print(f"Exception running command: {e}")
        return False


def install_pokerrl_pip():
    """
    Install PokerRL using pip.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("\nInstalling PokerRL via pip...")
    return run_command([sys.executable, "-m", "pip", "install", "PokerRL"])


def install_pokerrl_source():
    """
    Install PokerRL from source (GitHub).
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("\nInstalling PokerRL from source...")
    temp_dir = Path("temp_pokerrl_install")
    
    # Create temp directory
    os.makedirs(temp_dir, exist_ok=True)
    
    # Clone repository
    if not run_command(["git", "clone", "https://github.com/TinkeringCode/PokerRL.git", str(temp_dir)]):
        print("Failed to clone PokerRL repository")
        return False
    
    # Install dependencies
    if not run_command([sys.executable, "-m", "pip", "install", "-r", str(temp_dir / "requirements.txt")]):
        print("Failed to install PokerRL dependencies")
        return False
    
    # Install package
    if not run_command([sys.executable, "-m", "pip", "install", "-e", str(temp_dir)]):
        print("Failed to install PokerRL package")
        return False
    
    print("PokerRL installed successfully from source")
    return True


def check_dependencies():
    """
    Check dependencies required for PokerRL.
    
    Returns:
        list: Missing dependencies
    """
    dependencies = ["numpy", "torch", "matplotlib", "tqdm", "tensorboard"]
    missing = []
    
    for dep in dependencies:
        if importlib.util.find_spec(dep) is None:
            missing.append(dep)
    
    return missing


def main():
    """Main function."""
    args = parse_args()
    
    # Check if PokerRL is already installed
    is_installed = check_pokerrl_installed()
    
    # Check if we need to install
    if is_installed and not args.force:
        print("PokerRL is already installed. Use --force to reinstall.")
        return 0
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("Installing missing dependencies...")
        if not run_command([sys.executable, "-m", "pip", "install", *missing_deps]):
            print("Failed to install dependencies")
            return 1
    
    # Install if requested
    if args.install or args.force:
        if args.source_install:
            success = install_pokerrl_source()
        else:
            success = install_pokerrl_pip()
        
        if not success:
            print("\nFailed to install PokerRL")
            print("Please try installing manually:")
            print("  pip install PokerRL")
            print("Or from source:")
            print("  git clone https://github.com/TinkeringCode/PokerRL.git")
            print("  cd PokerRL")
            print("  pip install -r requirements.txt")
            print("  pip install -e .")
            return 1
        
        # Verify installation
        if not check_pokerrl_installed():
            print("Installation verification failed")
            return 1
    else:
        if not is_installed:
            print("\nPokerRL is not installed. Run with --install to install it.")
            return 1
    
    print("\nPokerRL is ready for use with the FEDOR project.")
    print("You can now proceed with developing the MCCFR training components.")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 