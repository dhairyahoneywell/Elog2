import os

from controllers.image_controller import image_bp
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
app.register_blueprint(image_bp, url_prefix="/images")
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Ensure the upload directory exists
UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def hello_world():
    return "Hellooo, World!"


@app.route("/api/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".png"):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Get image properties using Pillow
        with Image.open(file_path) as img:
            width, height = img.size
            format = img.format
            mode = img.mode

        os.remove(file_path)  # Clean up the uploaded file

        return jsonify(
            {"width": width, "height": height, "format": format, "mode": mode}
        ), 200
    else:
        return jsonify({"error": "File is not a PNG"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
