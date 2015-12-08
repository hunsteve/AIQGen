 # coding: utf8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from AIQGen.views.astar import astar_question
from AIQGen.views.minimax import minimax_question

from AIQGen.models import Test, Problem


def printview(request, pk):
    test = get_object_or_404(Test, pk=pk)
    args = {}
    args['pages'] = []

    q1 = {'index':1, 'score':5, 'freespace':25, 'text':' dolor sit amet, consectetur adipiscing elit. Pellentesque erat libero, pulvinar ut lectus mattis, ultricies iaculis magna. Morbi ac orci dictum eros sodales condimentum eu sed nunc. Maecenas vitae magna vitae elit sagittis hendrerit sed tincidunt ipsum. Aliquam ultrices, enim at volutpat bibendum, dui elit mattis neque, ut convallis eros odio vel elit. Phasellus porta vulputate efficitur. Sed a ante pretium, dictum metus a, imperdiet ipsum. Quisque egestas ultricies augue non rutrum. Praesent pellentesque nulla at dapibus faucibus. Nullam tristique feugiat vehicula. Cras porta pharetra nulla, a tempor lectus.'}
    q2 = {'index':2, 'score':3, 'freespace':0, 'text':'lorem ipsum'}
    q3 = {'index':3, 'score':2, 'freespace':0, 'text':'lorem ipsum'}
    q4 = {'index':4, 'score':2, 'freespace':0, 'text':'lorem ipsum'}
    (q5, a5) = astar_question(None)
    q5['index']=5

    (q6, a6) = minimax_question(None)
    q6['index']=6
       
    hpage4 = {'left':True, 'questions': [q6]}    
    hpage1 = {'left':False, 'header':test.__dict__, 'questions': [q1, q2, q3, q4, q5]}   

    hpage2 = {'left':True, 'questions': [q6]}    
    hpage3 = {'left':False, 'questions': [q6]}   

    args['pages'].append([hpage4, hpage1])
    args['pages'].append([hpage2, hpage3])

    return render(request, 'printview.html', args)
