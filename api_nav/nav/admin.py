from django.contrib import admin

# Register your models here.

from .models import NestedCategory

admin.site.register(NestedCategory)
