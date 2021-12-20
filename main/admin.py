from django.contrib import admin
from .models import CorgImage

class ImageAdmin(admin.ModelAdmin):
    fields = ('title', 'img', )

admin.site.register(CorgImage, ImageAdmin)
    
