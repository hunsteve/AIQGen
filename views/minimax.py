# coding: utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode
import pygraphviz as pgv
import random
import math
from AIQGen.utils import processparams
   
def minimaxgraph(minbranch = [2,2,1,0], maxbranch = [2,2,3,3], maxvalue = 20, minvalue = -20, seed = None, diffsymbol = 0, maxdepth = None):    
    
    random.seed(seed)

    if not maxdepth:
        maxdepth = len(minbranch)

    graph={}    
    depths=[]
    def generateNode(depth, nodeidx):
        graph[nodeidx]={}                
        nextnodeidx = nodeidx + 1
        depths.append(depth)         
        if depth >= maxdepth:            
            return nextnodeidx
        for i in range(random.randint(minbranch[depth],maxbranch[depth])):
            graph[nodeidx][nextnodeidx] = None
            nextnodeidx = generateNode(depth + 1, nextnodeidx)            
        return nextnodeidx

    generateNode(0,0)
    values=[float('nan')]*len(graph)
    
    for i in range(len(graph)):
        if not graph[i]:        
            values[i] = random.randint(minvalue,maxvalue)

    G=pgv.AGraph(graph)
    G.node_attr['shape']='circle'
    G.node_attr['fixedsize']='true'
    G.node_attr['width']=0.33
    G.node_attr['height']=0.33
    G.node_attr['fontsize']=10
    G.edge_attr['fontsize']=10
    G.graph_attr['nodesep']=0.1
    G.graph_attr['ranksep']=0.3
    G.graph_attr['rankdir']='TD'    
    G.graph_attr['nodesep']=0.1
    G.graph_attr['size']=6

        
    for i in range(len(graph)):        
        if math.isnan(values[i]):
            G.get_node(i).attr['label'] = ""            
            G.get_node(i).attr['width']=0.5
            if diffsymbol:
                if depths[i]%2:
                    G.get_node(i).attr['shape'] = "rectangle"
                else:
                    G.get_node(i).attr['shape'] = "diamond"   
            else:
                G.get_node(i).attr['shape'] = "rectangle"
        else:
            G.get_node(i).attr['label'] = values[i]            
            G.get_node(i).attr['shape'] = "circle"
        for child in graph[i]:
            G.get_edge(i, child).attr['dir'] = 'forward'
            G.get_edge(i, child).attr['arrowhead'] = 'odot'
            G.get_edge(i, child).attr['id'] = '%d,%d'%(i, child)
        G.get_node(i).attr['id'] = '%d'%i

    G.layout(prog="dot")      

    ismaxstarts = random.randint(0,1)==0

    return (G, graph, depths, values, ismaxstarts)

def minimaxsolver(G_in, graph, depths, values, ismaxstarts):
    G=G_in.copy()
    newvalues = [None] * len(values)

    def alphabeta(node, alpha, beta, isMax):
        if not graph[node]:
            return values[node]
        if isMax:
            v = float('-inf')
            pruned = False
            haspruned = False
            for child in sorted(graph[node].keys(),key=lambda x: int(G.get_node(x).attr['pos'].split(',')[0])):
                if not pruned:
                    v = max(v, alphabeta(child, alpha, beta, False))
                    alpha = max(alpha, v)
                    if beta<=alpha:
                        pruned = True
                else:
                    haspruned = True
                    G.get_edge(node, child).attr['label'] = 'x'
                    G.get_edge(node, child).attr['fontcolor'] = 'red'
                    G.get_edge(node, child).attr['dir'] = 'forward'
                    G.get_edge(node, child).attr['arrowhead'] = 'dot'
            if (haspruned):
                newvalues[node]="&ge;%s"%v
            else:
                newvalues[node]=v            
            return v
        else:       
            v = float('inf')
            pruned = False
            haspruned = False
            for child in sorted(graph[node].keys(),key=lambda x: int(G.get_node(x).attr['pos'].split(',')[0])):
                if not pruned:
                    v = min(v, alphabeta(child, alpha, beta, True))
                    beta = min(beta, v)
                    if beta<=alpha:
                        pruned = True
                else:
                    haspruned = True
                    G.get_edge(node, child).attr['label'] = 'x'
                    G.get_edge(node, child).attr['fontcolor'] = 'red'
                    G.get_edge(node, child).attr['dir'] = 'forward'
                    G.get_edge(node, child).attr['arrowhead'] = 'dot'
            if (haspruned):
                newvalues[node]="&le;%s"%v
            else:
                newvalues[node]=v
            return v    

    alphabeta(0,-float('inf'),float('inf'), ismaxstarts)

    for i in range(len(graph)):
        if newvalues[i] is not None:
            G.get_node(i).attr['label'] = newvalues[i]
            G.get_node(i).attr['fontcolor'] = 'red'


    G.layout(prog="dot")
    return G

def minimax_question(request):
    

    (G, graph, depths, values, ismaxstarts) = minimaxgraph(**processparams(request))            
    G2 = minimaxsolver(G, graph, depths, values, ismaxstarts)    
    svgdata = G.draw(format='svg')
    svgdata2 = G2.draw(format='svg')

    if ismaxstarts:
        rootplayer = "MAX"
    else:
        rootplayer = "MIN"

    q = {}
    a = {}

    q['text'] = (u"Az ábrán látható egy játékfa. A feladat (a) megadni a %s játékoshoz tartozó gyökér minimax értékét "
        u"a hiányzó hasznosságok beírásával, (b) bejelölni az élek végén lévő kis kör besatírozásával "
        u"az alfa és a béta értékekre vonatkozó érveléssel együtt, hogy mely ágakat "
        u"metszene el az alfa-béta metszés, ha a fa bejárása balról-jobbra történik.")%rootplayer

    q['score'] = 5
    q['extra'] = svgdata.decode("utf-8")

    a['text'] = q['text']
    a['score'] = q['score']
    a['extra'] = svgdata2.decode("utf-8")

    return (q,a)


def minimax(request):
    (q,a) = minimax_question(request)
    
    html = (u"<p>%s (%d pont)</p>%s<div>Megoldás:<br/>%s</div>"%(q['text'], q['score'], q['extra'], a['extra']))

    return HttpResponse(html)

