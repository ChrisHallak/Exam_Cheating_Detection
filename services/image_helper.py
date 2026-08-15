import io
import urllib.request
from typing import Optional
import numpy as np
from PIL import Image
from pathlib import Path
import tempfile
import cv2

# No self key with static function
# Try and catch when dealing with image and external urls
# If everything is static no need for __init__


# from URL -> NUMPY
# URL -> PIL -> NUMPY
# disk -> cv2.imread
# urllib ----> download url image
# urllib.read ----> read it as bytes
# io.BytesIO ----> save it as file
# PIL.read ----> read file as png/jpb image

class ImageHelper:

    @staticmethod
    def download_image_bytes(url) -> Optional[bytes]:
        """Download raw image bytes from a URL."""
        try:
            resp = urllib.request.urlopen(url)
            return resp.read()
        except Exception as e:
            print(f"[Error During Downloading Image ] {e}")
            return None

    @staticmethod
    def convert_bytes_images_to_pil(bytes_data) -> Optional[Image.Image]:
        """Convert raw image bytes into a PIL Image object."""
        try:
            return Image.open(io.BytesIO(bytes_data))
        except Exception as e:
            print(f"[Error During Loading Image ] {e}")
            return None

    @staticmethod
    def convert_url_to_pil(url):
        bytes_image = ImageHelper.download_image_bytes(url)
        pil_image = ImageHelper.convert_bytes_images_to_pil(bytes_image)
        return pil_image

    @staticmethod
    def show_image_pil(pil_image):
        print(pil_image.mode)
        np_image = ImageHelper.convert_pil_to_numpy(pil_image=pil_image)
        bgr_np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        cv2.imshow("BGR Image", bgr_np_image)
        cv2.waitKey(0)

    @staticmethod
    def save_image_to_temp(image, frame_id, format='JPEG'):

        # Clean the frame_id - remove any existing extension
        frame_id = str(frame_id).split('.')[0]

        # Create temp path with correct extension
        ext = '.jpg' if format.upper() == 'JPEG' else f'.{format.lower()}'
        temp_path = Path(tempfile.gettempdir()) / f"temp_{frame_id}{ext}"

        # Convert to RGB if needed (but preserve original if possible)
        rgb_img = ImageHelper.convert_to_rgb(image)

        # Save with explicit format
        rgb_img.save(temp_path, format=format)
        return temp_path

    @staticmethod
    def load_image_from_disk(image_path):
        """Load image from a path and return it as a NumPy array (BGR format)."""
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError("OpenCV could not load the image. Check path or file format.")
            return image
        except Exception as e:
            print(f"[Error During Converting to NumPy ] {e}")
            return None

    @staticmethod
    def display_image_using_cv2(image_title,numpy_image, window_name="Image"):
        """Display a NumPy image using OpenCV."""
        bgr_image = cv2.cvtColor(numpy_image ,cv2.COLOR_RGB2BGR)
        cv2.imshow(image_title, bgr_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def save_numpy_image_using_cv2(image, save_path):
        """Save a NumPy image array to disk."""
        try:
            cv2.imwrite(str(save_path), image)
            return save_path
        except Exception as e:
            print(f"[Error During Saving NumPy Image ] {e}")
            return None

    @staticmethod
    def convert_url_to_numpy_image(url):
        image_bytes = ImageHelper.download_image_bytes(url)
        image_pil = ImageHelper.convert_bytes_images_to_pil(image_bytes)
        numpy_image = np.array(image_pil)
        return numpy_image

    @staticmethod
    def convert_to_rgb(image):
        rgb_img = image
        # Convert to RGB if needed (but preserve original if possible)
        if image.mode != 'RGB':
            if image.mode == 'RGBA':
                # Handle transparency properly
                rgb_img = Image.new('RGB', image.size, (255, 255, 255))
                rgb_img.paste(image, mask=image.split()[3])

            else:
                rgb_img = image.convert('RGB')

        return rgb_img

    @staticmethod
    def convert_bytes_to_pil(bytes_image):
        # return Image.open(io.BytesIO(bytes_image))
        pil_image = Image.open(io.BytesIO(bytes(bytes_image)))
        return pil_image

    @staticmethod
    def convert_pil_to_numpy(pil_image):
        return np.array(pil_image)

    @staticmethod
    def convert_bytes_to_numpy(bytes_image):
        image = ImageHelper.convert_bytes_to_pil(bytes_image)
        numpy_image = ImageHelper.convert_pil_to_numpy(image)
        return numpy_image










