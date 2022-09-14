from django.db import models

# Website is hosted on Heroku, images will therefore be stored in static/assets to avoid hastle with cloud bucket.

class Counter(models.Model):
    counter = models.IntegerField()


class Url(models.Model):
    title = models.CharField(max_length=128)
    data = models.JSONField(default=list)

    def __str__(self):
        return self.title
