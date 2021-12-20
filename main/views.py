from django.shortcuts import render, redirect
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
        if width > 9999 or height > 9999:
            return render(request, self.template, {'error': 'Sorry, but the requested file is too large to be computed..!'})

        return redirect(resize(width, height))
     
    