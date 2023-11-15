from django.contrib import admin
from .models import Authors, Quotes, Tag

# Register your models here.
admin.site.register(Authors)
admin.site.register(Tag)
admin.site.register(Quotes)
