import os
import ssl
import urllib.request
from urllib.error import HTTPError

from django.conf import settings
from django.core.management.base import BaseCommand
from main.models import ScrapedImageUrl

ssl._create_default_https_context = ssl._create_unverified_context

LIMIT = 500
ASSETS_PATH = os.path.join(settings.BASE_DIR,  'main', 'static', 'assets')


def get_image(url, counter):
    if not os.path.isdir(ASSETS_PATH):
        os.mkdir(ASSETS_PATH)
   
    return urllib.request.urlretrieve(url, f'{ASSETS_PATH}/corgi_{counter}.jpg')
        

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = ScrapedImageUrl.objects.first()
        counter = 0
        for url in data.data[0:LIMIT]:
            try:
                get_image(url, counter)
                counter += 1
            except HTTPError:
                counter += 1

        self.stdout.write(self.style.SUCCESS('Assets have been saved!'))
