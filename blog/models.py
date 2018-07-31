from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from read_statistics.models import ReadNumExpendMethod, ReadDetail

# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    class Meta:
        db_table = 'blog_type'

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpendMethod):
    title = models.CharField(max_length=30)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'blog'
        ordering = ['-created_time'] #-表示倒序

    def __str__(self):
        return '<Blog: %s>' % self.title




