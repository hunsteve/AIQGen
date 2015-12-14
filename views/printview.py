 # coding: utf8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from AIQGen.views.astar import astar_question
from AIQGen.views.minimax import minimax_question

from AIQGen.models import Test, Problem
from itertools import permutations


#height: 996, margin: 24 - 24, minimal height: 54. header = 58
def getFirstGoodOrder(questions):
    k=len(questions)
    for indices in permutations(range(k),k):
        q_list=[]
        qs = []
        rh = 996 - 24 - 24 - 20 #page height minus paddings minus extra
        rh = rh - 58 #header
        for i in indices:
            q = questions[i]
            h = q['measuredheight'] + q['freespace']
            if rh > h:
                rh = rh - h
                qs.append(q)
            else:
                if len(q_list) >= 4:
                    break
                q_list.append(qs)
                qs = []
                rh = 996 - 24 - 24 - 20
                rh = rh - h
                qs.append(q)

        if len(q_list) >= 4:
            continue

        q_list.append(qs)
        while len(q_list) < 4:
            q_list.append([])
        i = 1
        for qs in q_list:
            for q in qs:
                q['index'] = i
                i = i + 1
        return q_list
    return None

    


def testPrintView(request, pk):

    '''
    q1 = {'index':1, 'score':5, 'freespace':25, 'body':'dolor sit amet, consectetur adipiscing elit. Pellentesque erat libero, pulvinar ut lectus mattis, ultricies iaculis magna. Morbi ac orci dictum eros sodales condimentum eu sed nunc. Maecenas vitae magna vitae elit sagittis hendrerit sed tincidunt ipsum. Aliquam ultrices, enim at volutpat bibendum, dui elit mattis neque, ut convallis eros odio vel elit. Phasellus porta vulputate efficitur. Sed a ante pretium, dictum metus a, imperdiet ipsum. Quisque egestas ultricies augue non rutrum. Praesent pellentesque nulla at dapibus faucibus. Nullam tristique feugiat vehicula. Cras porta pharetra nulla, a tempor lectus.'}
    q2 = {'index':2, 'score':3, 'freespace':0, 'body':'lorem ipsum'}
    q3 = {'index':3, 'score':2, 'freespace':0, 'body':'lorem ipsum'}
    q4 = {'index':4, 'score':2, 'freespace':0, 'body':'lorem ipsum'}
    (q5, a5) = astar_question(None)
    q5['index']=5

    (q6, a6) = minimax_question(None)
    q6['index']=6
    '''


    test = get_object_or_404(Test, pk=pk)
    pits = test.problemintest_set.all()
    questions=[]
    i=1
    sumscore = 0
    for pit in pits:        
        q = {'index':i, 'score':pit.customscore, 'body':pit.problem.text, 'freespace':pit.customspacing, 'measuredheight':pit.problem.measuredheight}
        i=i+1
        questions.append(q)
        sumscore = sumscore + pit.customscore

    q_list = getFirstGoodOrder(questions)
    if q_list is None:
        return HttpResponse('<h1>cannot render printview, too long test!</h1>')


    header = test.__dict__
    header['sum'] = sumscore
    args = {}
    args['pages'] = []

    hpage4 = {'left':True, 'questions': q_list[3]} 
    hpage1 = {'left':False, 'header':header, 'questions': q_list[0]}   

    hpage2 = {'left':True, 'questions': q_list[1]}    
    hpage3 = {'left':False, 'questions': q_list[2]}   

    args['pages'].append([hpage4, hpage1])
    args['pages'].append([hpage2, hpage3])

    return render(request, 'printview.html', args)
