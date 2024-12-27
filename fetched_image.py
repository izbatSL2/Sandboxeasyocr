import requests
import cv2
import numpy as np
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(wait=wait_random_exponential(min=1, max=50), stop=stop_after_attempt(5))
def fetch_image_from_web(image_url):
    """Fetches an image from a web URL with error handling."""
    try:
        print(f"Fetching image from: {image_url}")  # Debug information
        response = requests.get(image_url, timeout=10)  # Adding a timeout for better control
        print(f"Status code: {response.status_code}")  # Debug information
        response.raise_for_status()  # Raise an error for HTTP response codes 4xx/5xx
        image_bytes = response.content  # Get raw byte content of the image
        image_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image from the provided URL.")
        return image
    except requests.RequestException as e:
        print(f"RequestException: {e}")  # Debug information
        raise RuntimeError(f"Network error occurred: {e}") from e
    except Exception as e:
        print(f"Exception: {e}")  # Debug information
        raise RuntimeError(f"An unexpected error occurred: {e}") from e

def fetch_images_from_urls(image_urls):
    """Fetches multiple images from a list of URLs and returns them as a list."""
    images = []
    for url in image_urls:
        try:
            img = fetch_image_from_web(url)
            images.append(img)
        except Exception as e:
            print(f"Failed to fetch image from {url}: {e}")  # Debug information
            images.append(None)  # Append None for failed URLs
    return images
