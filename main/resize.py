from .models import CorgImage
from .choose_corgi import get_random_img

from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance

import base64
import random
import string

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
        self.width = width
        self.height = height
        self.filter = filter
        self.wanted_dimensions = (self.width, self.height)
    
    def get_largest(self):
        max_value = max([self.width, self.height])
        if max_value == self.height:
            return max_value, True
        else:
            return max_value, False
    
    def get_aspect_ratio(self, img):
        dimensions = img.size
        return dimensions[0] / dimensions[1]
        
    def upload_to_db(self, img):
        title = "corgi" + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
        new_image = CorgImage(
            title= title,
            img = img
            )
        new_image.save()
        return CorgImage.objects.get(title=title)
    
    def apply_crop(self, img, type):
        calc = img.size
        if type:
            resize = (calc[0] - self.width) // 2
            border = (resize, 0, resize, 0)
        else:
            resize = (calc[1] - self.height) // 2
            border = (0, resize, 0, resize)

        img = ImageOps.crop(img, border)

        if img.size != (self.wanted_dimensions):
            return img.resize((self.wanted_dimensions))

        return img

    def resize(self):
        img_io = BytesIO()
        corgi = get_random_img()
        image = Image.open(corgi)
        largest = self.get_largest()

        if largest[1]:
            new_image = image.resize((int(self.width * self.get_aspect_ratio(image)), largest[0]))
            new_image = self.apply_crop(new_image, True)
        else:
            new_image = image.resize((largest[0], int(self.height * self.get_aspect_ratio(image))))
            new_image = self.apply_crop(new_image, False)

        new_image = self.apply_filter(new_image)
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
        elif self.filter == 'invert':
            return self.invert(img)
        else:
            return img

