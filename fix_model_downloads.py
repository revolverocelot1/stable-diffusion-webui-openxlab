#!/usr/bin/env python3
"""
Fix model download URLs for OpenXLab deployment
"""
import os
import json

def create_model_symlinks():
    """Create symlinks for models that might be in different locations"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    
    # Create model directories if they don't exist
    subdirs = ["Stable-diffusion", "VAE", "Lora", "ControlNet", "ESRGAN", "Codeformer", "GFPGAN", "RealESRGAN", "SwinIR", "LDSR", "ScuNET"]
    for subdir in subdirs:
        os.makedirs(os.path.join(models_dir, subdir), exist_ok=True)

def create_model_config():
    """Create a configuration file with working model URLs"""
    config = {
        "model_sources": {
            "huggingface_mirror": "https://hf-mirror.com",
            "modelscope": "https://modelscope.cn/api/v1/models",
            "openxlab": "https://openxlab.org.cn/models",
            "civitai": "https://civitai.com/api/download/models"
        },
        "recommended_models": {
            "stable-diffusion": [
                {
                    "name": "Stable Diffusion XL Base 1.0",
                    "filename": "sd_xl_base_1.0.safetensors",
                    "urls": [
                        "https://hf-mirror.com/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
                        "https://modelscope.cn/api/v1/models/AI-ModelScope/stable-diffusion-xl-base-1.0/repo?FilePath=sd_xl_base_1.0.safetensors"
                    ]
                },
                {
                    "name": "Realistic Vision V5.1",
                    "filename": "realisticVisionV51.safetensors",
                    "urls": [
                        "https://civitai.com/api/download/models/130072"
                    ]
                }
            ],
            "vae": [
                {
                    "name": "SDXL VAE",
                    "filename": "sdxl_vae.safetensors",
                    "urls": [
                        "https://hf-mirror.com/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/vae/diffusion_pytorch_model.safetensors"
                    ]
                },
                {
                    "name": "SD 1.5 VAE",
                    "filename": "vae-ft-mse-840000-ema-pruned.safetensors",
                    "urls": [
                        "https://hf-mirror.com/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors"
                    ]
                }
            ],
            "upscalers": [
                {
                    "name": "RealESRGAN_x4plus",
                    "filename": "RealESRGAN_x4plus.pth",
                    "urls": [
                        "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
                    ]
                }
            ]
        }
    }
    
    # Save configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "model_sources.json")
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created model configuration: {config_path}")
    return config_path

def update_modelloader():
    """Update modelloader.py to handle China mirrors"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    modelloader_path = os.path.join(script_dir, "modules", "modelloader.py")
    
    if not os.path.exists(modelloader_path):
        print(f"✗ modelloader.py not found at {modelloader_path}")
        return
    
    # Read the current file
    with open(modelloader_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if already patched
    if "# China mirror support" in content:
        print("✓ modelloader.py already patched")
        return
    
    # Add mirror support function
    mirror_code = '''
# China mirror support
def try_download_with_mirrors(url: str, dest_path: str, progress: bool = True) -> bool:
    """Try to download from multiple mirrors"""
    mirrors = {
        "huggingface.co": ["hf-mirror.com", "modelscope.cn"],
        "github.com": ["gitee.com", "ghproxy.com/https://github.com"],
    }
    
    urls_to_try = [url]
    
    # Add mirror URLs
    for original, replacements in mirrors.items():
        if original in url:
            for mirror in replacements:
                mirror_url = url.replace(original, mirror)
                urls_to_try.append(mirror_url)
    
    # Try each URL
    for try_url in urls_to_try:
        try:
            print(f"Trying: {try_url}")
            from torch.hub import download_url_to_file
            download_url_to_file(try_url, dest_path, progress=progress)
            return True
        except Exception as e:
            print(f"Failed: {e}")
            continue
    
    return False
'''
    
    # Find the right place to insert
    import_end = content.find("def load_file_from_url(")
    if import_end == -1:
        print("✗ Could not find load_file_from_url function")
        return
    
    # Insert the mirror code
    new_content = content[:import_end] + mirror_code + "\n" + content[import_end:]
    
    # Update load_file_from_url to use mirrors
    new_content = new_content.replace(
        "download_url_to_file(url, cached_file, progress=progress)",
        "if not try_download_with_mirrors(url, cached_file, progress=progress):\n            raise Exception(f'Failed to download from all mirrors: {url}')"
    )
    
    # Write back
    with open(modelloader_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("✓ Patched modelloader.py with mirror support")

def main():
    print("=== Fixing Model Downloads for OpenXLab ===\n")
    
    # Create model directories
    create_model_symlinks()
    
    # Create configuration
    config_path = create_model_config()
    
    # Update modelloader
    update_modelloader()
    
    print("\n=== Fix Complete ===")
    print("\nModel download issues have been addressed:")
    print("1. Created model directories")
    print("2. Generated model_sources.json with working URLs")
    print("3. Patched modelloader.py to support China mirrors")
    print("\nYou can now:")
    print("- Run 'python download_openxlab_models.py' to download models")
    print("- Models will automatically try mirror URLs if primary fails")

if __name__ == "__main__":
    main()