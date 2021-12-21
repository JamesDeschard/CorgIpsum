from django.shortcuts import render
from django.views import View

from.resize import NewCorgi

FILTERS = ['sepia', 'grayscale', 'invert', 'contrast', 'blackandwhite']

class HomePage(View):

    template = "main/home.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)


class ImageView(View):

    template = "main/image.html"

    def get_filter(self, request):
        filter = request.path.split('/')[3]
        if filter in FILTERS:
            return filter
        return False 

    def get_dimensions(self, full_path):
        dimensions = full_path.split('/')[1:3]
        return int(dimensions[0]), int(dimensions[1])

        
    def get(self, request, *args, **kwargs):
        filter = False
        width, height = self.get_dimensions(request.path)

        if len(request.path.split('/')[1:]) > 3:
            filter = self.get_filter(request)
            if not filter:
                return render(request, self.template, {'error': 'Sorry, but the requested filter does not exist..!'})
        
        if width > 9999 or height > 9999:
            return render(request, self.template, {'error': 'Sorry, but the requested corgi is too large to be computed..!'})

        if filter:
            corgimage = NewCorgi(width, height, filter).resize()
        else:
            corgimage = NewCorgi(width, height).resize()
        
        return render(request, self.template, {'corgimage': corgimage})




     
    