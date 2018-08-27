from django.contrib import admin
from .models import ReadNum, ReadDetail, Userip, VisitCount
# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')


@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')


@admin.register(Userip)
class UseripAdmin(admin.ModelAdmin):
    list_display = ('id', 'uip', 'count')


@admin.register(VisitCount)
class VisitCount(admin.ModelAdmin):
    list_display = ('id', 'count')
