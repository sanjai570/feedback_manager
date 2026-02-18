from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'capacity', 'status')
    list_filter = ('type', 'status')
    search_fields = ('name',)
