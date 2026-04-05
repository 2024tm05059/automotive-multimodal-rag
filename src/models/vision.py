import google.generativeai as genai
from PIL import Image
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_image(image_path):
    model = genai.GenerativeModel("gemini-1.5-flash")

    img = Image.open(image_path)

    response = model.generate_content([
        "Give a detailed technical summary of this image for retrieval.",
        img
    ])

    return response.text