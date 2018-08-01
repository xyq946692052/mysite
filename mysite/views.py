import datetime
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse
from read_statistics.utils import get_seven_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm

def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today,  read_details__date__gte=date) \
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
    context['dates'] = dates
    return render(request,'home.html', context)


def login(request):
    '''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)

    #重定向到当前页面
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message':'用户名或密码不正确'})
    '''

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))
            else:
                login_form.add_error(None, '用户名或密码不正确')
                context = {}
                context['login_form'] = login_form
                return render(request, 'login.html', context)
        else:
            pass

    else:
        login_form = LoginForm()
        context = {}
        context['login_form'] = login_form
        return render(request, 'login.html',context)

