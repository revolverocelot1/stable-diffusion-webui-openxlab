# OpenXLab Local Dependencies Guide

This guide explains how to set up Stable Diffusion WebUI for deployment on OpenXLab or other environments where external GitHub/internet access is restricted.

## Problem

OpenXLab and similar platforms may restrict access to external URLs, causing failures when trying to download dependencies from GitHub:
- CLIP and OpenCLIP packages
- Git repositories (stable-diffusion, k-diffusion, CodeFormer, BLIP)
- Model files from GitHub releases

## Solution

We've created a local dependencies system that bundles all required external resources within the repository.

## Setup Instructions

### 1. Download Dependencies Locally (One-time setup on a machine with internet)

Run the download script to fetch all dependencies:

```bash
python download_dependencies.py
```

This will create a `dependencies/` directory with:
- `packages/` - CLIP and OpenCLIP zip files
- `repos/` - Git repositories needed by the project
- `models/` - Pre-trained model files
- `info.json` - Dependency information

### 2. Include Dependencies in Your Repository

After downloading, the `dependencies/` folder should be committed to your repository:

```bash
git add dependencies/
git commit -m "Add local dependencies for OpenXLab deployment"
git push
```

### 3. Deploy to OpenXLab

The system will automatically use local dependencies when available. The modified files:
- `launch.py` - Checks for and uses local launch_utils
- `modules/launch_utils_local.py` - Handles local dependency installation
- `app.py` - Enables local dependencies mode

## How It Works

1. **Package Installation**: Instead of downloading from GitHub, pip installs from local zip files
2. **Repository Cloning**: Instead of git clone, copies pre-downloaded repositories
3. **Model Downloads**: Instead of downloading from URLs, copies from local files

## Environment Variables

- `USE_LOCAL_DEPS=true` (default) - Enable local dependencies mode
- `USE_LOCAL_DEPS=false` - Disable and use normal download behavior

## Troubleshooting

If you encounter issues:

1. Ensure the `dependencies/` directory exists and contains all files
2. Check that `modules/launch_utils_local.py` exists
3. Verify that `USE_LOCAL_DEPS` is set to `true`

## Adding New Dependencies

To add new dependencies:

1. Update `download_dependencies.py` with the new URLs
2. Run the script to download them
3. Commit the updated `dependencies/` directory

## Note

This approach increases repository size but ensures reliable deployment in restricted environments.