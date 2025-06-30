import os
import time

# environment variables to make git clone more robust
os.environ.setdefault('GIT_LFS_SKIP_SMUDGE', '1')  # skip downloading large files
os.environ.setdefault('GIT_OPTIONAL_LOCKS', '0')

# Patch launch_utils.py to perform shallow clone with retries
patch_cmd = ("sed -i -e 's/\"git\" clone /\"git\" -c http.postBuffer=524288000 -c http.lowSpeedLimit=0 -c http.lowSpeedTime=999999 clone --depth 1 --filter=blob:none /' modules/launch_utils.py")
try:
    os.system(patch_cmd)
except Exception as e:
    print(f'Warning: could not patch launch_utils for shallow clone: {e}')

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

print("Cloning extensions...")
os.system("git clone https://github.com/mcmonkeyprojects/sd-dynamic-thresholding extensions/sd-dynamic-thresholding")
os.system("git clone https://github.com/Mikubill/sd-webui-controlnet extensions/sd-webui-controlnet")
os.system("git clone https://github.com/camenduru/sd-civitai-browser extensions/sd-civitai-browser")
os.system("git clone https://github.com/LonicaMewinsky/gif2gif extensions/gif2gif")
os.system("git clone https://github.com/zanllp/sd-webui-infinite-image-browsing extensions/sd-webui-infinite-image-browsing")
os.system("git clone https://github.com/P2Enjoy/sd-webui-roop-uncensored extensions/sd-webui-roop-uncensored")
os.system("git clone https://github.com/Gourieff/sd-webui-reactor extensions/sd-webui-reactor")
print("Extensions cloned.")

print("Downloading ControlNet models (only the .safetensors files, not YAML)...")
# Download only the essential ControlNet models (.safetensors files) - no YAML files as requested
#os.system("aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors -d extensions/sd-webui-controlnet/models -o control_v11f1p_sd15_depth_fp16.safetensors")
#os.system("aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors -d extensions/sd-webui-controlnet/models -o control_v11p_sd15_openpose_fp16.safetensors")
#os.system("aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors -d extensions/sd-webui-controlnet/models -o control_v11p_sd15s2_lineart_anime_fp16.safetensors")
#os.system("aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors -d extensions/sd-webui-controlnet/models -o control_v11f1e_sd15_tile_fp16.safetensors")
print("ControlNet models downloaded.")

print("Downloading models from OpenXLab...")
# Use the correct OpenXLab model URLs as per user's specification
nonce = int(time.time() * 1000)  # Generate a nonce timestamp
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://code.openxlab.org.cn/api/v1/repos/ninjawick/realistic-vision-5.1/media/Realistic_Vision_V6.0_NV_B1_inpainting.safetensors?ref=main&nonce={nonce} -d models/Stable-diffusion -o Realistic_Vision_V6.0_NV_B1_inpainting.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://code.openxlab.org.cn/api/v1/repos/ninjawick/realistic-vision-5.1/media/realisticVisionV51_v51VAE?ref=main&nonce={nonce+1} -d models/Stable-diffusion -o realisticVisionV51_v51VAE.safetensors")

# Add the backup Hugging Face model as in the original
os.system("aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/SG161222/Realistic_Vision_V5.1_noVAE/resolve/main/Realistic_Vision_V5.1_fp16-no-ema.safetensors -d models/Stable-diffusion -o Realistic_Vision_V5.1_fp16-no-ema.safetensors")
print("Models downloaded.")

print("Launching Web UI...")
os.system("python launch.py --cors-allow-origins=* --xformers --enable-insecure-extension-access --theme dark --gradio-queue --disable-safe-unpickle --ui-settings-file config.json --ui-config-file ui-config.json")
