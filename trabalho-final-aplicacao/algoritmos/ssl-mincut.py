# -*- coding: utf-8 -*-
import igraph as ig, numpy as np
from openopt import MILP

def mincut(vec, pos, neg,METRICA="euclidiana", LIMIAR=0.2, alfa=1.):
    """Realiza algoritmo de mincut de aprendizado semi-supervisionado

    Parâmetros
    ----------
    vec : vetor
        Vetor dos objetos com seus parâmetros para que as distâncias sejam calculadas. Cada linha é um objeto, cada coluna um parâmetro.
    L : vetor
        Vetor l x C, em que cada linha contem o dado rotulado e cada coluna contém 1 na classe correspondente.
    Li : vetor
        Vetor com os índices dos objetos referentes a L.
    METRICA : string
        String especificando se a métrica é "euclidiana" ou "exponencial"
    LIMIAR : float
        Número de ponto flutuante específicando o peso mínimo da aresta a ser construída.
    alfa : float
        Hiperparâmetro regulador da métrica exponencial.
    """
    n=len(vec)

    # Grafo não dirigido, cada nó um ponto
    g=ig.Graph(n)

    vec=np.array(vec)

    for i in xrange(0,n-1):
        for j in xrange(i+1,n):
            count+=1
            if i in pos and j in pos:
                g.add_edges((i,j))
                g.es[len(g.es)-1]["weight"]=np.inf
                ws.append(np.inf)

            elif i in neg and j in neg:
                g.add_edges((i,j))
                g.es[len(g.es)-1]["weight"]=np.inf
                ws.append(np.inf)
                ws_rm.append(count)
            elif METRICA=="euclidiana":
                d=(sum((v[i]-v[j])**2))**0.5
                print d
                if d < LIMIAR:
                    g.add_edges((i,j))
                    print "aresta feita!!!!!!"
                    g.es[len(g.es)-1]["weight"]=1/d
                    ws.append(1/d)
            elif METRICA=="exp":
                d=(sum((v[i]-v[j])**2))**0.5
                w=np.exp(-dist/alfa)
                print w
                if w > LIMIAR:
                    g.add_edges((i,j))
                    print "aresta feita!!!!!!"
                    g.es[len(g.es)-1]["weight"]=w
                    ws.append(w)

    #print .
    val=g.mincut_value(pos[0],neg[0],"weight")
    for i in xrange(len(g.es)):
        asum=0
        ws=g.es["weight"]


    return g.mincut("weight")

"""
a = np.arange(10) this is your problem
06:47 < seberg> m = MILP(f=a, Aeq=a, beq=[yoursum], intVars=range(len(a)), 
                lb=np.zeros(len(a)), ub=np.ones(len(a)))

ws=g.es["weight"]
np.delete(ws,ws_rm,0)
val=g.mincut_value(pos[0],neg[0],"weight")
m = MILP(f=ws, Aeq=ws, beq=[val], intVars=range(len(ws)), lb=np.zeros(len(ws)), ub=np.ones(len(ws)))
m.solve('glpk')
"""
if __name__=="__main__":
    ###########################
    METRICA="euclidiana"
    LIMIAR_D=0.2

    METRICA="exp"
    LIMIAR_E=0.2
    alfa=10.

    #################
    # Carregando vetor
    a=open("opiniao.arff","rb")
    vec=a.read(); a.close()
    vec=vec.split("@DATA"); vec=vec[1].split()
    vec=[i.split(",")[:-1] for i in vec]
    v=np.float64(vec)
    vec=[[float(i[0]),float(i[1])] for i in vec]
    #################

    #################
    # Definindo dados rotulados
    n=len(v)
    foo=np.arange(72); np.random.shuffle(foo)
    pos=foo[:36] # 20%

    foo=np.arange(72,n); np.random.shuffle(foo)
    neg=foo[:36] # 20%
    ################

    l=list(pos)+list(neg)

    L=np.zeros((len(l),2))
    L[:len(pos)][:,0]=1 # positivos
    L[len(pos):][:,1]=1 # negativos
    
    particao=mincut(v,pos,neg, LIMIAR=2)
