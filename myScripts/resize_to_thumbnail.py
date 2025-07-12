import os
from PIL import Image

# Configuration
IMAGE_DIR = "input_images"
OUTPUT_DIR = "thumbnails"
THUMBNAIL_SIZES = [
    (150, 150),   # Small thumbnail
    (300, 200),   # Medium thumbnail
    (600, 400),   # Large thumbnail
    (1200, 800),  # Hero image
]
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def optimize_image(input_path, output_path, size):
    try:
        with Image.open(input_path) as img:
            img = img.convert('RGB')  # For consistency and optimization
            img.thumbnail(size, Image.LANCZOS)
            img.save(output_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Failed to process {input_path}: {e}")


def create_thumbnails():
    optimized_files = []
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            input_path = os.path.join(IMAGE_DIR, filename)
            base_name, _ = os.path.splitext(filename)

            for width, height in THUMBNAIL_SIZES:
                size_label = f"{width}x{height}"
                output_filename = f"{base_name}_{size_label}.jpg"
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                optimize_image(input_path, output_path, (width, height))
                optimized_files.append((output_filename, width, height))

    return optimized_files


if __name__ == "__main__":
    optimized_list = create_thumbnails()
    print("\nOptimized Thumbnails:")
    for file, width, height in optimized_list:
        print(f"{file}: {width}x{height}")
