from django.core.management.base import BaseCommand
from django.conf import settings

from main.models import CorgImageUrls

import urllib.request
import os
import ssl 


ssl._create_default_https_context = ssl._create_unverified_context
LIMIT = 100


def get_image(url, counter):
    return urllib.request.urlretrieve(
        url, 
        os.path.join(settings.BASE_DIR, 'main', 'static', 'assets', 'corgi_{}.jpg'.format(counter))
    )
        

class Command(BaseCommand):

    def handle(self, *args, **options):
        data = CorgImageUrls.objects.first()
        counter = 0
        for url in data.data[0:100]:
            get_image(url, str(counter + 1))
            counter += 1

        self.stdout.write(self.style.SUCCESS('Assets have been saved!'))