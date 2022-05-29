from django.contrib import admin
from .models import CorgImageUrls, Counter


class CorgImageUrlsAdmin(admin.ModelAdmin):
    fields = ('title', 'data', )

class CorgiCounter(admin.ModelAdmin):
    fields = ('counter', )


admin.site.register(CorgImageUrls, CorgImageUrlsAdmin)
admin.site.register(Counter, CorgiCounter)

    
