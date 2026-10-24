from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

INPUT_IMAGE = DATA_DIR / "source-photo.jpeg"
OUTPUT_IMAGE = DATA_DIR / "source-prepped.png"


def main():
    # Check that the source photo exists
    if not INPUT_IMAGE.exists():
        raise FileNotFoundError(
            f"Photo not found: {INPUT_IMAGE}"
        )

    print("Loading photo...")

    # Open the photo and convert it to RGB
    with Image.open(INPUT_IMAGE) as image:
        image = image.convert("RGB")

    print("Removing background...")

    # Remove the background; the result has transparency
    foreground = remove(image).convert("RGBA")

    # Create a pure white background
    white_background = Image.new(
        "RGBA",
        foreground.size,
        (255, 255, 255, 255),
    )

    # Composite the foreground over white
    prepared = Image.alpha_composite(
        white_background,
        foreground,
    ).convert("RGB")

    # Convert the image to OpenCV format
    image_array = np.array(prepared)
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

    # Improve local contrast using CLAHE
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )
    enhanced = clahe.apply(gray)

    # Save the processed image
    result = Image.fromarray(enhanced)
    result.save(OUTPUT_IMAGE)

    print("\nPhoto preparation complete!")
    print(f"Saved image: {OUTPUT_IMAGE}")
    print(f"Image dimensions: {result.width} x {result.height}")


if __name__ == "__main__":
    main()

