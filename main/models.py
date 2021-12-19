from django.db import models


class CorgImage(models.Model):
    title = models.CharField(max_length=128)
    img = models.ImageField(upload_to="media/corgi/images", height_field=None, width_field=None, max_length=100)
    created_on = models.TimeField(auto_now=True)
