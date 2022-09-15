from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Counter
from .resize import GetAndModifyImage


def update_and_get_counter(add=True):
    current_count = Counter.objects.first()

    if add == False:
        return current_count.counter

    counter = current_count.counter + 1
    current_count.counter = counter
    current_count.save()
    return counter


def home(request):
    return render(request, 'main/home.html', {'counter': update_and_get_counter(False)})


class ImageView(View):
    template = "main/image.html"
    filters = ['sepia', 'grayscale', 'invert', 'contrast', 'blackandwhite', 'blur']
    
    def check_filter(self, filter):
        return True if filter in self.filters else False
    
    def check_dimensions(self, *args):
        return True if all([arg <= 5000 for arg in args]) else False
    
    def get(self, request, *args, **kwargs):
        url_params = [int(p) if p.isnumeric() else p for p in request.path.split('/') if p]

        if len(url_params) == 1:
            width = height = url_params[0]
            if not self.check_dimensions(width, height):
                return HttpResponse('Desired corgi is too large..!')
            
            corgi = GetAndModifyImage(int(width), int(height)).resize()
        
        elif len(url_params) == 2:
            width, height = url_params
            if not self.check_dimensions(width, height):
                return HttpResponse('Desired corgi is too large..!')
            
            corgi = GetAndModifyImage(int(width), int(height)).resize()
        
        elif len(url_params) == 3:
            width, height, filter = url_params
            if not self.check_dimensions(width, height):
                return HttpResponse('Desired corgi is too large..!')
            
            if not self.check_filter(filter):
                return HttpResponse('Requested filter does not exist..!')
            
            corgi = GetAndModifyImage(int(width), int(height), filter).resize()
        
        else:
            return HttpResponse('Url parameters must be width, width/height or width/height/filter..! The filter parameter must NOT BE CLOSED WITH A SLASH..!')
        
        response = HttpResponse(content_type='image/jpg')
        corgi.save(response, "JPEG")
        update_and_get_counter()
        return response



 




     
    