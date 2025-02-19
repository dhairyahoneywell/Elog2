class ImageInput:
    def __init__(self, filename: str):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def is_png(self):
        return self.filename.lower().endswith(".png")
