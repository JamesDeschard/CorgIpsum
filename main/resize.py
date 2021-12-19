from django.templatetags.static import static
from django.conf import settings

from PIL import Image

import os
import glob


def get_latest_file():
    list_of_files = glob.glob(os.path.join(settings.BASE_DIR, 'main', 'static', 'assets', 'redimensioned', '*')) 
    return max(list_of_files, key=os.path.getctime)


def resize(width, height):
    corgi = os.path.join(settings.BASE_DIR, 'main', 'static', 'assets', 'corgi.jpg')
    image = Image.open(corgi)
    new_image = image.resize((width, height))
    new_image.save(os.path.join(settings.BASE_DIR, 'main', 'static', 'assets', 'redimensioned') + "/new.jpg")
    return get_latest_file()

