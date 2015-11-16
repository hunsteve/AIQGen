# coding: utf8
import pygraphviz as pgv
import random
import math

def char_range(c1, c2):
    ret = []
    for c in xrange(ord(c1), ord(c2)+1):
        ret.append(chr(c))
    return ret




def minimaxgraph(minbranch = [2,2,1,0], maxbranch = [2,2,3,4], maxvalue = 20, minvalue = -20, seed = None, diffsymbol = 0, maxdepth = None):    
    
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
    G.graph_attr['rankdir']='TD'    
    G.graph_attr['nodesep']=0.1

        
    for i in range(len(graph)):        
        if math.isnan(values[i]):
            G.get_node(i).attr['label'] = ""
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
