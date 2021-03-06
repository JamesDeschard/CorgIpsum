from django.shortcuts import render
from django.views import View

from .utils import BaseCorgImage, update_and_get_counter


class HomePage(View):

    template = "main/home.html"

    def get(self, request, *args, **kwargs):
        context = {
            'counter': update_and_get_counter(add=False)
        }
        return render(request, self.template, context)


class ImageView(BaseCorgImage):

    def __init__(self):
        self.length = 3
        self.template = "main/image.html"


class ImageSquareView(BaseCorgImage):

    def __init__(self):
        self.length = 2
        self.template = "main/image.html"
    
    def adjust(self):
        return True



 




     
    