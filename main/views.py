from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View

from .models import Counter
from .resize import GetAndModifyImage


def update_and_get_counter(add=True):
    counter = Counter.objects.first()

    if add == False:
        return counter.counter

    counter.counter += 1
    counter.save()
    return counter.counter


def home(request):
    return render(request, 'main/home.html', {'counter': update_and_get_counter(False)})


class ImageView(View):
    template = "main/image.html"
    filters = ['sepia', 'grayscale', 'invert', 'contrast', 'blackandwhite', 'blur']
    
    def is_not_null(self, value):
        return all(value)
    
    def check_filter(self, filter):
        return True if filter in self.filters else False
    
    def check_dimensions(self, *args):
        return True if all([arg <= 5000 for arg in args]) else False
    
    def get(self, request, *args, **kwargs):
        url_params = [int(p) if p.isnumeric() else p for p in request.path.split('/') if p]
        
        if len(url_params) == 1:
            # Only one possible scenario: get image of param x param
            width = height = url_params[0]
            if not self.is_not_null((width, height)) or not self.check_dimensions(width, height):
                raise Http404()
            
            corgi = GetAndModifyImage(width, height).resize()
        
        elif len(url_params) == 2:
            # Two possible scenarios: get image of param x param with filter or get image of param x param
            filter = None
            
            if not all(map(lambda x: True if type(x) == int else None, url_params)):
                width = height = url_params[0]
                filter = url_params[1]
                
            else:
                width, height = url_params

            if not self.is_not_null((width, height)) or not self.check_dimensions(width, height):
                raise Http404()
            
            if filter:
                if not self.check_filter(filter):
                    return Http404()
                else:
                    corgi = GetAndModifyImage(width, height, filter).resize()
                
            else:
                corgi = GetAndModifyImage(width, height).resize()
                
        elif len(url_params) == 3:
            # Only one possible scenario: get image of param x param with filter
            width, height, filter = url_params
            if not self.is_not_null((width, height)) or not self.check_dimensions(width, height):
                raise Http404()
            
            if not self.check_filter(filter):
                return Http404()
            
            corgi = GetAndModifyImage(width, height, filter).resize()
        
        else:
            raise Http404()
        
        response = HttpResponse(content_type='image/jpg')
        corgi.save(response, "JPEG")
        update_and_get_counter()
        return response
