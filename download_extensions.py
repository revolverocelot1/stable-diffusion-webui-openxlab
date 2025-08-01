#!/usr/bin/env python3
"""
Download essential extensions for Stable Diffusion WebUI with China-friendly mirrors
"""
import os
import subprocess
import shutil
import sys

def clone_extension(name, url, dest_path, branch=None):
    """Clone an extension repository"""
    print(f"\nCloning {name}...")
    
    if os.path.exists(dest_path):
        print(f"✓ {name} already exists")
        return True
        
    try:
        cmd = ['git', 'clone', '--depth', '1']
        if branch:
            cmd.extend(['-b', branch])
        cmd.extend([url, dest_path])
        
        subprocess.run(cmd, check=True)
        print(f"✓ Successfully cloned {name}")
        return True
    except Exception as e:
        print(f"✗ Failed to clone {name}: {e}")
        
        # Try alternative mirror for China
        if "github.com" in url:
            mirror_url = url.replace("github.com", "gitee.com")
            print(f"  Trying Gitee mirror: {mirror_url}")
            try:
                cmd[-2] = mirror_url
                subprocess.run(cmd, check=True)
                print(f"✓ Successfully cloned {name} from mirror")
                return True
            except:
                pass
        
        return False

def main():
    # Essential extensions for Stable Diffusion WebUI
    extensions = [
        {
            "name": "sd-webui-controlnet",
            "url": "https://github.com/Mikubill/sd-webui-controlnet.git",
            "description": "ControlNet for Stable Diffusion WebUI"
        },
        {
            "name": "sd-dynamic-prompts",
            "url": "https://github.com/adieyal/sd-dynamic-prompts.git",
            "description": "Dynamic prompts extension"
        },
        {
            "name": "sd-webui-additional-networks",
            "url": "https://github.com/kohya-ss/sd-webui-additional-networks.git",
            "description": "Additional networks (LoRA support)"
        },
        {
            "name": "a1111-sd-webui-locon",
            "url": "https://github.com/KohakuBlueleaf/a1111-sd-webui-locon.git",
            "description": "LoCon support"
        },
        {
            "name": "sd-webui-wildcards",
            "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards.git",
            "description": "Wildcards extension"
        },
        {
            "name": "sd-webui-segment-anything",
            "url": "https://github.com/continue-revolution/sd-webui-segment-anything.git",
            "description": "Segment Anything extension"
        },
        {
            "name": "stable-diffusion-webui-images-browser",
            "url": "https://github.com/AlUlkesh/stable-diffusion-webui-images-browser.git",
            "description": "Image browser"
        },
        {
            "name": "sd-civitai-browser",
            "url": "https://github.com/camenduru/sd-civitai-browser.git",
            "description": "CivitAI browser"
        }
    ]
    
    # Create extensions directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extensions_dir = os.path.join(script_dir, "extensions")
    os.makedirs(extensions_dir, exist_ok=True)
    
    print(f"Installing extensions to: {extensions_dir}")
    
    # Clone each extension
    success_count = 0
    for ext in extensions:
        dest = os.path.join(extensions_dir, ext["name"])
        if clone_extension(ext["name"], ext["url"], dest):
            success_count += 1
    
    print(f"\n✓ Successfully installed {success_count}/{len(extensions)} extensions")
    
    # Create extensions info file
    info_file = os.path.join(extensions_dir, "extensions_info.txt")
    with open(info_file, "w", encoding="utf-8") as f:
        f.write("Installed Extensions:\n\n")
        for ext in extensions:
            f.write(f"{ext['name']}: {ext['description']}\n")
            f.write(f"  URL: {ext['url']}\n\n")
    
    print(f"\nExtensions info saved to: {info_file}")

if __name__ == "__main__":
    main()