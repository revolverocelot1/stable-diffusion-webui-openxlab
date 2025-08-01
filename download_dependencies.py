"""
Script to download all dependencies locally for OpenXLab deployment
"""
import os
import urllib.request
import zipfile
import shutil
import subprocess
import json

def download_file(url, dest_path):
    """Download a file from URL to destination path"""
    print(f"Downloading {url} to {dest_path}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"✓ Downloaded {os.path.basename(dest_path)}")
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False
    return True

def clone_repo(url, dest_path, commit_hash=None):
    """Clone a git repository to destination path"""
    print(f"Cloning {url} to {dest_path}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Remove existing directory if it exists
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    
    try:
        # Clone the repository
        subprocess.run(['git', 'clone', '--depth', '1', url, dest_path], check=True)
        
        # Checkout specific commit if provided
        if commit_hash:
            os.chdir(dest_path)
            subprocess.run(['git', 'fetch', '--depth', '1', 'origin', commit_hash], check=True)
            subprocess.run(['git', 'checkout', commit_hash], check=True)
            os.chdir('..')
        
        print(f"✓ Cloned {os.path.basename(dest_path)}")
    except Exception as e:
        print(f"✗ Failed to clone {url}: {e}")
        return False
    return True

def main():
    # Define dependencies
    dependencies = {
        "packages": {
            "clip.zip": "https://github.com/openai/CLIP/archive/d50d76daa670286dd6cacf3bcd80b5e4823fc8e1.zip",
            "open_clip.zip": "https://github.com/mlfoundations/open_clip/archive/bb6e834e9c70d9c27d0dc3ecedeebeaeb1ffad6b.zip"
        },
        "repos": {
            "stable-diffusion-stability-ai": {
                "url": "https://github.com/Stability-AI/stablediffusion.git",
                "commit": "cf1d67a6fd5ea1aa600c4df58e5b47da45f6bdbf"  # v2-1-release
            },
            "generative-models": {
                "url": "https://github.com/Stability-AI/generative-models.git",
                "commit": "45c443b316737a4ab6e40413d7794a7f5657c19f"  # 2023.12.02
            },
            "k-diffusion": {
                "url": "https://github.com/crowsonkb/k-diffusion.git",
                "commit": "1e3cd256c40ad78d94f1fa760913cd01d2f01ee5"
            },
            "CodeFormer": {
                "url": "https://github.com/sczhou/CodeFormer.git",
                "commit": "c5b4593074ba6214284d6acd5f1719b6c5d739af"
            },
            "BLIP": {
                "url": "https://github.com/salesforce/BLIP.git",
                "commit": "48211a1594f1321b00f14c9f7a5b4813144b2fb9"
            }
        },
        "models": {
            # RealESRGAN models
            "realesr-general-x4v3.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
            "realesr-general-wdn-x4v3.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth",
            "realesr-animevideov3.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth",
            "RealESRGAN_x4plus.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
            "RealESRGAN_x4plus_anime_6B.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
            "RealESRGAN_x2plus.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
            
            # MiDaS models
            "dpt_large-midas-2f21e586.pt": "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_large-midas-2f21e586.pt",
            "dpt_hybrid-midas-501f0c75.pt": "https://github.com/intel-isl/DPT/releases/download/1_0/dpt_hybrid-midas-501f0c75.pt",
            "midas_v21-f6b98070.pt": "https://github.com/AlexeyAB/MiDaS/releases/download/midas_dpt/midas_v21-f6b98070.pt",
            "midas_v21_small-70d6b9c8.pt": "https://github.com/AlexeyAB/MiDaS/releases/download/midas_dpt/midas_v21_small-70d6b9c8.pt",
            
            # VAE models
            "model.pt": "https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/download/v1.0.0-pre/model.pt",
            "vae-ft-mse-840000-ema-pruned.safetensors": "https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/download/v1.0.0-pre/vae-ft-mse-840000-ema-pruned.safetensors"
        }
    }
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Starting dependency download...\n")
    
    # Download packages
    print("=== Downloading packages ===")
    for filename, url in dependencies["packages"].items():
        dest = os.path.join("dependencies", "packages", filename)
        download_file(url, dest)
    
    # Clone repositories
    print("\n=== Cloning repositories ===")
    for repo_name, repo_info in dependencies["repos"].items():
        dest = os.path.join("dependencies", "repos", repo_name)
        clone_repo(repo_info["url"], dest, repo_info.get("commit"))
    
    # Download models
    print("\n=== Downloading models ===")
    for filename, url in dependencies["models"].items():
        dest = os.path.join("dependencies", "models", filename)
        download_file(url, dest)
    
    # Create dependency info file
    info = {
        "description": "Local dependencies for OpenXLab deployment",
        "packages": dependencies["packages"],
        "repos": {k: v["url"] for k, v in dependencies["repos"].items()},
        "models": dependencies["models"]
    }
    
    with open("dependencies/info.json", "w") as f:
        json.dump(info, f, indent=2)
    
    print("\n✓ All dependencies downloaded successfully!")
    print("Dependencies saved to 'dependencies/' directory")

if __name__ == "__main__":
    main()