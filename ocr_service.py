import cv2

import easyocr 

reader = easyocr.Reader(['en','id'], gpu =False)

# Access the debug message
#debug_message = reader.debug_message
#clprint(debug_message)

def overlay_ocr_text_from_image(img):
    """
    Processes an image (numpy array), recognizes text, expands bounding boxes based on fixed keywords,
    re-analyzes expanded areas, and returns the final extracted texts.
    """
    keywords = ["IDPEL", "REF", "KWH", "TOKO"]

    if img is None:
        raise ValueError("No image provided for OCR processing.")

    # Convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect text using EasyOCR
    results = reader.readtext(img)

    final_texts = []  # To store only the final extracted texts

    for (bbox, text, prob) in results:
        if prob >= 0.5:
            # Find keyword similarity
            matched_keyword = next((kw for kw in keywords if kw in text.upper()), None)
            if matched_keyword:
                # Get bounding box coordinates
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = (int(top_left[0]), int(top_left[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

                # Expand bounding box to the right edge of the image
                updated_bottom_right = (img.shape[1] - 1, bottom_right[1])
                updated_top_right = (img.shape[1] - 1, top_right[1])

                # Crop expanded bounding box area
                expanded_bbox_img = img[top_left[1]:bottom_right[1], top_left[0]:updated_bottom_right[0]]

                # Rerun OCR on the updated bounding box
                new_results = reader.readtext(expanded_bbox_img)
                new_texts = [res[1] for res in new_results]
                final_text = ' '.join(new_texts)

                # Append the re-analyzed text to the final results
                final_texts.append(final_text)
    print("DEBUG ANALYSIS : COMPLETED")
    return final_texts
