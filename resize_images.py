"""
Resize images to width 300px (height auto) to reduce file size.
Creates output folder with suffix "-w-300"
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image


def resize_images(input_folder: str, target_width: int = 300, quality: int = 85):
    """
    Resize all images in a folder to specified width, maintaining aspect ratio.

    Args:
        input_folder: Path to folder containing images
        target_width: Target width in pixels (default: 300)
        quality: JPEG quality 1-100 (default: 85)
    """
    input_path = Path(input_folder)

    if not input_path.exists():
        print(f"Error: Folder '{input_folder}' not found!")
        return

    # Create output folder with suffix "-w-300"
    output_folder = input_path.parent / f"{input_path.name}-w-{target_width}"
    output_folder.mkdir(exist_ok=True)

    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

    # Get all image files
    image_files = [f for f in input_path.iterdir()
                   if f.is_file() and f.suffix.lower() in image_extensions]

    if not image_files:
        print(f"No images found in '{input_folder}'")
        return

    print(f"Found {len(image_files)} images")
    print(f"Output folder: {output_folder}")
    print("-" * 50)

    processed = 0
    for img_file in image_files:
        try:
            with Image.open(img_file) as img:
                # Get original dimensions
                orig_width, orig_height = img.size

                # Skip if already smaller than target
                if orig_width <= target_width:
                    # Copy as-is but still compress
                    new_width, new_height = orig_width, orig_height
                else:
                    # Calculate new height maintaining aspect ratio
                    ratio = target_width / orig_width
                    new_width = target_width
                    new_height = int(orig_height * ratio)

                # Resize image
                resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Convert RGBA to RGB for JPEG
                if resized.mode in ('RGBA', 'P'):
                    resized = resized.convert('RGB')

                # Save with compression
                output_path = output_folder / f"{img_file.stem}.jpg"
                resized.save(output_path, 'JPEG', quality=quality, optimize=True)

                # Get file sizes for comparison
                orig_size = img_file.stat().st_size / 1024  # KB
                new_size = output_path.stat().st_size / 1024  # KB
                reduction = (1 - new_size / orig_size) * 100

                print(f"✓ {img_file.name}: {orig_width}x{orig_height} -> {new_width}x{new_height} "
                      f"({orig_size:.1f}KB -> {new_size:.1f}KB, -{reduction:.1f}%)")
                processed += 1

        except Exception as e:
            print(f"✗ {img_file.name}: Error - {e}")

    print("-" * 50)
    print(f"Done! Processed {processed}/{len(image_files)} images")
    print(f"Output: {output_folder}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default: current directory
        folder = input("Enter folder path (or press Enter for current directory): ").strip()
        if not folder:
            folder = "."
    else:
        folder = sys.argv[1]

    # Optional: custom width and quality
    width = 300
    quality = 85

    if len(sys.argv) >= 3:
        width = int(sys.argv[2])
    if len(sys.argv) >= 4:
        quality = int(sys.argv[3])

    resize_images(folder, width, quality)
