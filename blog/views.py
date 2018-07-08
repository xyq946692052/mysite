from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType

# Create your views here.

def blog_list(request):
    blogs_all_list = Blog.objects.filter(is_deleted=False)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数GET请求，默认第一页
    page_of_blogs = paginator.get_page(page_num)  #get_page 会把字符串转换成数字，page_num是数值,无效数值会跳到默认的页面
    current_page_num = page_of_blogs.number #获取当前页码
    #获取当前页码前后各两页的范围
    page_range = list(range(max(current_page_num-2,1), current_page_num))+\
                 list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1)) #paginator.num_pages获取总页数

    # 加入省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append("...")

    #加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range  #显示页码范围
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() #上一篇
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first() #下一篇
    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10个进行分页
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

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['blog_type'] = blog_type
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    return render_to_response('blog/blogs_with_type.html', context)
