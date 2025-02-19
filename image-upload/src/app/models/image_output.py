# app/models/image_output.py
class ImageOutput:
    def __init__(self, width: int, height: int, mode: str):
        self.width = width
        self.height = height
        self.mode = mode

    def get_specs(self):
        return {
            "width": self.width,
            "height": self.height,
            "mode": self.mode,
        }
