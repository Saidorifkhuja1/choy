from django.contrib import admin
from .models import Diller



@admin.register(Diller)
class DillerAdmin(admin.ModelAdmin):
    list_display = ['name']
