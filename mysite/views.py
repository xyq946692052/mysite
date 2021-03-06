import datetime
from django.shortcuts import render, redirect
from django.db.models import Sum,Count
from django.utils import timezone
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_read_data, get_today_hot_data, get_yesterday_hot_data, change_ip_or_visitnum
from blog.models import BlogTag
from blog.models import Blog
from blog.views import blogs_with_tag


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today,  read_details__date__gte=date, is_display=True) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_read_data(blog_content_type)


    #获取七天热门博客缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days,3600)

    context = {}
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs()
    context['blog_tags'] = BlogTag.objects.annotate(blog_count=Count('blog'))
    context['blogs_with_tag'] = blogs_with_tag
    context['dates'] = dates
    context['visit_count'] = change_ip_or_visitnum(request)



    return render(request,'home.html', context)



