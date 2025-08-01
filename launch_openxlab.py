#!/usr/bin/env python3
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
