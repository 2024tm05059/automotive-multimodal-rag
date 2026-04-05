import fitz

def parse_pdf(file_path):
    doc = fitz.open(file_path)

    text_chunks = []
    image_paths = []

    for page_num, page in enumerate(doc):
        text = page.get_text()

        if text.strip():
            text_chunks.append({
                "content": text,
                "page": page_num,
                "type": "text"
            })

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)

            img_bytes = base_image["image"]
            img_path = f"temp_img_{page_num}_{img_index}.png"

            with open(img_path, "wb") as f:
                f.write(img_bytes)

            image_paths.append((img_path, page_num))

    return text_chunks, image_paths