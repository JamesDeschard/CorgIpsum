from django.shortcuts import render
from django.views import View

from.resize import resize


class HomePage(View):

    template = "main/home.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)


class ImageView(View):

    template = "main/image.html"

    def get_dimensions(self, full_path):
        dimensions = full_path.split('/')[1:]
        return int(dimensions[0]), int(dimensions[1])
        
    def get(self, request, *args, **kwargs):
        width, height = self.get_dimensions(request.path)
        context = {
            'width': width,
            'height': height,
            'img': resize(width, height)
        }
        return render(request, self.template, context)