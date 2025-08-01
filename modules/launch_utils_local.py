"""
Modified launch_utils.py for local dependencies in OpenXLab environment
"""
import os
import sys
import shutil
import importlib.util
from modules import launch_utils

# Copy all functions and variables from original launch_utils
from modules.launch_utils import *

# Store original functions
original_run_pip = run_pip
original_git_clone = git_clone

# Get the base directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
deps_dir = os.path.join(base_dir, "dependencies")

def check_and_copy_repo(repo_name, dest_path):
    """Check if local repo exists and copy it to destination"""
    local_repo = os.path.join(deps_dir, "repos", repo_name)
    if os.path.exists(local_repo):
        print(f"Using local repository: {repo_name}")
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        shutil.copytree(local_repo, dest_path)
        return True
    return False

def install_local_package(package_name):
    """Install a package from local dependencies"""
    local_package = os.path.join(deps_dir, "packages", f"{package_name}.zip")
    if os.path.exists(local_package):
        print(f"Installing local package: {package_name}")
        return run(f'"{python}" -m pip install "{local_package}" --prefer-binary', desc=f"Installing {package_name}", errdesc=f"Couldn't install {package_name}")
    return None

# Override run_pip to check for local packages first
def run_pip(command, desc=None, live=default_command_live):
    if args.skip_install:
        return
    
    # Check if this is a clip or open_clip installation
    if "clip" in desc.lower() and "install" in command:
        # Extract package URL from command
        parts = command.split()
        if "install" in parts:
            install_idx = parts.index("install")
            if install_idx + 1 < len(parts):
                package_url = parts[install_idx + 1]
                
                # Check for local packages
                if "CLIP/archive" in package_url and "openai" in package_url:
                    result = install_local_package("clip")
                    if result is not None:
                        return result
                elif "open_clip/archive" in package_url:
                    result = install_local_package("open_clip")
                    if result is not None:
                        return result
    
    # Fall back to original behavior
    return original_run_pip(command, desc, live)

# Override git_clone to use local repositories
def git_clone(url, dir, name, commithash=None):
    # Map URLs to local repo names
    repo_map = {
        "https://github.com/Stability-AI/stablediffusion.git": "stable-diffusion-stability-ai",
        "https://github.com/Stability-AI/generative-models.git": "generative-models",
        "https://github.com/crowsonkb/k-diffusion.git": "k-diffusion",
        "https://github.com/sczhou/CodeFormer.git": "CodeFormer",
        "https://github.com/salesforce/BLIP.git": "BLIP"
    }
    
    # Check if we have a local copy
    repo_name = repo_map.get(url)
    if repo_name and check_and_copy_repo(repo_name, dir):
        return
    
    # Fall back to original behavior
    return original_git_clone(url, dir, name, commithash)

# Override model download functions
def download_model(model_path, url):
    """Download a model file, checking local dependencies first"""
    # Extract filename from URL
    filename = os.path.basename(url)
    local_model = os.path.join(deps_dir, "models", filename)
    
    if os.path.exists(local_model):
        print(f"Using local model: {filename}")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        shutil.copy2(local_model, model_path)
        return
    
    # Fall back to original download if local not found
    print(f"Warning: Local model not found for {filename}, attempting download from {url}")
    from modules.modelloader import download_file
    download_file(url, model_path)

# Monkey patch the download functions in other modules
def patch_model_downloads():
    """Patch model download functions to use local files"""
    try:
        # Patch realesrgan_model
        import modules.realesrgan_model
        if hasattr(modules.realesrgan_model, 'download_model'):
            modules.realesrgan_model.download_model = download_model
    except:
        pass
    
    try:
        # Patch sd_models
        import modules.sd_models
        if hasattr(modules.sd_models, 'download_model'):
            modules.sd_models.download_model = download_model
    except:
        pass
    
    try:
        # Patch sd_vae_approx
        import modules.sd_vae_approx
        if hasattr(modules.sd_vae_approx, 'download_model'):
            modules.sd_vae_approx.download_model = download_model
    except:
        pass
    
    try:
        # Patch sd_vae_taesd
        import modules.sd_vae_taesd
        if hasattr(modules.sd_vae_taesd, 'download_model'):
            modules.sd_vae_taesd.download_model = download_model
    except:
        pass

# Apply patches when module is imported
patch_model_downloads()

print("Using local dependencies mode for OpenXLab deployment")