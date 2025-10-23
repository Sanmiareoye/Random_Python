from rembg import remove
from PIL import Image
import os
from glob import glob


def remove_bg_from_folder(input_folder, output_folder, max_width=1024):
    # Make sure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Supported image extensions
    image_extensions = ["jpg", "jpeg", "png", "webp"]

    # Collect all image paths
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(
            glob(os.path.join(input_folder, f"**/*.{ext}"), recursive=True)
        )

    for img_path in image_paths:
        print(f"Processing: {img_path}")

        # Open image
        img = Image.open(img_path)

        # Resize if needed
        if img.width > max_width:
            new_height = int(img.height * max_width / img.width)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # Remove background
        output = remove(img)
        img_no_bg = output.convert("RGB")

        # Prepare output filename
        filename = os.path.basename(img_path)
        name, ext = os.path.splitext(filename)

        output_filename = f"no_bg_{name}{ext}"
        output_path = os.path.join(output_folder, output_filename)

        # Save processed image
        img_no_bg.save(output_path)
        print(f"Saved: {output_path}")


# Usage
input_folder = "nail_dataset"
output_folder = "nail_dataset_no_bg"
remove_bg_from_folder(input_folder, output_folder)
