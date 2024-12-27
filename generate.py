from pydantic import BaseModel

# Define the request model
class ImageURLRequest(BaseModel):
    image_urls: list[str]