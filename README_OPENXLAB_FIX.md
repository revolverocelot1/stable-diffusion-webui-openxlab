# OpenXLab Stable Diffusion WebUI Fix Guide

This guide addresses common issues with deploying Stable Diffusion WebUI on OpenXLab, including missing repositories, model download failures, and China network restrictions.

## Common Issues Fixed

1. **Missing repositories** (CodeFormer, BLIP, etc.)
2. **Failed model downloads** from OpenXLab
3. **Missing extensions directory**
4. **China network restrictions**

## Quick Fix Steps

### 1. Run the Setup Fix Script

```bash
python fix_openxlab_setup.py
```

This script will:
- Create missing repository directories
- Set up extensions folder
- Create launch wrapper for OpenXLab
- Generate model download guide

### 2. Download Dependencies (Optional)

If you have internet access:

```bash
python download_dependencies.py
```

### 3. Download Extensions

```bash
python download_extensions.py
```

This will download essential extensions with China-friendly mirrors.

### 4. Download Models

```bash
python download_openxlab_models.py
```

This script downloads models from multiple sources with fallback options.

### 5. Launch the Application

Use the OpenXLab-specific launcher:

```bash
python launch_openxlab.py
```

Or the original launcher:

```bash
python launch.py
```

## Manual Fixes

### Fix Missing Repositories

The repositories are expected in the `repositories/` folder:

```
repositories/
├── stable-diffusion-stability-ai/
├── generative-models/
├── k-diffusion/
├── CodeFormer/
│   └── requirements.txt
└── BLIP/
```

### Fix Model Downloads

1. **Use China-friendly mirrors:**
   - HuggingFace → https://hf-mirror.com
   - GitHub → https://gitee.com
   - Use OpenXLab's model hub

2. **Recommended models:**
   - SDXL Base 1.0
   - SDXL Refiner
   - Realistic Vision V5.1
   - VAE models

### Network Configuration

Set environment variables for China mirrors:

```bash
export PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
export TORCH_INDEX_URL=https://mirrors.aliyun.com/pytorch-wheels/cu118
```

## Troubleshooting

### Error: "Could not open requirements file"

Run:
```bash
python fix_openxlab_setup.py
```

### Error: "Resource not found" when downloading models

1. Check if the model URL is accessible
2. Try alternative mirrors
3. Download manually and place in correct folder

### Error: "No local extensions directory found"

Extensions folder has been created. You can now:
1. Clone extensions manually
2. Run `python download_extensions.py`

### Launch Issues

Use the OpenXLab wrapper:
```bash
python launch_openxlab.py
```

This sets up proper environment variables for offline mode.

## Model Directory Structure

```
models/
├── Stable-diffusion/   # Checkpoint models (.safetensors, .ckpt)
├── VAE/                # VAE models
├── Lora/               # LoRA models
├── ControlNet/         # ControlNet models
├── ESRGAN/             # Upscaler models
└── Codeformer/         # Face restoration models

embeddings/             # Textual inversion embeddings
```

## Recommended Models from OpenXLab

1. **Base Models:**
   - stabilityai/stable-diffusion-xl-base-1.0
   - SG_161222/Realistic_Vision_V5.1

2. **VAE:**
   - stabilityai/sdxl-vae

3. **Embeddings:**
   - EasyNegativeV2
   - bad_prompt_version2

## Support

For OpenXLab-specific issues:
- Check OpenXLab documentation
- Use local/offline dependencies when possible
- Configure China-friendly mirrors

For general Stable Diffusion WebUI issues:
- Check the main repository issues
- Review error logs in console
- Ensure all dependencies are installed