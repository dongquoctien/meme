# meme
Image meme, sticker, gifs

## Tools

### resize_images.py

Resize images to reduce file size while maintaining aspect ratio.

**Features:**
- Resize images to specified width (default: 300px), height auto
- Output to new folder with suffix `-w-300`
- Supports: JPG, PNG, GIF, BMP, WebP
- JPEG compression with configurable quality

**Usage:**

```bash
# Basic usage
python resize_images.py <folder_path>

# Custom width and quality
python resize_images.py <folder_path> <width> <quality>

# Example
python resize_images.py ./images 300 85
```

**Requirements:**
```bash
pip install Pillow
```
