#!/usr/bin/env python3
"""
Prepare offline installation package for Stable Diffusion WebUI in restricted environments
This script creates local copies of all necessary dependencies
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

def create_directory_structure():
    """Create necessary directories for offline installation"""
    directories = [
        "local_extensions",
        "local_models/stable-diffusion",
        "local_models/controlnet",
        "repositories",
        "dependencies/packages",
        "dependencies/repos"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def create_requirements_file():
    """Create a requirements file that uses only pip-installable packages"""
    requirements_content = """# Core packages that can be installed from PyPI mirrors
torch==2.0.1
torchvision==0.15.2
xformers==0.0.20
transformers==4.30.2
accelerate==0.21.0
basicsr==1.4.2
gfpgan==1.3.8
gradio==3.41.2
numpy==1.23.5
opencv-contrib-python==4.8.0.74
opencv-python==4.8.0.74
requests==2.31.0
tqdm==4.65.0
pillow==9.5.0
scipy==1.9.3
psutil==5.9.5
rich==13.5.2
GitPython==3.1.32
torchsde==0.2.5
safetensors==0.3.1
httpcore==0.15
fastapi==0.94.0
uvicorn==0.23.2
omegaconf==2.2.3
kornia==0.6.9
jsonmerge==1.8.0
resize-right==0.0.2
torchdiffeq==0.2.3
einops==0.4.1
clean-fid==0.1.35
timm==0.9.2
open-clip-torch==2.20.0
clip==0.2.0
"""
    
    with open("requirements_offline.txt", "w") as f:
        f.write(requirements_content)
    print("Created requirements_offline.txt")

def create_pip_install_script():
    """Create a script to install packages from Chinese mirrors"""
    script_content = """#!/bin/bash
# Install packages from Chinese PyPI mirrors

echo "Installing packages from Aliyun mirror..."
pip install -r requirements_offline.txt -i https://mirrors.aliyun.com/pypi/simple/

echo "Installing additional packages that might be missing..."
# Try to install clip and open-clip separately if they fail
pip install clip -i https://mirrors.aliyun.com/pypi/simple/ || echo "Warning: clip installation failed"
pip install open-clip-torch -i https://mirrors.aliyun.com/pypi/simple/ || echo "Warning: open-clip installation failed"

echo "Package installation completed!"
"""
    
    with open("install_offline_packages.sh", "w") as f:
        f.write(script_content)
    
    # Make it executable on Unix-like systems
    if sys.platform != "win32":
        os.chmod("install_offline_packages.sh", 0o755)
    
    # Also create a Windows batch file
    batch_content = """@echo off
REM Install packages from Chinese PyPI mirrors

echo Installing packages from Aliyun mirror...
pip install -r requirements_offline.txt -i https://mirrors.aliyun.com/pypi/simple/

echo Installing additional packages that might be missing...
REM Try to install clip and open-clip separately if they fail
pip install clip -i https://mirrors.aliyun.com/pypi/simple/ || echo Warning: clip installation failed
pip install open-clip-torch -i https://mirrors.aliyun.com/pypi/simple/ || echo Warning: open-clip installation failed

echo Package installation completed!
pause
"""
    
    with open("install_offline_packages.bat", "w") as f:
        f.write(batch_content)
    
    print("Created installation scripts")

def create_extension_list():
    """Create a JSON file with extension information"""
    extensions = {
        "extensions": [
            {
                "name": "sd-dynamic-thresholding",
                "description": "Dynamic Thresholding for improved image quality",
                "url": "https://github.com/mcmonkeyprojects/sd-dynamic-thresholding"
            },
            {
                "name": "sd-webui-controlnet",
                "description": "ControlNet for Stable Diffusion WebUI",
                "url": "https://github.com/Mikubill/sd-webui-controlnet"
            },
            {
                "name": "sd-civitai-browser",
                "description": "Civitai model browser",
                "url": "https://github.com/camenduru/sd-civitai-browser"
            },
            {
                "name": "gif2gif",
                "description": "Generate GIF animations",
                "url": "https://github.com/LonicaMewinsky/gif2gif"
            },
            {
                "name": "sd-webui-infinite-image-browsing",
                "description": "Infinite image browsing",
                "url": "https://github.com/zanllp/sd-webui-infinite-image-browsing"
            },
            {
                "name": "sd-webui-roop-uncensored",
                "description": "Face swap extension",
                "url": "https://github.com/P2Enjoy/sd-webui-roop-uncensored"
            },
            {
                "name": "sd-webui-reactor",
                "description": "Reactor face swap",
                "url": "https://github.com/Gourieff/sd-webui-reactor"
            }
        ]
    }
    
    with open("extensions_list.json", "w") as f:
        json.dump(extensions, f, indent=2)
    print("Created extensions_list.json")

def create_model_list():
    """Create a JSON file with model information and OpenXLab alternatives"""
    models = {
        "stable_diffusion_models": [
            {
                "name": "openxlv3.safetensors",
                "url": "https://code.openxlab.org.cn/api/v1/repos/xiaozhijason/openxl/media/openxlv3.safetensors?ref=main",
                "description": "OpenXL v3.0 - High quality SDXL model"
            },
            {
                "name": "dreamshaper_xl.safetensors",
                "url": "https://code.openxlab.org.cn/api/v1/repos/Lykon/DreamShaper/media/dreamshaper_xl.safetensors?ref=main",
                "description": "DreamShaper XL - Versatile art model"
            },
            {
                "name": "pony_diffusion_v6_xl.safetensors", 
                "url": "https://code.openxlab.org.cn/api/v1/repos/PurpleSmartAI/pony-diffusion-v6/media/pony_diffusion_v6_xl.safetensors?ref=main",
                "description": "Pony Diffusion V6 XL - Anime/cartoon style"
            }
        ],
        "controlnet_models": [
            {
                "name": "control_sdxl_recolor.safetensors",
                "url": "https://code.openxlab.org.cn/api/v1/repos/stabilityai/control-sdxl/media/control_sdxl_recolor.safetensors?ref=main",
                "description": "ControlNet SDXL Recolor"
            }
        ]
    }
    
    with open("models_list.json", "w") as f:
        json.dump(models, f, indent=2)
    print("Created models_list.json")

def create_readme():
    """Create a README file with instructions"""
    readme_content = """# Offline Installation Guide for Stable Diffusion WebUI

## Overview
This package is designed to work in restricted environments where GitHub and Hugging Face are blocked.

## Directory Structure
- `local_extensions/` - Place downloaded extensions here
- `local_models/` - Place downloaded models here
- `repositories/` - Place required git repositories here
- `dependencies/` - Python packages and dependencies

## Installation Steps

### 1. Install Python Dependencies
Run the appropriate script for your OS:
- Linux/Mac: `./install_offline_packages.sh`
- Windows: `install_offline_packages.bat`

### 2. Prepare Extensions
Download extensions manually and place them in `local_extensions/`:
- Each extension should be in its own folder
- Preserve the original folder structure

### 3. Prepare Models
Download models from OpenXLab and place them in `local_models/`:
- Stable Diffusion models go in `local_models/stable-diffusion/`
- ControlNet models go in `local_models/controlnet/`

### 4. Configure Environment Variables
Set these before running:
```bash
export USE_LOCAL_DEPS=true
export CLIP_PACKAGE=clip==1.0
export OPENCLIP_PACKAGE=open_clip_torch
```

### 5. Run the Application
```bash
python app.py
```

## Available OpenXLab Models
See `models_list.json` for a list of models available from OpenXLab.

## Troubleshooting
- If CLIP installation fails, the system will try to use a fallback
- Extensions can be installed manually by copying to the extensions folder
- Models can be downloaded separately and placed in the models folder

## Network Configuration
The system is configured to use Aliyun mirrors for PyPI packages.
"""
    
    with open("OFFLINE_INSTALL_README.md", "w") as f:
        f.write(readme_content)
    print("Created OFFLINE_INSTALL_README.md")

def main():
    print("Preparing offline installation package...")
    
    create_directory_structure()
    create_requirements_file()
    create_pip_install_script()
    create_extension_list()
    create_model_list()
    create_readme()
    
    print("\nOffline installation package prepared!")
    print("Please read OFFLINE_INSTALL_README.md for instructions.")
    print("\nNext steps:")
    print("1. Download extensions and models manually")
    print("2. Place them in the appropriate local directories")
    print("3. Run the installation script")
    print("4. Launch with 'python app.py'")

if __name__ == "__main__":
    main()