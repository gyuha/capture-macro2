import io

import cv2
import numpy as np
from PIL import Image


def is_effectively_grayscale(image):
    if len(image.shape) == 2:
        return True
    if len(image.shape) == 3:
        if image.shape[2] == 1:
            return True
        # Check if all channels are equal
        return np.all(image[:, :, 0] == image[:, :, 1]) and np.all(
            image[:, :, 1] == image[:, :, 2]
        )
    return False


def jpg_image_optimize(img, file_path, quality=85, progressive=True):
    img_np = np.array(img)

    is_grayscale = is_effectively_grayscale(img_np)

    if is_grayscale:
        # If grayscale or effectively grayscale, convert to 2D array
        if len(img_np.shape) == 3:
            img_np = img_np[:, :, 0]  # Take only one channel

        # Convert to PIL Image
        pil_img = Image.fromarray(img_np)
    else:
        # For color images, convert RGB to BGR
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Convert to PIL Image
        pil_img = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))

    # Use PIL for JPEG optimization
    buffer = io.BytesIO()
    pil_img.save(
        buffer, format="JPEG", quality=quality, optimize=True, progressive=progressive
    )

    # Get the size of the optimized image
    buffer.seek(0, 2)
    size_bytes = buffer.tell()

    # Save the optimized image
    with open(file_path, "wb") as f:
        f.write(buffer.getvalue())

    print(f"Image saved as {'grayscale' if is_grayscale else 'color'} to {file_path}")
    print(f"Optimized image size: {size_bytes / 1024:.2f} KB")

    # Optional: You can return the image type and size for further processing if needed
    return ("grayscale" if is_grayscale else "color"), size_bytes


# Example usage
# img = Image.open("input_image.jpg")
# jpg_image_optimize(img, "output_image.jpg", quality=85, progressive=True)
# img = Image.open("input_image.jpg")
# jpg_image_optimize(img, "output_image.jpg", quality=85, progressive=True)
