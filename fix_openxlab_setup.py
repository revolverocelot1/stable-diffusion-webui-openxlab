#!/usr/bin/env python3
"""
Fix OpenXLab setup issues for Stable Diffusion WebUI
Handles missing repositories, extensions, and model downloads with China-friendly mirrors
"""
import os
import subprocess
import shutil
import sys
import time

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description or cmd}")
    print(f"{'='*60}")
    
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0:
            print(f"Warning: {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def ensure_repositories():
    """Ensure all required repositories exist"""
    print("\n=== Checking repositories ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repos_dir = os.path.join(script_dir, "repositories")
    os.makedirs(repos_dir, exist_ok=True)
    
    # If local dependencies exist, copy them
    deps_repos = os.path.join(script_dir, "dependencies", "repos")
    if os.path.exists(deps_repos):
        print("Found local dependencies, copying repositories...")
        for repo_name in os.listdir(deps_repos):
            src = os.path.join(deps_repos, repo_name)
            dst = os.path.join(repos_dir, repo_name)
            if not os.path.exists(dst) and os.path.isdir(src):
                print(f"  Copying {repo_name}...")
                shutil.copytree(src, dst)
                print(f"  ✓ Copied {repo_name}")
    
    # Create empty directories for missing repos
    required_repos = [
        "stable-diffusion-stability-ai",
        "generative-models", 
        "k-diffusion",
        "CodeFormer",
        "BLIP"
    ]
    
    for repo in required_repos:
        repo_path = os.path.join(repos_dir, repo)
        if not os.path.exists(repo_path):
            print(f"  Creating placeholder for {repo}...")
            os.makedirs(repo_path, exist_ok=True)
            
            # Create a basic requirements.txt for CodeFormer
            if repo == "CodeFormer":
                req_file = os.path.join(repo_path, "requirements.txt")
                with open(req_file, "w") as f:
                    f.write("# CodeFormer requirements\n")
                    f.write("basicsr>=1.4.2\n")
                    f.write("facexlib>=0.3.0\n")
                    f.write("gfpgan>=1.3.8\n")
                    f.write("realesrgan>=0.3.0\n")
                    f.write("lpips\n")
    
    print("✓ Repositories check complete")

def ensure_extensions():
    """Ensure extensions directory exists"""
    print("\n=== Checking extensions ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extensions_dir = os.path.join(script_dir, "extensions")
    os.makedirs(extensions_dir, exist_ok=True)
    
    # Create placeholder for built-in extensions
    builtin_dir = os.path.join(script_dir, "extensions-builtin")
    os.makedirs(builtin_dir, exist_ok=True)
    
    print("✓ Extensions directories created")

def fix_launch_scripts():
    """Update launch scripts to handle OpenXLab environment"""
    print("\n=== Fixing launch scripts ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a launch wrapper for OpenXLab
    wrapper_content = '''#!/usr/bin/env python3
"""
OpenXLab launch wrapper for Stable Diffusion WebUI
"""
import os
import sys
import subprocess

# Set environment variables for OpenXLab
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['PIP_INDEX_URL'] = 'https://mirrors.aliyun.com/pypi/simple/'
os.environ['TORCH_INDEX_URL'] = 'https://mirrors.aliyun.com/pytorch-wheels/cu118'

# Use local repositories
script_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['STABLE_DIFFUSION_REPO'] = f'local://{os.path.join(script_dir, "repositories/stable-diffusion-stability-ai")}'
os.environ['STABLE_DIFFUSION_XL_REPO'] = f'local://{os.path.join(script_dir, "repositories/generative-models")}'
os.environ['K_DIFFUSION_REPO'] = f'local://{os.path.join(script_dir, "repositories/k-diffusion")}'
os.environ['CODEFORMER_REPO'] = f'local://{os.path.join(script_dir, "repositories/CodeFormer")}'
os.environ['BLIP_REPO'] = f'local://{os.path.join(script_dir, "repositories/BLIP")}'

# Launch the main script
if __name__ == "__main__":
    # Try to import launch first
    try:
        import launch
        launch.main()
    except Exception as e:
        print(f"Error launching: {e}")
        print("Trying alternative launch method...")
        
        # Alternative: run webui.py directly
        webui_path = os.path.join(script_dir, "webui.py")
        if os.path.exists(webui_path):
            subprocess.run([sys.executable, webui_path] + sys.argv[1:])
        else:
            print("Could not find webui.py")
'''
    
    wrapper_path = os.path.join(script_dir, "launch_openxlab.py")
    with open(wrapper_path, "w") as f:
        f.write(wrapper_content)
    
    print(f"✓ Created launch wrapper: {wrapper_path}")

def create_model_download_list():
    """Create a list of recommended models for OpenXLab"""
    print("\n=== Creating model download list ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    # Create subdirectories
    subdirs = ["Stable-diffusion", "VAE", "Lora", "ControlNet", "ESRGAN", "Codeformer"]
    for subdir in subdirs:
        os.makedirs(os.path.join(models_dir, subdir), exist_ok=True)
    
    # Create model download instructions
    instructions = '''# Recommended Models for OpenXLab Deployment

## Base Models (Place in models/Stable-diffusion/)

1. **Stable Diffusion XL Base**
   - Download: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
   - Mirror: Use Modelscope or OpenXLab mirror if available

2. **Realistic Vision V5.1**
   - Popular photorealistic model
   - Check CivitAI or local mirrors

## VAE Models (Place in models/VAE/)

1. **SDXL VAE**
   - Essential for SDXL models
   - Download from HuggingFace or mirrors

2. **SD 1.5 VAE**
   - vae-ft-mse-840000-ema-pruned.safetensors

## Extensions to Install

Run: python download_extensions.py

## Models Download

Run: python download_openxlab_models.py

## Troubleshooting

1. If downloads fail, try using a VPN or proxy
2. Use Gitee mirrors for GitHub repositories
3. Check OpenXLab model hub for China-friendly links
'''
    
    with open(os.path.join(script_dir, "MODELS_GUIDE.md"), "w") as f:
        f.write(instructions)
    
    print("✓ Created models guide: MODELS_GUIDE.md")

def main():
    print("=== Fixing OpenXLab Setup Issues ===")
    print("This script will fix common issues with OpenXLab deployment")
    
    # Run all fixes
    ensure_repositories()
    ensure_extensions()
    fix_launch_scripts()
    create_model_download_list()
    
    print("\n=== Setup Complete ===")
    print("\nNext steps:")
    print("1. Run: python download_dependencies.py")
    print("2. Run: python download_extensions.py")
    print("3. Run: python download_openxlab_models.py")
    print("4. Launch with: python launch_openxlab.py")
    print("\nCheck MODELS_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()