from django.contrib import admin
from .models import BlogType, Blog

# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    ordering = ('id',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_type', 'author', 'title', 'is_deleted', 'created_time', 'last_updated_time')
    ordering = ('-id',)
