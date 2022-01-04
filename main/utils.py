from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from PIL import Image

import os

from .resize import NewCorgi
from .models import Counter

INEXISTENT_FILE = {'error': 'Sorry, but the requested file is too large to be computed..!'}
INEXISTENT_FILTER = {'error': 'Sorry, but the requested filter does not exist..!'}
FILE_TOO_LARGE = {'error': 'Sorry, but the requested corgi is too large to be computed..!'}

FILTERS = ['sepia', 'grayscale', 'invert', 'contrast', 'blackandwhite', 'blur']

BASE_FILE = os.path.join(settings.BASE_DIR, 'main', 'generated_image', 'corgimage.png')

def update_and_get_counter(add=True):
    counter_object = Counter.objects.first()

    if add == False:
        return counter_object.counter

    counter = counter_object.counter + 1
    counter_object.counter = counter
    counter_object.save()
    return counter

class BaseCorgImage(View):

    def __init__(self):
        self.length = ''
        self.template = ''
        os.remove(BASE_FILE)

    def check_filter(self, filter):
        if filter in FILTERS:
            return True
        return False
    
    def check_dimensions(self, *args):
        width, height = args
        if int(width) <= 9999 or int(height) <= 9999 :
            return True
        return False
    
    def get_dimensions(self, request):
        return [x for x in request.path.split('/') if x]
    
    def adjust(self):
        return False
    
    def get(self, request, *args, **kwargs):
        update_and_get_counter()
        dimensions = self.get_dimensions(request)
        if len(dimensions) == self.length:
            if self.adjust():
                width, height, filter = [dimensions[0], dimensions[0], dimensions[1]]
            else:
                width, height, filter = dimensions

            if not self.check_dimensions(width, height):
                return render(request, self.template, FILE_TOO_LARGE)

            if not self.check_filter(filter):
                return render(request, self.template, INEXISTENT_FILTER)
            else:
                NewCorgi(int(width), int(height), filter).resize()

        elif len(dimensions) > self.length:
            return JsonResponse(INEXISTENT_FILE, status=403)

        else:
            if self.adjust():
                width, height = [dimensions[0], dimensions[0]]
            else:
                width, height = dimensions 
                
            if not self.check_dimensions(width, height):
                return render(request, self.template, FILE_TOO_LARGE)
            else:
                NewCorgi(int(width), int(height)).resize()
        
        base_file = os.path.join(BASE_FILE)
        corgimage = Image.open(base_file)
        response = HttpResponse(content_type="image/jpeg")
        corgimage.save(response, "JPEG") 
        return response
