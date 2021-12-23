from django.contrib import admin
from .models import CorgImageUrls


class CorgImageUrlsAdmin(admin.ModelAdmin):
    fields = ('title', 'data', )


admin.site.register(CorgImageUrls, CorgImageUrlsAdmin)

    
