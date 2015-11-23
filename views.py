# coding: utf8
from django.shortcuts import render
from django.http import HttpResponse
import question_astar
import question_minimax
from django.utils.encoding import smart_str, smart_unicode

# Create your views here.

def index(request):
    return HttpResponse(u"<a href=astar>A* keresés</a><br><a href=minimax>minimax játékfa</a><br><a href=static/valami.html>v</a>")
    
def processparams(request):
    urlparams = {}
    for k,v in request.GET.dict().iteritems():
        if k=="seed":
            urlparams[k]=int(v)
        if k=="minbranch" or k=="maxbranch":
            ss = v.replace("[","").replace("]","").split(',')
            urlparams[k]=[int(i) for i in ss]
        else:
            urlparams[k]=max(min(int(v),500),-500)
    return urlparams



def astar(request):
    (G,A,H,goals)=question_astar.astargraph(**processparams(request))
    names = []
    for i in range(len(A)):
        names.append(G.get_node(i).attr['label'].split("\n")[0])

    solution = question_astar.astarsolver(A, H, goals, names)    

    G.layout(prog="dot")
    svgdata=G.draw(format='svg')

    html = (u"<p>A* keresési algoritmussal találja meg a <i>start</i> pontból a <i>cél</i> "
           u"pontig vezető legolcsóbb utat. Az útköltségek az éleken, a heurisztika értékek a "
           u"körökben láthatók. A keresés előrehaladását Open listákkal adja meg táblázatosan. "
           u"Az Open listán minden csomópont mellé jegyezze fel annak (h, Σg, f) értékét. A pillanatnyi "
           u"legjobb csomópontot húzza alá! (5 pont)</p><div>%s</div><div>Megoldás:<pre><code>%s</code></pre></div>"%(svgdata.decode("utf-8"),solution))

    return HttpResponse(html)

def minimax(request):

    (G, graph, depths, values, ismaxstarts) = question_minimax.minimaxgraph(**processparams(request))            
    G2 = question_minimax.minimaxsolver(G, graph, depths, values, ismaxstarts)    
    svgdata = G.draw(format='svg')
    svgdata2 = G2.draw(format='svg')

    if ismaxstarts:
        rootplayer = "MAX"
    else:
        rootplayer = "MIN"

    html = (u"<p>Az ábrán látható egy játékfa. A feladat (a) megadni a %s játékoshoz tartozó gyökér minimax értékét "
            u"a hiányzó hasznosságok beírásával, (b) bejelölni az élek végén lévő kis kör besatírozásával "
            u"az alfa és a béta értékekre vonatkozó érveléssel együtt, hogy mely ágakat "
            u"metszene el az alfa-béta metszés, ha a fa bejárása balról-jobbra történik. (5 pont)"
            u"</p><div>%s</div><div>Megoldás:<br/>%s</div>"%(rootplayer, svgdata.decode("utf-8"),svgdata2.decode("utf-8")))

    return HttpResponse(html)
