from django.contrib import admin
from .models import BlogType, BlogTag, Blog
from . import models

from mdeditor.widgets import MDEditorWidget

# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    ordering = ('id',)


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_name')
    ordering = ('id',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_type', 'blog_tag', 'author','get_read_num', 'title', 'is_display','is_deleted', 'created_time', 'last_updated_time')
    ordering = ('-id',)

    formfield_overrides = {
        models.MDTextField:{'widget':MDEditorWidget(config_name='content_mdeditor')}
    }
