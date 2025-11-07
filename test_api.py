import requests
import os

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY", "")

prompt = "A cinematic futuristic city at sunset, vibrant colors, high detail"

url = "https://api.openai.com/v1/images/generations"

response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
)

if response.status_code == 200:
    image_url = response.json()["data"][0]["url"]
    print(f"Generated Image URL: {image_url}")
else:
    print(f"Failed to generate image. Status Code: {response.status_code}")
    print(f"Response: {response.text}")

