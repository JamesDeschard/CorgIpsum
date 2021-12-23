from django.views import View
from django.http import JsonResponse
from django.shortcuts import render

from .resize import NewCorgi

INEXISTENT_FILE = {'error': 'Sorry, but the requested file is too large to be computed..!'}
INEXISTENT_FILTER = {'error': 'Sorry, but the requested filter does not exist..!'}
FILE_TOO_LARGE = {'error': 'Sorry, but the requested corgi is too large to be computed..!'}

FILTERS = ['sepia', 'grayscale', 'invert', 'contrast', 'blackandwhite']

class BaseCorgImage(View):

    def __init__(self):
        self.length = ''
        self.template = ''

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
                corgimage = NewCorgi(int(width), int(height), filter).resize()
                return render(request, self.template, {'corgimage': corgimage})

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
                corgimage = NewCorgi(int(width), int(height)).resize()
                return render(request, self.template, {'corgimage': corgimage})