# Recommended Models for OpenXLab Deployment

## Base Models (Place in models/Stable-diffusion/)

1. **Stable Diffusion XL Base**
   - Download: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
   - Mirror: Use Modelscope or OpenXLab mirror if available

2. **Realistic Vision V5.1**
   - Popular photorealistic model
   - Check CivitAI or local mirrors

## VAE Models (Place in models/VAE/)

1. **SDXL VAE**
   - Essential for SDXL models
   - Download from HuggingFace or mirrors

2. **SD 1.5 VAE**
   - vae-ft-mse-840000-ema-pruned.safetensors

## Extensions to Install

Run: python download_extensions.py

## Models Download

Run: python download_openxlab_models.py

## Troubleshooting

1. If downloads fail, try using a VPN or proxy
2. Use Gitee mirrors for GitHub repositories
3. Check OpenXLab model hub for China-friendly links
