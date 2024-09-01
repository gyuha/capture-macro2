import cv2
import numpy as np

def jpg_image_optimize(img, file_path, quality=85):
    img_np = np.array(img)

    # Check if the image is grayscale
    is_grayscale = len(img_np.shape) == 2 or (len(img_np.shape) == 3 and img_np.shape[2] == 1)

    if is_grayscale:
        # If grayscale, ensure it's in the correct format
        if len(img_np.shape) == 3:
            img_np = img_np[:,:,0]  # Take only one channel if it's 3D

        # Save as grayscale
        cv2.imwrite(file_path, img_np, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    else:
        # For color images, convert RGB to BGR
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Save as color image
        cv2.imwrite(file_path, img_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

    print(f"Image saved as {'grayscale' if is_grayscale else 'color'} to {file_path}")

    # Optional: You can return the image type for further processing if needed
    return 'grayscale' if is_grayscale else 'color'
