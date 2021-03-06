from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
from .models import Blog, BlogType, BlogTag



# Create your views here.

def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数GET请求，默认第一页
    page_of_blogs = paginator.get_page(page_num)  # get_page 会把字符串转换成数字，page_num是数值,无效数值会跳到默认的页面
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后各两页的范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num,
                            min(current_page_num + 2, paginator.num_pages) + 1))  # paginator.num_pages获取总页数

    # 加入省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #日期归档统计
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month,is_display=True).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_tags'] = BlogTag.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    context['page_range'] = page_range  # 显示页码范围
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.filter(is_deleted=False,is_display=True)
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request,'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type,is_display=True)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_tag(request, blog_tag_pk):
    blog_tag = get_object_or_404(BlogTag, pk=blog_tag_pk)
    blogs_all_list = Blog.objects.filter(blog_tag = blog_tag,is_display=True)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_tag'] = blog_tag
    return render(request, 'blog/blogs_with_tag.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month,is_display=True)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    return render(request,'blog/blogs_with_date.html', context)


def blogs_with_search(request, ketstr):
    blogs_all_list = Blog.objects.filter(content__icontains = ketstr,is_display=True)
    context = get_blog_list_common_data(request, blogs_with_search)
    return render(request, '/blog/blogs_with_search', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog) #阅读计数

    context = dict()
    context['blog'] = blog
    context['content'] = blog.content
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() #上一篇
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first() #下一篇
    response = render(request,'blog/blog_detail.html', context)  #相应
    response.set_cookie(read_cookie_key, 'true')
    return response
