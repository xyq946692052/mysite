from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog_detail/<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('blog_type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
    path('blog_tag/<int:blog_tag_pk>', views.blogs_with_tag, name='blogs_with_tag'),
    path('date/<int:year>/<int:month>',views.blogs_with_date, name='blogs_with_date'),
    path('blogs_with_search', views.blogs_with_search, name='blogs_with_search'),
]
