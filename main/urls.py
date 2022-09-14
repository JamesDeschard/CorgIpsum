from django.urls import path

from .views import HomePage, ImageView


def get_name(_class):
    return _class.__name__.lower()

urlpatterns = [
    path('', HomePage.as_view(), name=get_name(HomePage)),
    path('<int:width>/', ImageView.as_view()),
    path('<int:width>/<int:height>/', ImageView.as_view()),
    path('<int:width>/<int:height>/<str:filter>/', ImageView.as_view())
]
