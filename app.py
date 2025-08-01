import os
import time
import shutil

# Enable local dependencies mode for OpenXLab deployment
os.environ['USE_LOCAL_DEPS'] = 'true'

# environment variables to make git clone more robust
os.environ.setdefault('GIT_LFS_SKIP_SMUDGE', '1')  # skip downloading large files
os.environ.setdefault('GIT_OPTIONAL_LOCKS', '0')

# Check if dependencies exist locally
deps_dir = os.path.join(os.path.dirname(__file__), 'dependencies')
if not os.path.exists(deps_dir):
    print("WARNING: Local dependencies not found. Some features may not work in OpenXLab environment.")
    print("Please run download_dependencies.py to download all dependencies locally.")
else:
    print("Found local dependencies directory.")

# If local dependencies don't exist, try using proxy for github
if not os.path.exists(deps_dir):
    # Use a proxy for github to avoid connection timeouts
    os.environ['CLIP_PACKAGE'] = "https://ghproxy.com/https://github.com/openai/CLIP/archive/d50d76daa670286dd6cacf3bcd80b5e4823fc8e1.zip"
    os.environ['OPENCLIP_PACKAGE'] = "https://ghproxy.com/https://github.com/mlfoundations/open_clip/archive/bb6e834e9c70d9c27d0dc3ecedeebeaeb1ffad6b.zip"

# Create requirements.txt with the exact dependencies from the reference
with open('requirements.txt', 'w') as f:
    f.write("""--extra-index-url https://download.pytorch.org/whl/cu118
torch==2.0.1+cu118
torchvision==0.15.2+cu118
torchaudio==2.0.2+cu118
torchtext==0.15.2
torchdata==0.6.1
xformers==0.0.20
triton==2.0.0
""")

print("Installing dependencies...")
os.system("pip install -r requirements.txt")
print("Dependencies installed.")

# Helper function to inject header content into modules/ui.py
def inject_header():
    """Inject header content into modules/ui.py at the demo: marker"""
    ui_file = 'modules/ui.py'
    header_file = 'header.py'

    if not os.path.exists(ui_file) or not os.path.exists(header_file):
        print(f"Warning: {ui_file} or {header_file} not found, skipping header injection")
        return

    with open(header_file, 'r') as f:
        header_content = f.read()

    with open(ui_file, 'r') as f:
        ui_content = f.read()

    # Find the demo: marker and inject header content after it
    demo_marker = 'demo:'
    if demo_marker in ui_content:
        lines = ui_content.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if demo_marker in line:
                # Add the header content after the demo: line
                new_lines.extend(header_content.split('\n'))

        with open(ui_file, 'w') as f:
            f.write('\n'.join(new_lines))
        print("Header injection completed.")
    else:
        print("Warning: demo: marker not found in ui.py, skipping header injection")

def remove_lines(filename, line_numbers):
    """Remove lines from a file."""
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found, skipping line removal")
        return

    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        for i, line in enumerate(lines):
            if i + 1 not in line_numbers:
                f.write(line)

print("Applying UI modifications...")

# Inject header content into modules/ui.py
inject_header()

# Modify modules/ui_settings.py - remove the specified line ranges
ui_settings_deletions = list(range(253, 259)) + list(range(186, 229)) + list(range(171, 179)) + list(range(108, 114))
remove_lines('modules/ui_settings.py', ui_settings_deletions)

# Modify modules/ui_loadsave.py - remove the specified line ranges
ui_loadsave_deletions = list(range(225, 228)) + list(range(214, 218))
remove_lines('modules/ui_loadsave.py', ui_loadsave_deletions)

print("UI modifications applied.")

print("Setting up extensions...")

# Create extensions directory if it doesn't exist
if not os.path.exists("extensions"):
    os.makedirs("extensions")

# List of required extensions (can be pre-downloaded and placed in a local folder)
extensions_list = [
    ("sd-dynamic-thresholding", "Dynamic Thresholding extension"),
    ("sd-webui-controlnet", "ControlNet extension"),
    ("sd-civitai-browser", "Civitai Browser extension"),
    ("gif2gif", "GIF2GIF extension"),
    ("sd-webui-infinite-image-browsing", "Infinite Image Browsing extension"),
    ("sd-webui-roop-uncensored", "Roop Uncensored extension"),
    ("sd-webui-reactor", "Reactor extension")
]

# Try to use local pre-downloaded extensions
local_ext_path = "local_extensions"
if os.path.exists(local_ext_path):
    print(f"Found local extensions directory at {local_ext_path}")
    for ext_name, ext_desc in extensions_list:
        src_path = os.path.join(local_ext_path, ext_name)
        dst_path = os.path.join("extensions", ext_name)
        if os.path.exists(src_path) and not os.path.exists(dst_path):
            print(f"Copying {ext_desc} from local directory...")
            shutil.copytree(src_path, dst_path)
        elif os.path.exists(dst_path):
            print(f"{ext_desc} already exists, skipping...")
        else:
            print(f"Warning: {ext_desc} not found in local directory")
else:
    print("Warning: No local extensions directory found. Extensions need to be manually installed.")
    print("Please download the following extensions and place them in the 'extensions' folder:")
    for ext_name, ext_desc in extensions_list:
        print(f"  - {ext_name}: {ext_desc}")

print("Extensions setup completed.")

print("Setting up models...")

# Create necessary directories
os.makedirs("models/Stable-diffusion", exist_ok=True)
os.makedirs("extensions/sd-webui-controlnet/models", exist_ok=True)

# Check for local models first
local_models_path = "local_models"
if os.path.exists(local_models_path):
    print(f"Found local models directory at {local_models_path}")
    # Copy Stable Diffusion models
    sd_models = ["Realistic_Vision_V6.0_NV_B1_inpainting.safetensors", 
                 "realisticVisionV51_v51VAE.safetensors",
                 "Realistic_Vision_V5.1_fp16-no-ema.safetensors"]
    
    for model in sd_models:
        src = os.path.join(local_models_path, "stable-diffusion", model)
        dst = os.path.join("models/Stable-diffusion", model)
        if os.path.exists(src) and not os.path.exists(dst):
            print(f"Copying {model}...")
            shutil.copy2(src, dst)
    
    # Copy ControlNet models
    controlnet_models = ["control_v11f1p_sd15_depth_fp16.safetensors",
                        "control_v11p_sd15_openpose_fp16.safetensors",
                        "control_v11p_sd15s2_lineart_anime_fp16.safetensors",
                        "control_v11f1e_sd15_tile_fp16.safetensors"]
    
    for model in controlnet_models:
        src = os.path.join(local_models_path, "controlnet", model)
        dst = os.path.join("extensions/sd-webui-controlnet/models", model)
        if os.path.exists(src) and not os.path.exists(dst):
            print(f"Copying ControlNet model {model}...")
            shutil.copy2(src, dst)
else:
    print("Downloading models from OpenXLab...")
    # Use the correct OpenXLab model URLs
    nonce = int(time.time() * 1000)  # Generate a nonce timestamp
    
    # Try OpenXLab first
    print("Attempting to download from OpenXLab...")
    os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://code.openxlab.org.cn/api/v1/repos/ninjawick/realistic-vision-5.1/media/Realistic_Vision_V6.0_NV_B1_inpainting.safetensors?ref=main&nonce={nonce} -d models/Stable-diffusion -o Realistic_Vision_V6.0_NV_B1_inpainting.safetensors")
    os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://code.openxlab.org.cn/api/v1/repos/ninjawick/realistic-vision-5.1/media/realisticVisionV51_v51VAE?ref=main&nonce={nonce+1} -d models/Stable-diffusion -o realisticVisionV51_v51VAE.safetensors")
    
    # Try alternative OpenXLab model
    print("Downloading OpenXL v3.0 model from OpenXLab...")
    os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://code.openxlab.org.cn/api/v1/repos/xiaozhijason/openxl/media/openxlv3.safetensors?ref=main&nonce={nonce+2} -d models/Stable-diffusion -o openxlv3.safetensors")

print("Models setup completed.")

print("Launching Web UI...")
os.system("python launch.py --cors-allow-origins=* --xformers --enable-insecure-extension-access --theme dark --gradio-queue --disable-safe-unpickle --ui-settings-file config.json --ui-config-file ui-config.json")
 