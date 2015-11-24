 # coding: utf8
from django.shortcuts import render
from django.http import HttpResponse

from AIQGen.views.astar import astar_question
from AIQGen.views.minimax import minimax_question

def printview(request):
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

       
    hpage4A = {'left':True, 'questions': [q6]}    
    hpage1A = {'left':False, 'header':{'title':'MI pótZH', 'group':'A', 'date':'2015. 11. 13.'}, 'questions': [q1, q2, q3, q4, q5]}   

    hpage2A = {'left':True}    
    hpage3A = {'left':False}   

    #---------------------------------------

    hpage4B = {'left':True}    
    hpage1B = {'left':False, 'header':{'title':'MI pótZH', 'group':'B', 'date':'2015. 11. 13.'}}   

    hpage2B = {'left':True}    
    hpage3B = {'left':False}   

    args['pages'].append([hpage4A, hpage1A])
    args['pages'].append([hpage2A, hpage3A])
    args['pages'].append([hpage4B, hpage1B])
    args['pages'].append([hpage2B, hpage3B])

    return render(request, 'printview.html', args)
