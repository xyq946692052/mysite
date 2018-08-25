import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail, VisitCount, Userip

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        #总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        #当天阅读数+1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()

    return key


def get_seven_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects \
                                 .filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects \
                             .filter(content_type=content_type, date=today) \
                             .order_by('-read_num')
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects \
                             .filter(content_type=content_type, date=yesterday) \
                             .order_by('-read_num')
    return read_details[:7]



def change_ip_or_visitnum(request):
    count_obj = VisitCount.objects.all()
    if count_obj:
        count_nums = count_obj[0]
        count_nums.count += 1
    else:
        count_nums = VisitCount(count = 0)
    count_nums.save()

    #记录访问ip和每个ip的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META:   #获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(',')[0]   #此处为真实IP
    else:
        client_ip = request.META.get('REMOTE_ADDR', '')  #此处为获得代理IP

    ip_exist = Userip.objects.filter(ip=str(client_ip))
    if ip_exist:
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = Userip()
        uobj.ip = client_ip
        uobj.count = 1
    uobj.save()
    return VisitCount.objects.all()[0].count


