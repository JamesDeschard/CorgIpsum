from django.urls import path, re_path

from .views import home, ImageView


urlpatterns = [
    path('', home),
    re_path(r'^(?P<width>\d+)/?$', ImageView.as_view()),
    re_path(r'^(?P<width>\d+)/(?P<filter>\w+)/?$', ImageView.as_view()),
    re_path(r'^(?P<width>\d+)/(?P<height>\d+)/?$', ImageView.as_view()),
    re_path(r'^(?P<width>\d+)/(?P<height>\d+)/(?P<filter>\w+)/?$', ImageView.as_view()),
]
