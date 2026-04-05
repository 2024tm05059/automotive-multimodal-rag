from .parser import parse_pdf
from .image_handler import summarize_image

def ingest_pdf(file_path):
    text_chunks, image_paths = parse_pdf(file_path)

    image_chunks = []

    for img_path, page in image_paths:
        summary = summarize_image(img_path)

        image_chunks.append({
            "content": summary,
            "page": page,
            "type": "image"
        })

    return text_chunks + image_chunks