from django.contrib import admin
from .models import*

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display=['title','category','user','published_at']
    prepopulated_fields={'slug':('title',)}
    list_filter=['category','user']
    
