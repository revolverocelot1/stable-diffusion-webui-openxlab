import os
os.chdir(f"/home/xlab-app-center")
os.system(f"git clone -b v2.6 https://github.com/camenduru/stable-diffusion-webui /home/xlab-app-center/stable-diffusion-webui")
os.chdir(f"/home/xlab-app-center/stable-diffusion-webui")
os.system(f"git lfs install")
os.system(f"git reset --hard")
os.system(f"sed -i -e '/demo:/r /home/xlab-app-center/header.py' /home/xlab-app-center/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '253,258d' /home/xlab-app-center/stable-diffusion-webui/modules/ui_settings.py")
os.system(f"sed -i -e '186,228d' /home/xlab-app-center/stable-diffusion-webui/modules/ui_settings.py")
os.system(f"sed -i -e '171,178d' /home/xlab-app-center/stable-diffusion-webui/modules/ui_settings.py")
os.system(f"sed -i -e '108,113d' /home/xlab-app-center/stable-diffusion-webui/modules/ui_settings.py")
os.system(f"sed -i -e '225,227d' /home/xlab-app-center/stable-diffusion-webui/modules/ui_loadsave.py")
os.system(f"sed -i -e '214,217d' /home/xlab-app-center/stable-diffusion-webui/modules/ui_loadsave.py")
# extenstions
os.system(f"git clone https://github.com/mcmonkeyprojects/sd-dynamic-thresholding /home/xlab-app-center/stable-diffusion-webui/extensions/sd-dynamic-thresholding")
os.system(f"git clone https://github.com/Mikubill/sd-webui-controlnet /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet")
os.system(f"git clone https://github.com/P2Enjoy/sd-webui-roop-uncensored /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-roop-uncensored")
os.system(f"git clone https://github.com/LonicaMewinsky/gif2gif /home/xlab-app-center/stable-diffusion-webui/extensions/gif2gif")
os.system(f"git clone https://github.com/revolverocelot1/sd-civitai-browser-plus /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-infinite-image-browsing")
os.system(f"git clone https://github.com/BlafKing/sd-civitai-browser-plus /home/xlab-app-center/stable-diffusion-webui/extensions/sd-civitai-browser-plus")
os.system(f"git clone https://github.com/djbielejeski/a-person-mask-generator.git /home/xlab-app-center/stable-diffusion-webui/extensions/a-person-mask-generator")
os.system(f"git clone https://github.com/DominikDoom/a1111-sd-webui-tagcomplete /home/xlab-app-center/stable-diffusion-webui/extensions/a1111-sd-webui-tagcomplete")
os.system(f"git clone https://github.com/Bing-su/adetailer.git /home/xlab-app-center/stable-diffusion-webui/extensions/adetailer")
os.system(f"git clone https://github.com/Iyashinouta/sd-model-downloader /home/xlab-app-center/stable-diffusion-webui/extensions/sd-model-downloader")

os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/SG161222/Realistic_Vision_V5.1_noVAE/resolve/main/Realistic_Vision_V5.1_fp16-no-ema.safetensors -d /home/xlab-app-center/stable-diffusion-webui/models/Stable-diffusion -o Realistic_Vision_V5.1_fp16-no-ema.safetensors")
#model cn
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11e_sd15_ip2p_fp16.safetensors")
# os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11e_sd15_shuffle_fp16.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_canny_fp16.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11f1p_sd15_depth_fp16.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_inpaint_fp16.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_lineart_fp16.safetensors")
# os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_mlsd_fp16.safetensors")
# os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_normalbae_fp16.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_openpose_fp16.safetensors")
# os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_scribble_fp16.safetensors")
# os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_seg_fp16.safetensors")
# os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_softedge_fp16.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus-face_sd15.bin -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o ip-adapter-plus-face_sd15.pth")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.bin -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o ip-adapter-plus_sd15.pth")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15s2_lineart_anime_fp16.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11f1e_sd15_tile_fp16.safetensors")
#yaml cn
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_ip2p_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11e_sd15_ip2p_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_shuffle_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11e_sd15_shuffle_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_canny_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_canny_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1p_sd15_depth_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11f1p_sd15_depth_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_inpaint_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_inpaint_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_lineart_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_lineart_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_mlsd_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_mlsd_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_normalbae_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_normalbae_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_openpose_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_scribble_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_scribble_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_seg_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_seg_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_softedge_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15_softedge_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15s2_lineart_anime_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11p_sd15s2_lineart_anime_fp16.yaml")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --async-dns=false https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1e_sd15_tile_fp16.yaml -d /home/xlab-app-center/stable-diffusion-webui/extensions/sd-webui-controlnet/models -o control_v11f1e_sd15_tile_fp16.yaml")
#
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/ninjawick/mine/resolve/main/gameOfThrones_s01e0103.safetensors -d /home/xlab-app-center/stable-diffusion-webui/models/Stable-diffusion -o gameOfThrones_s01e0103.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://civitai.com/api/download/models/141909 -d /home/xlab-app-center/stable-diffusion-webui/models/Stable-diffusion -o gameOfThrones_s01e0103.safetensors")
os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://download.openxlab.org.cn/models/camenduru/cyber-realistic/weight//cyberrealistic_v32.safetensors -d /home/xlab-app-center/stable-diffusion-webui/models/Stable-diffusion -o cyberrealistic_v32.safetensors")
os.system(f"python launch.py --cors-allow-origins=* --xformers --enable-insecure-extension-access --theme dark --gradio-queue --disable-safe-unpickle --ui-settings-file /home/xlab-app-center/config.json --ui-config-file /home/xlab-app-center/ui-config.json")
