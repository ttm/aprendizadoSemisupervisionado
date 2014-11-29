# -*- coding: utf-8 -*-
import networkx as nx, numpy as N

# Closeness Vitality é:
# -Uma medida referente a um nó ou uma aresta
# que corresponte à diferença entre as distâncias
# entre cada par de nós no caso do nó ou aresta ser retirada.

# Note que a soma das distâncias entre cada par de nós
# corresponde à soma do inverso da centralidade.

# Use com:
#from closeness_vitality import *
#g=nx.erdos_renyi_graph(20,.4), g é o grafo
#closeness_vitality(g,1), 1 é o vértice de interesse
# para uma demonstração, basta rodar com:
# python closeness_vitality.py



def closeness_vitality(grafo,vertice, aresta=False):
    """Calcula closeness vitality do vértice no grafo

    Retorna a closeness vitality para o vértice ou aresta especificado
    no grafo especificado.

    Parâmetros
    ----------
    grafo: grafo networkx
        Grafo no qual se quer calcular closeness vitality.
    vertice: identificador
        Identificador do vértice para o qual se quer a medida.
    aresta: tupla
        Identificador dos vértices que formam a aresta para o qual se quer a medida de centralidade.
    """

    g_foo=nx.copy.deepcopy(grafo)
    dists=nx.shortest_path_length(g_foo, weighted=True)
    vertices=g_foo.nodes()
    pares=[]
    soma_dists1=0
    for v1 in vertices:
        for v2 in vertices:
            if set((v1,v2)) not in pares:
                soma_dists1+=dists[v1][v2]
                pares.append(set((v1,v2)))
    Iwg=soma_dists1

    if aresta:
        g_foo.remove_edge(aresta[0],aresta[1])
        dists=nx.shortest_path_length(g_foo, weighted=True)
        vertices=g_foo.nodes()
        pares=[]
        soma_dists2=0
        for v1 in vertices:
            for v2 in vertices:
                if set((v1,v2)) not in pares:
                    soma_dists2+=dists[v1][v2]
                    pares.append(set((v1,v2)))
        Iwg2=soma_dists2
        return Iwg-Iwg2

    g_foo.remove_node(vertice)

    dists=nx.shortest_path_length(g_foo, weighted=True)
    vertices=g_foo.nodes()
    pares=[]
    soma_dists2=0
    for v1 in vertices:
        for v2 in vertices:
            if set((v1,v2)) not in pares:
                soma_dists2+=dists[v1][v2]
                pares.append(set((v1,v2)))
    Iwg2=soma_dists2

    return Iwg-Iwg2




if __name__=="__main__":

    grafo=nx.random_graphs.barabasi_albert_graph(50,5)
    #grafo=nx.barbell_graph(15,20)
    cores=[]
    for v in grafo.nodes():
        print v
        cores.append(closeness_vitality(grafo,v))
    import pylab as pl
    print "AAAAAAAAAA"
    nx.draw(grafo,node_size=100,node_color=cores)
    pl.colorbar()
    pl.show()
