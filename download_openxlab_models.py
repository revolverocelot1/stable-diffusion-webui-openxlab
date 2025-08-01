#!/usr/bin/env python3
"""
Download models from OpenXLab with China-friendly mirrors and alternatives
"""
import os
import urllib.request
import urllib.error
import json
import time

def download_file(url, dest_path, retry_count=3):
    """Download a file with retry logic and progress reporting"""
    print(f"Downloading: {url}")
    print(f"Destination: {dest_path}")
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    for attempt in range(retry_count):
        try:
            # Add headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            request = urllib.request.Request(url, headers=headers)
            
            # Download with progress
            with urllib.request.urlopen(request, timeout=30) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                chunk_size = 8192
                
                with open(dest_path, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\rProgress: {progress:.1f}%", end='', flush=True)
                
                print(f"\n✓ Successfully downloaded: {os.path.basename(dest_path)}")
                return True
                
        except urllib.error.HTTPError as e:
            print(f"\n✗ HTTP Error {e.code}: {e.reason}")
            if e.code == 404:
                break  # Don't retry on 404
        except Exception as e:
            print(f"\n✗ Error: {e}")
            
        if attempt < retry_count - 1:
            print(f"  Retrying in 5 seconds... (attempt {attempt + 2}/{retry_count})")
            time.sleep(5)
    
    return False

def main():
    # Model configurations with OpenXLab and alternative sources
    models = {
        "checkpoints": [
            {
                "name": "sd_xl_base_1.0.safetensors",
                "urls": [
                    "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
                    "https://code.openxlab.org.cn/api/v1/models/stabilityai/stable-diffusion-xl-base-1.0/sd_xl_base_1.0.safetensors"
                ],
                "size": "6.94 GB",
                "description": "Stable Diffusion XL base model"
            },
            {
                "name": "sd_xl_refiner_1.0.safetensors",
                "urls": [
                    "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors",
                    "https://code.openxlab.org.cn/api/v1/models/stabilityai/stable-diffusion-xl-refiner-1.0/sd_xl_refiner_1.0.safetensors"
                ],
                "size": "6.08 GB",
                "description": "Stable Diffusion XL refiner"
            },
            {
                "name": "realisticVisionV51.safetensors",
                "urls": [
                    "https://civitai.com/api/download/models/130072",
                    "https://code.openxlab.org.cn/api/v1/models/SG_161222/Realistic_Vision_V5.1_noVAE/realisticVisionV51.safetensors"
                ],
                "size": "5.75 GB",
                "description": "Realistic Vision V5.1"
            }
        ],
        "vae": [
            {
                "name": "sdxl_vae.safetensors",
                "urls": [
                    "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/vae/diffusion_pytorch_model.safetensors",
                    "https://code.openxlab.org.cn/api/v1/models/stabilityai/sdxl-vae/sdxl_vae.safetensors"
                ],
                "size": "334.6 MB",
                "description": "SDXL VAE"
            },
            {
                "name": "vae-ft-mse-840000-ema-pruned.safetensors",
                "urls": [
                    "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors"
                ],
                "size": "334.6 MB",
                "description": "Standard VAE for SD 1.5"
            }
        ],
        "embeddings": [
            {
                "name": "EasyNegativeV2.safetensors",
                "urls": [
                    "https://civitai.com/api/download/models/134583",
                    "https://code.openxlab.org.cn/api/v1/models/gsdf/Counterfeit-V3.0/EasyNegativeV2.safetensors"
                ],
                "size": "312 KB",
                "description": "Easy Negative embedding"
            },
            {
                "name": "bad_prompt_version2.pt",
                "urls": [
                    "https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt"
                ],
                "size": "60.9 KB",
                "description": "Bad prompt negative embedding"
            }
        ],
        "lora": [
            {
                "name": "detail_tweaker_xl.safetensors",
                "urls": [
                    "https://civitai.com/api/download/models/135867"
                ],
                "size": "197.4 MB",
                "description": "Detail tweaker for SDXL"
            }
        ],
        "controlnet": [
            {
                "name": "control_v11p_sd15_openpose.pth",
                "urls": [
                    "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth"
                ],
                "size": "1.45 GB",
                "description": "OpenPose ControlNet"
            }
        ]
    }
    
    # Create model directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    
    # Download configuration
    download_config = {
        "checkpoints": os.path.join(models_dir, "Stable-diffusion"),
        "vae": os.path.join(models_dir, "VAE"),
        "embeddings": os.path.join(script_dir, "embeddings"),
        "lora": os.path.join(models_dir, "Lora"),
        "controlnet": os.path.join(models_dir, "ControlNet")
    }
    
    # Create all directories
    for dir_path in download_config.values():
        os.makedirs(dir_path, exist_ok=True)
    
    # Download models
    total_models = sum(len(models[category]) for category in models)
    downloaded = 0
    failed = []
    
    print(f"Starting download of {total_models} models...\n")
    
    for category, model_list in models.items():
        print(f"\n{'='*60}")
        print(f"Downloading {category.upper()}")
        print(f"{'='*60}")
        
        dest_dir = download_config[category]
        
        for model in model_list:
            print(f"\nModel: {model['name']}")
            print(f"Size: {model['size']}")
            print(f"Description: {model['description']}")
            
            dest_path = os.path.join(dest_dir, model['name'])
            
            # Skip if already exists
            if os.path.exists(dest_path):
                file_size = os.path.getsize(dest_path)
                if file_size > 1000:  # Basic check for non-empty file
                    print(f"✓ Already exists: {model['name']}")
                    downloaded += 1
                    continue
            
            # Try each URL
            success = False
            for url in model['urls']:
                if download_file(url, dest_path):
                    downloaded += 1
                    success = True
                    break
            
            if not success:
                failed.append(f"{category}/{model['name']}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Download Summary")
    print(f"{'='*60}")
    print(f"✓ Successfully downloaded: {downloaded}/{total_models}")
    
    if failed:
        print(f"\n✗ Failed downloads ({len(failed)}):")
        for item in failed:
            print(f"  - {item}")
    
    # Create info file
    info_file = os.path.join(models_dir, "models_info.json")
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump({
            "download_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "models": models,
            "directories": download_config,
            "downloaded": downloaded,
            "total": total_models,
            "failed": failed
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nModels info saved to: {info_file}")

if __name__ == "__main__":
    main()