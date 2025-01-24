import os
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        raise

def setup_git_repo(repo_path):
    """Initialize git repo and make initial commit"""
    print("🔧 Setting up git repository...")
    run_command("git init", cwd=repo_path)
    run_command("git add .", cwd=repo_path)
    run_command('git commit -m "Initial commit"', cwd=repo_path)
    print("✅ Git repository initialized and initial commit made")

def run_codemod(repo_path):
    """Run the codemod script"""
    print("\n🚀 Running codemod script...")
    codemod_path = os.path.join(repo_path, "codemod.py")
    run_command(f"python {codemod_path}", cwd=repo_path)
    print("✅ Codemod script completed")

def get_git_diff(repo_path):
    """Get the git diff of changes"""
    print("\n📝 Getting diff of changes...")
    return run_command("git diff HEAD", cwd=repo_path)

def cleanup_git(repo_path):
    """Remove git repository"""
    print("\n🧹 Cleaning up git repository...")
    git_dir = os.path.join(repo_path, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
    print("✅ Git repository removed")

def main():
    # Path to the example directory
    example_dir = os.path.join(os.path.dirname(__file__), "example")
    
    try:
        # Ensure we're starting clean
        cleanup_git(example_dir)
        
        # Setup git repo and run codemod
        setup_git_repo(example_dir)
        run_codemod(example_dir)
        
        # Get and display the diff
        diff = get_git_diff(example_dir)
        if diff:
            print("\n📊 Changes made by codemod:")
            print("=" * 80)
            print(diff)
            print("=" * 80)
        else:
            print("\n📊 No changes were made by the codemod")
            
        # Cleanup
        cleanup_git(example_dir)
        print("\n✨ Process completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        # Ensure cleanup happens even if there's an error
        cleanup_git(example_dir)
        raise

if __name__ == "__main__":
    main()
