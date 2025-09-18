
"""
import requests
import os
from urllib.parse import urlparse

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get URL from user
    url = input("Please enter the image URL: ")
    
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)
        
        # Fetch the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename:
            filename = "downloaded_image.jpg"
            
        # Save the image
        filepath = os.path.join("Fetched_Images", filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        print("\nConnection strengthened. Community enriched.")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

if __name__ == "__main__":
    main()
"""


# Challenge Questions

# Modify the program to handle multiple URLs at once.

# Implement precautions that you should  take when downloading files from unknown sources.

# Implement a feature that prevents downloading duplicate images.

# Implement what HTTP headers might be important to check before saving the response content.

import os
import requests
import hashlib

# ----------------- Configuration -----------------
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB max
FOLDER_NAME = "Fetched_Images"

# ----------------- Setup -----------------
# Create folder if it doesn't exist
os.makedirs(FOLDER_NAME, exist_ok=True)

# Initialize set for duplicate detection
saved_hashes = set()

# ----------------- Input -----------------
urls_input = input("Enter image URLs separated by commas: ")
urls = [url.strip() for url in urls_input.split(",")]

# ----------------- Processing -----------------
for url in urls:
    try:
        # Fetch headers first to check content type and size
        response = requests.get(url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"Skipped {url}: Not an image ({content_type})")
            continue

        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_FILE_SIZE:
            print(f"Skipped {url}: File too large ({int(content_length)/1024:.2f} KB)")
            continue

        # Read full content after header checks
        image_data = response.content

        # ----------------- Duplicate Check -----------------
        image_hash = hashlib.md5(image_data).hexdigest()
        if image_hash in saved_hashes:
            print(f"Skipped {url}: Duplicate image detected")
            continue

        # ----------------- Filename -----------------
        filename = os.path.basename(url) or f"image_{image_hash[:8]}.jpg"
        save_path = os.path.join(FOLDER_NAME, filename)

        # Avoid filename conflicts by appending hash
        if os.path.exists(save_path):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{image_hash[:8]}{ext}"
            save_path = os.path.join(FOLDER_NAME, filename)

        # ----------------- Save Image -----------------
        with open(save_path, "wb") as f:
            f.write(image_data)

        # Add hash to set
        saved_hashes.add(image_hash)
        print(f"Saved {filename} from {url}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
