from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CorgImage

from io import BytesIO
from PIL import Image

import os
import random
import string

def upload_to_db(img):
    title = "corgi" + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
    new_image = CorgImage(
        title= title,
        img = img
        )
    new_image.save()
    return CorgImage.objects.get(title=title).img.url


def resize(width, height):
    img_io = BytesIO()
    corgi = os.path.join(settings.BASE_DIR, 'main', 'static', 'assets', 'corgi.jpg')
    image = Image.open(corgi)
    new_image = image.resize((width, height))
    new_image.save(img_io, format='JPEG', quality=100)
    thumb_file = InMemoryUploadedFile(img_io, None, 'corgi.jpg', 'image/jpeg', img_io.getbuffer().nbytes, None)
    return upload_to_db(thumb_file)

