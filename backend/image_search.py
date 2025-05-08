# backend/image_search.py

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "af61590d02c558cbe14c4b39b38d822cfa67027e80903fe8db89e34c667e98b5")

def search_images(query):
    """
    Search images from Google using SerpAPI based on the user's dress prompt.
    Returns a list of image URLs with additional metadata.
    """
    # Enhance the query for better results
    enhanced_query = f"{query} clothing design pattern"

    params = {
        "q": enhanced_query,
        "tbm": "isch",  # 'isch' stands for image search
        "api_key": SERPAPI_API_KEY,
        "ijn": "0",  # Page number
        "num": "8"   # Number of results per page
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()

        images = []
        for img in data.get('images_results', [])[:8]:  # Limit to 8 images
            image_data = {
                "url": img.get('original') or img.get('thumbnail'),
                "title": img.get('title', 'Clothing Design'),
                "source_url": img.get('source', '#')
            }
            images.append(image_data)

        return images

    except Exception as e:
        print(f"Error searching images: {e}")
        # Return some fallback images if the API fails
        return [
            {
                "url": "https://via.placeholder.com/300x400?text=Image+Not+Available",
                "title": "Placeholder Image",
                "source_url": "#"
            }
        ] * 4  # Return 4 placeholder images
