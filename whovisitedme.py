from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode
from datetime import datetime

def whovisitedme(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    with open("visitors.log", "a") as myfile:
        myfile.write("%s             %s             https://who.is/whois-ip/ip-address/%s\n" % (str(datetime.now()), str(ip), str(ip)))
    return HttpResponse("")

def listlog(request):
    with open('visitors.log', 'r') as myfile:
        data=myfile.read().replace("\n","<br/>")
    return HttpResponse(data)