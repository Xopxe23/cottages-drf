from PIL import Image
import os

SUPPORTED_MEDIA_TYPES = [
    "png",
    "jpg"
]

def convertImage(imagePath: str):
    """
        Конвертирует и сжимает формат изображене в .webp

        Arguments:
            imagePath (str): Путь до файла.
        
        Exception (str):
            Если формат файла не поддерживается.

        returns (Image):
            Конвертированное изображение.
    """

    imageExt = os.path.basename(imagePath).split(".")[1]

    if not imageExt in SUPPORTED_MEDIA_TYPES:
        raise Exception("File type not supported")

    return Image.open(imagePath).convert("RGB")
