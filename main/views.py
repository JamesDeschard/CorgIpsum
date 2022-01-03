from django.shortcuts import render
from django.views import View

from .utils import *
from .models import Counter

def update_and_get_counter(add=True):
    counter_object = Counter.objects.first()

    if add == False:
        return counter_object.counter

    counter = counter_object.counter + 1
    counter_object.counter = counter
    counter_object.save()
    return counter
    

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



 




     
    