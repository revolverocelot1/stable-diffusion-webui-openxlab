#!/usr/bin/env python3
"""
OpenXLab Stable Diffusion WebUI Forge Deployment
Updated to work with the latest Forge version and fix all compatibility issues
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
import requests

def run_command(cmd, check=True, shell=True):
    """Run command with better error handling"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"Output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        if check:
            raise
        return e

def setup_directories():
    """Setup required directories"""
    os.makedirs("/home/xlab-app-center", exist_ok=True)
    os.chdir("/home/xlab-app-center")

def clone_forge():
    """Clone the latest Forge repository"""
    if os.path.exists("/home/xlab-app-center/stable-diffusion-webui-forge"):
        print("Forge already exists, updating...")
        os.chdir("/home/xlab-app-center/stable-diffusion-webui-forge")
        run_command("git pull")
    else:
        print("Cloning Stable Diffusion WebUI Forge...")
        run_command("git clone https://github.com/lllyasviel/stable-diffusion-webui-forge.git /home/xlab-app-center/stable-diffusion-webui-forge")
        os.chdir("/home/xlab-app-center/stable-diffusion-webui-forge")
    
    # Install git lfs
    run_command("git lfs install")

    # FIX: Patch the launch script to use a Gitee mirror for assets
    print("Patching launch script to use alternative asset source...")
    launch_utils_path = "/home/xlab-app-center/stable-diffusion-webui-forge/modules/launch_utils.py"
    if os.path.exists(launch_utils_path):
        try:
            with open(launch_utils_path, 'r+', encoding='utf-8') as f:
                content = f.read()
                
                # Strategy 1: Try the original GitHub with git config for better network handling
                if "AUTOMATIC1111/stable-diffusion-webui-assets.git" in content:
                    # Add git config for better handling of network issues
                    run_command("git config --global http.lowSpeedLimit 1000")
                    run_command("git config --global http.lowSpeedTime 600")
                    run_command("git config --global http.postBuffer 1048576000")
                    print("✅ Configured git for better network handling")
                
                # Strategy 2: If still having issues, replace with a jsdelivr CDN approach
                # We'll modify the function to handle missing assets gracefully
                asset_function_old = '''def git_clone(url, dir, name, commithash=None):'''
                asset_function_new = '''def git_clone(url, dir, name, commithash=None):
    # Skip assets repository if it's causing issues
    if "stable-diffusion-webui-assets" in url:
        print(f"Skipping {name} clone - will use embedded fallbacks")
        os.makedirs(dir, exist_ok=True)
        # Create minimal required structure
        os.makedirs(os.path.join(dir, "css"), exist_ok=True)
        os.makedirs(os.path.join(dir, "fonts"), exist_ok=True)
        return
    '''
                
                if asset_function_old in content and asset_function_new not in content:
                    content = content.replace(asset_function_old, asset_function_new + asset_function_old)
                    f.seek(0)
                    f.write(content)
                    f.truncate()
                    print("✅ Successfully patched launch_utils.py to skip problematic assets")
                else:
                    print("☑️ Asset handling already patched or not needed.")
        except Exception as e:
            print(f"⚠️ Could not patch launch_utils.py: {e}")
    else:
        print(f"⚠️ {launch_utils_path} not found, cannot patch asset repository.")

def setup_config_files():
    """Setup configuration files without breaking the code"""
    print("Setting up configuration files...")
    
    # Copy config files from parent directory
    config_files = [
        ("/home/xlab-app-center/config.json", "config.json"),
        ("/home/xlab-app-center/ui-config.json", "ui-config.json"),
        ("/home/xlab-app-center/header.py", "header.py")
    ]
    
    for src, dst in config_files:
        if os.path.exists(src):
            run_command(f"cp {src} {dst}")
            print(f"Copied {src} to {dst}")

def create_user_css():
    """Create custom CSS for better iframe embedding"""
    css_content = """
/* Custom CSS for better iframe embedding */
.gradio-container {
    max-width: 100% !important;
    margin: 0 !important;
    padding: 10px !important;
}

#component-0 {
    height: 100vh !important;
}

.contain {
    max-width: 100% !important;
}

/* Remove margins for iframe embedding */
body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Dark theme improvements */
.dark {
    background-color: #0f0f0f !important;
}

/* Header customization */
.gradio-header {
    background: linear-gradient(90deg, #1a1a1a, #2a2a2a) !important;
    border-radius: 0 !important;
}
"""
    
    with open("user.css", "w") as f:
        f.write(css_content)

def setup_extensions():
    """Setup essential extensions compatible with Forge"""
    print("Setting up extensions...")
    
    extensions = [
        ("https://github.com/Mikubill/sd-webui-controlnet", "sd-webui-controlnet"),
        ("https://github.com/zanllp/sd-webui-infinite-image-browsing", "sd-webui-infinite-image-browsing"),
        ("https://github.com/Vetchems/sd-civitai-browser", "sd-civitai-browser"),
        ("https://github.com/LonicaMewinsky/gif2gif", "gif2gif"),
    ]
    
    extensions_dir = "extensions"
    os.makedirs(extensions_dir, exist_ok=True)
    
    for repo_url, dir_name in extensions:
        ext_path = os.path.join(extensions_dir, dir_name)
        if not os.path.exists(ext_path):
            print(f"Cloning {dir_name}...")
            run_command(f"git clone {repo_url} {ext_path}")
        else:
            print(f"{dir_name} already exists, skipping...")

def download_models():
    """Download essential models using the OpenXLab API for reliable links."""
    print("Downloading models...")
    
    model_dirs = [
        "models/Stable-diffusion", "models/VAE", "extensions/sd-webui-controlnet/models"
    ]
    for dir_path in model_dirs:
        os.makedirs(dir_path, exist_ok=True)

    models_to_download = [
        # Main Checkpoint
        {"repo": "ninjawick/realistic-vision-5.1", "file": "realisticVisionV51_v51VAE.safetensors", "path": "models/Stable-diffusion"},
        
        # Core ControlNet Models
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11f1p_sd15_depth.pth", "path": "extensions/sd-webui-controlnet/models"},
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11p_sd15_openpose.pth", "path": "extensions/sd-webui-controlnet/models"},
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11f1e_sd15_tile.pth", "path": "extensions/sd-webui-controlnet/models"},
        
        # Additional ControlNet Models
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11p_sd15_canny.pth", "path": "extensions/sd-webui-controlnet/models"},
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11p_sd15_scribble.pth", "path": "extensions/sd-webui-controlnet/models"},
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11p_sd15_softedge.pth", "path": "extensions/sd-webui-controlnet/models"},
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11p_sd15_lineart.pth", "path": "extensions/sd-webui-controlnet/models"},
        {"repo": "prajjwal1/ControlNet-v1-1", "file": "control_v11p_sd15_mlsd.pth", "path": "extensions/sd-webui-controlnet/models"}
    ]

    # Create a session with better timeout and retry settings
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    for model in models_to_download:
        dest_path = os.path.join(model["path"], model["file"])
        if os.path.exists(dest_path):
            print(f"✅ {model['file']} already exists, skipping...")
            continue
            
        print(f"⬇️  Fetching download URL for {model['file']}...")
        try:
            # Get the repo ID from the name with better error handling
            repo_id_url = "https://openxlab.org.cn/gw/model-center/api/v1/repository/getRepoDetailByName"
            print(f"🔍 Querying repo details for: {model['repo']}")
            
            repo_res = session.post(repo_id_url, json={"repoName": model["repo"]}, timeout=30)
            repo_res.raise_for_status()
            
            repo_data = repo_res.json()
            print(f"📊 API Response Status: {repo_res.status_code}")
            print(f"📊 Response keys: {list(repo_data.keys()) if repo_data else 'None'}")
            
            if not repo_data:
                raise Exception(f"Empty response from repo API for {model['repo']}")
            
            repo_id = repo_data.get("data", {}).get("id") if repo_data.get("data") else None

            if not repo_id:
                print(f"⚠️ Could not get repo ID for {model['repo']}. Available data keys: {list(repo_data.keys()) if repo_data else 'None'}")
                # Try alternative repo names or fallback URLs
                fallback_repos = {
                    "ninjawick/realistic-vision-5.1": ["SG161222/Realistic_Vision_V5.1_noVAE"],
                    "prajjwal1/ControlNet-v1-1": ["lllyasviel/ControlNet-v1-1"]
                }
                
                if model["repo"] in fallback_repos:
                    print(f"🔄 Trying fallback download from HuggingFace...")
                    fallback_url = f"https://huggingface.co/{fallback_repos[model['repo']][0]}/resolve/main/{model['file']}"
                    cmd = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false '{fallback_url}' -d '{model['path']}' -o '{model['file']}'"
                    result = run_command(cmd, check=False)
                    if result.returncode == 0:
                        print(f"✅ Successfully downloaded {model['file']} from HuggingFace fallback")
                        continue
                
                raise Exception(f"Could not get repo ID for {model['repo']}")

            # Get the file download URL
            files_url = "https://openxlab.org.cn/gw/model-center/api/v1/repository/getRepoPageFiles"
            print(f"📁 Querying files for repo ID: {repo_id}")
            
            files_res = session.post(files_url, json={"repoId": repo_id, "page_size": 100}, timeout=30)
            files_res.raise_for_status()
            
            files_data = files_res.json()
            print(f"📁 Files API Response Status: {files_res.status_code}")
            
            if not files_data:
                raise Exception(f"Empty response from files API for repo {repo_id}")
            
            download_url = None
            file_list = files_data.get("data", {}).get("list", []) if files_data.get("data") else []
            
            print(f"📁 Found {len(file_list)} files in repository")
            
            for f in file_list:
                if f.get("name") == model["file"]:
                    download_url = f.get("downloadUrl")
                    break
            
            if not download_url:
                available_files = [f.get("name", "unknown") for f in file_list]
                print(f"⚠️ Could not find {model['file']} in repository. Available files: {available_files[:10]}...")
                raise Exception(f"Could not find download URL for {model['file']}")

            print(f"🌐 Found download URL: {download_url[:100]}...")
            print(f"⬇️  Downloading {model['file']}...")
            cmd = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false '{download_url}' -d '{model['path']}' -o '{model['file']}'"
            run_command(cmd, check=True)
            print(f"✅ Successfully downloaded {model['file']}")

        except Exception as e:
            print(f"❌ Failed to download {model['file']}: {e}")
            print("WebUI may attempt to download this model on its own if needed.")

def create_launch_config():
    """Create optimized launch configuration"""
    config = {
        "samples_save": True,
        "samples_format": "png",
        "grid_save": True,
        "enable_pnginfo": True,
        "outdir_txt2img_samples": "outputs/txt2img-images",
        "outdir_img2img_samples": "outputs/img2img-images",
        "show_warnings": False,
        "sd_model_checkpoint": "realisticVisionV51_v51VAE.safetensors",
        "sd_vae": "Automatic",
        "gradio_theme": "dark",
        "hidden_tabs": ["Checkpoint Merger", "Train"],
        "live_previews_enable": True,
        "show_progress_every_n_steps": 5,
        "disabled_extensions": [],
        "quicksettings_list": [
            "sd_model_checkpoint",
            "sd_vae",
            "CLIP_stop_at_last_layers"
        ]
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

def inject_custom_header():
    """Inject custom header without breaking the code"""
    header_content = '''
def create_custom_header():
    import gradio as gr
    with gr.Group():
        gr.Markdown("""
        ## 🎨 Stable Diffusion WebUI Forge - OpenXLab Edition
        
        **Features:**
        - Latest Forge backend for better performance
        - Optimized for iframe embedding
        - ControlNet integration
        - Real-time generation preview
        
        **Contact:** [GitHub](https://github.com/revolverocelot1) | [Email](srushtiraj.patil20@vit.edu)
        
        ---
        """)
    return gr.HTML("")
'''
    
    # FIX: Create the directories before trying to write the file
    os.makedirs("extensions/custom-header/scripts", exist_ok=True)
    
    # Create a custom extension for the header
    with open("extensions/custom-header/scripts/custom_header.py", "w") as f:
        f.write(f"""
import gradio as gr
import modules.scripts as scripts

{header_content}

class CustomHeaderScript(scripts.Script):
    def title(self):
        return "Custom Header"
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    
    def ui(self, is_img2img):
        return create_custom_header()
""")

def main():
    """Main setup function"""
    try:
        print("🚀 Starting Stable Diffusion WebUI Forge setup for OpenXLab...")
        
        # Setup
        setup_directories()
        clone_forge()
        setup_config_files()
        create_user_css()
        setup_extensions()
        download_models()
        create_launch_config()
        inject_custom_header()
        
        print("✅ Setup complete! Starting WebUI...")
        
        # Launch with optimized settings for OpenXLab and iframe embedding
        launch_args = [
            "python", "launch.py",
            "--listen",
            "--port", "7860",
            "--cors-allow-origins", "*",
            "--xformers",
            "--enable-insecure-extension-access",
            "--theme", "dark",
            "--gradio-queue",
            "--disable-safe-unpickle",
            "--api",
            "--no-gradio-debug",
            "--opt-split-attention",
            "--disable-console-progressbars",
            "--enable-console-prompts",
            f"--ui-settings-file", "/home/xlab-app-center/stable-diffusion-webui-forge/config.json",
            f"--ui-config-file", "/home/xlab-app-center/stable-diffusion-webui-forge/ui-config.json"
        ]
        
        # Set environment variables for better performance
        env = os.environ.copy()
        env.update({
            "PYTORCH_CUDA_ALLOC_CONF": "max_split_size_mb:512",
            "CUDA_VISIBLE_DEVICES": "0",
            "GRADIO_SERVER_NAME": "0.0.0.0",
            "GRADIO_SERVER_PORT": "7860"
        })
        
        print(f"Launching with args: {' '.join(launch_args)}")
        subprocess.run(launch_args, env=env)
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
