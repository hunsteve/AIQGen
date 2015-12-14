from django.http import HttpResponse
from selenium import webdriver
from AIQGen.models import Test, Problem, ProblemInTest
from django.core.urlresolvers import reverse
from django.http import HttpRequest

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

def measureHeight(problem, request):
    
    driver = webdriver.PhantomJS() # or add to your PATH
    driver.set_window_size(1920,1080) # optional
    driver.get(request.build_absolute_uri(reverse('problem_printview',args=[problem.id])))
    #driver.save_screenshot('screen.png') # save a screenshot to disk
    

    # rect = driver.execute_script("return document.getElementsByClassName('page')[0].getBoundingClientRect();")
    # print(rect)

    # neptun_cells=[]
    # for i in range(6):
    #     rect = driver.execute_script("return document.getElementById('header').getElementsByClassName('codecell')[%d].getBoundingClientRect();"%i)
    #     neptun_cells.append(rect)
    # print(neptun_cells)

    rectpage = driver.execute_script("return document.getElementsByClassName('page')[0].getBoundingClientRect();")
    rectq = driver.execute_script("return document.getElementsByClassName('question')[0].getBoundingClientRect();")
    driver.quit()

    #h = (100 * (rectq['bottom'] - rectq['top'])) / (rectpage['bottom'] - rectpage['top'])
    h = rectq['bottom'] - rectq['top']
    
    return h
