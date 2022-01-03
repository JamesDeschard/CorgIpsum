from django.db import models

class Counter(models.Model):
    counter = models.IntegerField()

class CorgImage(models.Model):
    title = models.CharField(max_length=128)
    img = models.ImageField(upload_to="media/corgi/images", height_field=None, width_field=None, max_length=100)
    created_on = models.TimeField(auto_now=True)

    def __str__(self):
        return self.title

class CorgImageUrls(models.Model):
    title = models.CharField(max_length=128)
    data = models.JSONField(default=list)

    def __str__(self):
        return self.title