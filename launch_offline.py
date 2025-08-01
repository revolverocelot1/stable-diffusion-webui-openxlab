#!/usr/bin/env python3
"""
Offline launcher for Stable Diffusion WebUI in restricted environments
This script configures the environment to work without GitHub/Hugging Face access
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_environment():
    """Set up environment variables for offline mode"""
    print("Setting up offline environment...")
    
    # Enable local dependencies mode
    os.environ['USE_LOCAL_DEPS'] = 'true'
    
    # Configure PyPI mirror
    os.environ['PIP_INDEX_URL'] = 'https://mirrors.aliyun.com/pypi/simple/'
    
    # Skip git operations
    os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'
    os.environ['GIT_OPTIONAL_LOCKS'] = '0'
    
    # Configure CLIP packages to use pip instead of GitHub
    os.environ['CLIP_PACKAGE'] = 'clip==1.0'
    os.environ['OPENCLIP_PACKAGE'] = 'open_clip_torch'
    
    # Configure torch index
    os.environ['TORCH_INDEX_URL'] = 'https://mirrors.aliyun.com/pytorch-wheels/cu118'
    
    # Skip network checks
    os.environ['COMMANDLINE_ARGS'] = '--skip-torch-cuda-test --no-download-sd-model --skip-version-check'
    
    print("Environment configured for offline mode")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = ['torch', 'torchvision', 'gradio', 'transformers']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please run install_offline_packages.sh or .bat first!")
        return False
    
    return True

def check_models():
    """Check if models are available"""
    print("\nChecking models...")
    
    models_dir = Path("models/Stable-diffusion")
    if not models_dir.exists():
        models_dir.mkdir(parents=True, exist_ok=True)
    
    model_files = list(models_dir.glob("*.safetensors")) + list(models_dir.glob("*.ckpt"))
    
    if not model_files:
        print("⚠ No models found in models/Stable-diffusion/")
        print("Please download models from OpenXLab and place them in this directory")
        print("\nRecommended models from OpenXLab:")
        print("1. OpenXL v3.0: https://code.openxlab.org.cn/xiaozhijason/openxl")
        print("2. DreamShaper XL: https://code.openxlab.org.cn/Lykon/DreamShaper")
        print("3. Realistic Vision: https://code.openxlab.org.cn/ninjawick/realistic-vision-5.1")
        return False
    else:
        print(f"✓ Found {len(model_files)} model(s):")
        for model in model_files[:3]:  # Show first 3 models
            print(f"  - {model.name}")
        if len(model_files) > 3:
            print(f"  ... and {len(model_files) - 3} more")
    
    return True

def check_extensions():
    """Check if extensions are available"""
    print("\nChecking extensions...")
    
    extensions_dir = Path("extensions")
    local_extensions_dir = Path("local_extensions")
    
    if local_extensions_dir.exists() and any(local_extensions_dir.iterdir()):
        print("✓ Found local extensions directory")
        # Copy extensions if not already done
        for ext in local_extensions_dir.iterdir():
            if ext.is_dir():
                target = extensions_dir / ext.name
                if not target.exists():
                    print(f"  Copying {ext.name}...")
                    shutil.copytree(ext, target)
    
    installed_extensions = [d.name for d in extensions_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if installed_extensions:
        print(f"✓ Found {len(installed_extensions)} extension(s):")
        for ext in installed_extensions[:3]:
            print(f"  - {ext}")
        if len(installed_extensions) > 3:
            print(f"  ... and {len(installed_extensions) - 3} more")
    else:
        print("⚠ No extensions found")
        print("Extensions are optional but enhance functionality")
    
    return True

def create_config_files():
    """Create necessary config files if they don't exist"""
    print("\nChecking configuration files...")
    
    # Create config.json if it doesn't exist
    if not Path("config.json").exists():
        config = {
            "samples_save": True,
            "samples_format": "png",
            "samples_filename_pattern": "",
            "save_images_add_number": True,
            "grid_save": True,
            "grid_format": "png",
            "grid_extended_filename": False,
            "grid_only_if_multiple": True,
            "grid_prevent_empty_spots": False,
            "n_rows": -1,
            "enable_pnginfo": True,
            "save_txt": False,
            "save_images_before_face_restoration": False,
            "save_images_before_highres_fix": False,
            "save_images_before_color_correction": False,
            "jpeg_quality": 80,
            "export_for_4chan": True,
            "use_original_name_batch": True,
            "use_upscaler_name_as_suffix": False,
            "save_selected_only": True,
            "do_not_add_watermark": False,
            "temp_dir": "",
            "clean_temp_dir_at_start": False
        }
        
        import json
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("✓ Created config.json")
    
    # Create ui-config.json if it doesn't exist
    if not Path("ui-config.json").exists():
        ui_config = {
            "txt2img/Prompt/visible": True,
            "txt2img/Negative prompt/visible": True,
            "txt2img/Sampling steps/visible": True,
            "txt2img/Sampling steps/value": 20,
            "txt2img/CFG Scale/visible": True,
            "txt2img/CFG Scale/value": 7.0,
            "txt2img/Width/visible": True,
            "txt2img/Width/value": 512,
            "txt2img/Height/visible": True,
            "txt2img/Height/value": 512
        }
        
        import json
        with open("ui-config.json", "w") as f:
            json.dump(ui_config, f, indent=2)
        print("✓ Created ui-config.json")

def launch_webui():
    """Launch the web UI"""
    print("\n" + "="*50)
    print("Launching Stable Diffusion WebUI...")
    print("="*50 + "\n")
    
    # Prepare launch arguments
    launch_args = [
        sys.executable,
        "launch.py",
        "--cors-allow-origins=*",
        "--xformers",
        "--enable-insecure-extension-access",
        "--theme", "dark",
        "--gradio-queue",
        "--disable-safe-unpickle",
        "--skip-torch-cuda-test",
        "--no-download-sd-model",
        "--skip-version-check"
    ]
    
    # Add config files if they exist
    if Path("config.json").exists():
        launch_args.extend(["--ui-settings-file", "config.json"])
    if Path("ui-config.json").exists():
        launch_args.extend(["--ui-config-file", "ui-config.json"])
    
    # Launch the process
    try:
        subprocess.run(launch_args)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nError launching WebUI: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure all dependencies are installed")
        print("2. Check that Python version is 3.8 or higher")
        print("3. Verify CUDA is installed if using GPU")
        print("4. Check the log files in the logs directory")

def main():
    print("Stable Diffusion WebUI - Offline Launcher")
    print("="*50)
    
    # Setup environment
    setup_environment()
    
    # Check prerequisites
    if not check_dependencies():
        print("\n❌ Missing dependencies. Please install them first.")
        sys.exit(1)
    
    if not check_models():
        print("\n⚠ No models found, but continuing anyway...")
        print("You can add models later to the models/Stable-diffusion directory")
    
    check_extensions()
    create_config_files()
    
    # Launch WebUI
    launch_webui()

if __name__ == "__main__":
    main()