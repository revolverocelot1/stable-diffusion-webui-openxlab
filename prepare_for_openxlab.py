#!/usr/bin/env python3
"""
Prepare repository for OpenXLab deployment by downloading all dependencies
and committing them to git.
"""
import os
import subprocess
import sys
import argparse

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description or cmd}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    if result.stdout:
        print(result.stdout)
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Prepare repository for OpenXLab deployment")
    parser.add_argument("--skip-download", action="store_true", help="Skip downloading dependencies")
    parser.add_argument("--skip-git", action="store_true", help="Skip git operations")
    parser.add_argument("--commit-message", default="Add local dependencies for OpenXLab deployment", help="Git commit message")
    args = parser.parse_args()
    
    # Step 1: Download dependencies
    if not args.skip_download:
        print("\n=== STEP 1: Downloading Dependencies ===")
        if os.path.exists("dependencies"):
            response = input("Dependencies directory already exists. Delete and re-download? (y/n): ")
            if response.lower() == 'y':
                import shutil
                shutil.rmtree("dependencies")
            else:
                print("Skipping download...")
        
        if not os.path.exists("dependencies"):
            if not run_command("python download_dependencies.py", "Downloading all dependencies"):
                print("Failed to download dependencies!")
                return 1
    
    # Step 2: Check if dependencies were downloaded
    if not os.path.exists("dependencies"):
        print("Error: dependencies directory not found!")
        return 1
    
    # Count files in dependencies
    total_files = 0
    for root, dirs, files in os.walk("dependencies"):
        total_files += len(files)
    
    print(f"\nFound {total_files} files in dependencies directory")
    
    # Step 3: Git operations
    if not args.skip_git:
        print("\n=== STEP 2: Git Operations ===")
        
        # Check git status
        result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error: Not in a git repository!")
            return 1
        
        # Add files to git
        print("\nAdding files to git...")
        files_to_add = [
            "dependencies/",
            "download_dependencies.py",
            "modules/launch_utils_local.py",
            "README_OPENXLAB.md",
            "prepare_for_openxlab.py",
            "launch.py",
            "app.py"
        ]
        
        for file in files_to_add:
            if os.path.exists(file):
                run_command(f"git add {file}", f"Adding {file}")
        
        # Show what will be committed
        print("\nFiles to be committed:")
        run_command("git status --cached")
        
        # Commit
        response = input("\nProceed with commit? (y/n): ")
        if response.lower() == 'y':
            run_command(f'git commit -m "{args.commit_message}"', "Committing changes")
            
            # Ask about push
            response = input("\nPush to remote? (y/n): ")
            if response.lower() == 'y':
                run_command("git push", "Pushing to remote")
    
    print("\n=== DONE ===")
    print("\nYour repository is now prepared for OpenXLab deployment!")
    print("\nNext steps:")
    print("1. Deploy your repository to OpenXLab")
    print("2. The system will automatically use local dependencies")
    print("3. Check README_OPENXLAB.md for more information")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())