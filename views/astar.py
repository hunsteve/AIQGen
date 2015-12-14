# coding: utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode
import pygraphviz as pgv
import random
import math
from AIQGen.utils import processparams
    
def adjacencyToEdgeDict(A):
    graph = {}
    for n in range(len(A)):
        graph[n] = {}
        for n2 in range(len(A)):            
            if not math.isnan(A[n][n2]):
                graph[n][n2] = A[n][n2]
    return graph

def astargraph(nodeCnt = 8, minedge = 2, maxedge = 3, spread = 3, mincost = 1, maxcost = 10, seed = None):    
    
    random.seed(seed)

    A=[[float('nan')]*nodeCnt for i in range(nodeCnt)] #adjacency matrix
    for n in range(nodeCnt):
        for k in range(random.randint(1,maxedge)):
            while(True):
                n2 = random.randint(max(n-spread,0),min(n+spread,nodeCnt-1))
                if (n2 != n):
                    break
            A[n][n2] = A[n2][n] = random.randint(mincost,maxcost)    


    graph = adjacencyToEdgeDict(A)

    G=pgv.AGraph(graph)
    G.node_attr['shape']='circle'
    G.node_attr['fixedsize']='true'
    G.node_attr['width']=0.33
    G.node_attr['height']=0.33
    G.node_attr['fontsize']=10
    G.edge_attr['fontsize']=10
    G.graph_attr['nodesep']=0.1
    G.graph_attr['ranksep']=0.1
    G.graph_attr['rankdir']='LR'
    #G.graph_attr['size']=3

    goals = [nodeCnt-1]
    totalcosts = costsToGoal(A,goals)
    H=[0]*nodeCnt
    for i in range(nodeCnt):        
        if i==0 or i in goals:
            if nodeCnt<24:
                G.get_node(i).attr['label']=chr(ord('A')+i)
            else:
                G.get_node(i).attr['label']="N%d"%i
        else:            
            H[i] = max(mincost,totalcosts[i]-random.randint(mincost,maxcost))            
            if nodeCnt<24:
                G.get_node(i).attr['label']=chr(ord('A')+i-1)+"\n%d"%H[i]
            else:
                G.get_node(i).attr['label']="N%d\n%d"%(i,H[i])

    G.get_node(0).attr['label']="start"
    G.get_node(nodeCnt-1).attr['label']=u"cél"

    for n,neighbours in graph.iteritems():
        for n2,v in neighbours.iteritems():
            G.get_edge(n,n2).attr['label']=v
    return (G,A,H,goals)

def costsToGoal(A, goalNodes):
    nodeCnt = len(A)
    costs = [float('nan')]*nodeCnt
    l=[]
    for n in goalNodes:
        costs[n] = 0
        l.append(n)
    while True:
        l = sorted(l,key=lambda x: costs[x])
        nextnode = l.pop(0)
        for i in range(nodeCnt):        
            cost = A[nextnode][i]
            if math.isnan(costs[i]) and not math.isnan(cost):
                costs[i] = costs[nextnode] + cost
                l.append(i)
        if len(l)==0:
            break
    return costs


def astarsolver(A, H, goalNodes, nodeNames=None):
    closedSet=[]
    openSet=[0]
    g = [float("inf")]*len(A)
    g[0] = 0
    f = [float("inf")]*len(A)
    f[0] = g[0] + H[0]

    ret = ""
    while openSet:        
        current = openSet.pop(0)
        if nodeNames:
            ret = ret + "\n%s: "%nodeNames[current]
        else:
            ret = ret + "\n%d: "%current

        if current in goalNodes:
            ret = ret + "GOAL"
            return ret
        closedSet.append(current)
        for nb in range(len(A)):
            cost = A[current][nb]
            if math.isnan(cost):
                continue
            if nb in closedSet:
                continue
            tg = g[current] + cost
            if not nb in openSet:
                openSet.append(nb)
            elif tg >= g[nb]:
                continue

            g[nb] = tg
            f[nb] = g[nb] + H[nb]
        openSet = sorted(openSet,key=lambda x: f[x])
        if nodeNames:
            ret = ret + ", ".join(["%s(%d,%d,%d)"%(nodeNames[i],H[i],g[i],f[i]) for i in openSet])
        else:
            ret = ret + ", ".join(["%d(%d,%d,%d)"%(i,H[i],g[i],f[i]) for i in openSet])


def astar_question(request):
    (G,A,H,goals)=astargraph(**processparams(request))
    names = []
    for i in range(len(A)):
        names.append(G.get_node(i).attr['label'].split("\n")[0])

    solution = astarsolver(A, H, goals, names)    

    G.layout(prog="dot")
    svgdata=G.draw(format='svg')

    q={}
    a={}
    q['text'] = (u"A* keresési algoritmussal találja meg a <i>start</i> pontból a <i>cél</i> "
        u"pontig vezető legolcsóbb utat. Az útköltségek az éleken, a heurisztika értékek a "
        u"körökben láthatók. A keresés előrehaladását Open listákkal adja meg táblázatosan. "
        u"Az Open listán minden csomópont mellé jegyezze fel annak (h, Σg, f) értékét. A pillanatnyi "
        u"legjobb csomópontot húzza alá!")
    q['score'] = 5
    q['extra'] = svgdata.decode("utf-8")

    a['text'] = q['text']
    a['score'] = q['score']
    a['extra'] = solution    

    return (q,a)

def astar(request):
    
    (q,a) = astar_question(request)

    html = u"<p>%s (%d pont)</p><div>%s</div><div>Megoldás:<pre><code>%s</code></pre></div>"%(q['text'], q['score'], q['extra'], a['extra'])

    return HttpResponse(html)

'''
                <div style="float: right;">
                    {{question.extra | safe}}
                </div>
                <p align="justify">{{question.text | safe}}</p>                     
                <div style=" clear:both;"></div>
                {{question.answer | safe}}
'''