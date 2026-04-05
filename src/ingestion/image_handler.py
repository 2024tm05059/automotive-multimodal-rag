import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_image(image_path):
    try:
        img = Image.open(image_path)

        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

        response = model.generate_content(img)

        return response.text if response.text else "No description"

    except Exception as e:
        return f"Image summary failed: {str(e)}"