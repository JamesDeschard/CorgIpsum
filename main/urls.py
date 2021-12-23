from django.urls import path, re_path
from .views import HomePage, ImageView, ImageSquareView

def get_name(_class):
    return _class.__name__.lower()

urlpatterns = [
    path('', HomePage.as_view(), name=get_name(HomePage)),
    re_path(
        r'(?P<width>[0-9]+)/(?P<height>[0-9]+)', 
        ImageView.as_view(), 
        name=get_name(ImageView)
    ),
    re_path(
        r'(?P<width>[0-9]+)/', 
        ImageSquareView.as_view(), 
        name=get_name(ImageSquareView)
    ),
]
