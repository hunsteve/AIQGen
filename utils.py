from django.http import HttpResponse

def processparams(request):
    urlparams = {}
    if request:
        for k,v in request.GET.dict().iteritems():
            if k=="seed":
                urlparams[k]=int(v)
            if k=="minbranch" or k=="maxbranch":
                ss = v.replace("[","").replace("]","").split(',')
                urlparams[k]=[int(i) for i in ss]
            else:
                urlparams[k]=max(min(int(v),500),-500)
    return urlparams

