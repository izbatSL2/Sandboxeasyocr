from fastapi import APIRouter, HTTPException, FastAPI

from fetched_image import fetch_images_from_urls
from generate import ImageURLRequest
from ocr_service import overlay_ocr_text_from_image

# Buat instance FastAPI
app = FastAPI()

# Initialize FastAPI Router
router = APIRouter(prefix="/ocr_service")

# Tambahkan router ke app
app.include_router(router)

@app.get("/ocr_service")
async def analyze_images(request: ImageURLRequest):
    """
    Endpoint to process multiple images fetched from URLs and extract OCR results for each image.
    """
    try:
        # Fetch images from URLs in batch
        images = fetch_images_from_urls(request.image_urls)

        results = []
        for idx, img in enumerate(images):
            if img is None:
                # If an image failed to fetch, skip processing
                results.append({
                    "image_url": request.image_urls[idx],
                    "error": "Failed to fetch or decode image."
                })
                continue

            # Perform OCR and keyword analysis
            final_texts = overlay_ocr_text_from_image(img)

            # Add result for this image
            results.append({
                "image_url": request.image_urls[idx],
                "extracted_texts": final_texts
            })

        # Return results as a JSON response
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
