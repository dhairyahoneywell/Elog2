import os

from flask import Blueprint, jsonify, request
from PIL import Image

image_bp = Blueprint("image", __name__)

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@image_bp.route("/upload", methods=["POST"])
def upload():
    from app.models.image_input import ImageInput  # Import ImageInput
    from app.models.image_output import ImageOutput  # Import ImageOutput
    from app.services.image_service import ImageService  # Import ImageService

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if uploaded_file and uploaded_file.filename.endswith(".png"):
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        # Get image properties using Pillow
        with Image.open(file_path) as img:
            width, height = img.size
            mode = img.mode

        os.remove(file_path)  # Clean up the uploaded file

        # Create an ImageInput instance
        image_input = ImageInput(filename=uploaded_file.filename)

        # Process the image using the image_service
        image_service = ImageService()

        # Process the image and get the output
        result = image_service.process_image(image_input)

        # Create an ImageOutput instance with the properties obtained
        image_output = ImageOutput(width=width, height=height, mode=mode)

        return jsonify(
            {
                "input": image_input.filename,
                "output": image_output.get_specs(),
                "result": result,
            }
        ), 200
    else:
        return jsonify({"error": "File is not a PNG."}), 400
