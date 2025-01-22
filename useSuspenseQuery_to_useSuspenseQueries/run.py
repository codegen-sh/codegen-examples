import os
import subprocess
import shutil


def run_command(command, cwd=None):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            command, cwd=cwd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {command} failed:")
        print(e.stderr)
        raise


def main():
    # Clone ThreatMapper repository
    print("\n🚀 Cloning ThreatMapper repository...")
    if os.path.exists("ThreatMapper"):
        shutil.rmtree("ThreatMapper")
    run_command("git clone https://github.com/deepfence/ThreatMapper")

    repo_path = os.path.join(os.getcwd(), "ThreatMapper")

    # Create and activate virtual environment
    print("\n🔧 Setting up virtual environment...")
    run_command("python3 -m venv venv", cwd=repo_path)
    run_command("source venv/bin/activate", cwd=repo_path)

    # Install codegen in the virtual environment
    venv_pip = os.path.join(repo_path, "venv", "bin", "pip")
    run_command(f"{venv_pip} install codegen")

    # Copy codemod.py to the repository
    print("\n📝 Creating codemod.py...")
    codemod_source = os.path.join(os.getcwd(), "codemod.py")
    codemod_dest = os.path.join(repo_path, "codemod.py")
    shutil.copy2(codemod_source, codemod_dest)

    # Run the codemod
    print("\n🔄 Running codemod...")
    venv_python = os.path.join(repo_path, "venv", "bin", "python")
    run_command(f"{venv_python} codemod.py", cwd=repo_path)

    # Show git status
    print("\n📊 Git status:")
    run_command("git status", cwd=repo_path)

    # Show git diff
    print("\n📝 Changes made:")
    try:
        diff_output = run_command("git diff", cwd=repo_path)
        print(diff_output)
    except subprocess.CalledProcessError:
        print("Unable to show diff")

    # Clean up by removing the ThreatMapper repository
    print("\n🧹 Cleaning up...")
    repo_folder = os.path.join(os.getcwd(), "ThreatMapper")
    if os.path.exists(repo_folder):
        shutil.rmtree(repo_folder)
        print("Removed ThreatMapper repository")


if __name__ == "__main__":
    main()
