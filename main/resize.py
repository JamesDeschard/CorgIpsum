import os
import random

from django.conf import settings
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


class Filters:
    def black_and_white(self, img):
        return img.convert('1')

    def invert(self, img):
        return ImageOps.invert(img)

    def contrast(self, img, scale_value=0.3):
        return ImageEnhance.Contrast(img).enhance(scale_value)

    def grayscale(self, img):
        return ImageOps.grayscale(img)
    
    def blur(self, img):
        return img.filter(ImageFilter.BLUR)

    def sepia(self, img):
        width, height = img.size
        pixels = img.load()

        for py in range(height):
            for px in range(width):
                r, g, b = img.getpixel((px, py))

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                if tr > 255:
                    tr = 255

                if tg > 255:
                    tg = 255

                if tb > 255:
                    tb = 255

                pixels[px, py] = (tr,tg,tb)

        return img

class GetAndModifyImage(Filters):
    asset_path = os.path.join(settings.BASE_DIR,  'main', 'static', 'assets')
    asset_files_length = len(os.listdir(asset_path))

    def __init__(self, width, height, filter=False):
        self.filter = filter
        self.wanted_dimensions = (width, height)
    
    def resize(self):
        image = f'{self.asset_path}/corgi_{random.randint(0, self.asset_files_length)}.jpg'
        image = Image.open(image)
        new_image = ImageOps.fit(image, self.wanted_dimensions, Image.ANTIALIAS)
        new_image = self.apply_filter(new_image) if self.filter else new_image
        return new_image

    def apply_filter(self, img):
        if self.filter == 'sepia':
            return self.sepia(img)

        elif self.filter == 'blackandwhite':
            return self.black_and_white(img)

        elif self.filter == 'contrast':
            return self.contrast(img)

        elif self.filter == 'grayscale':
            return self.grayscale(img)
            
        elif self.filter == 'blur':
            return self.blur(img)

        else:
            return self.invert(img)


