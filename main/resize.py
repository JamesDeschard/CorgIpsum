from .models import CorgImage
from .choose_corgi import get_random_img

from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance

import base64

class Filters(object):

    def black_and_white(self, img):
        return img.convert('1')

    def invert(self, img):
        return ImageOps.invert(img)

    def contrast(self, img, scale_value=0.3):
        return ImageEnhance.Contrast(img).enhance(scale_value)

    def grayscale(self, img):
        return ImageOps.grayscale(img)

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

class NewCorgi(Filters):

    def __init__(self, width, height, filter=False):
        self.filter = filter
        self.wanted_dimensions = (width, height)
    
    def resize(self):
        img_io = BytesIO()
        corgi = get_random_img()
        image = Image.open(corgi)

        new_image = ImageOps.fit(image, self.wanted_dimensions, Image.ANTIALIAS)
        new_image = self.apply_filter(new_image) if self.filter else new_image
        
        new_image.save(img_io, format='png')
        img_io.seek(0)
        new_image = base64.b64encode(img_io.getvalue())
        
        return new_image.decode('utf8')

    def apply_filter(self, img):
        if self.filter == 'sepia':
            return self.sepia(img)

        elif self.filter == 'blackandwhite':
            return self.black_and_white(img)

        elif self.filter == 'contrast':
            return self.contrast(img)

        elif self.filter == 'grayscale':
            return self.grayscale(img)

        else:
            return self.invert(img)


