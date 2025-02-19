from app.models.image_input import ImageInput
from app.models.image_output import ImageOutput
from PIL import Image


class ImageService:
    def process_image(self, image_input: ImageInput) -> ImageOutput:
        # Logic to process the image
        with Image.open(image_input.filename) as img:
            img.verify()  # Verify if it's an image
            file_size = img.size  # (width, height)

        return ImageOutput(
            original_filename=image_input.filename,
            file_size=image_input.file_size,
            dimensions=file_size,
        )
