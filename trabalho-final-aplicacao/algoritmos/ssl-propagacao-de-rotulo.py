# -*- coding: utf-8 -*-
import numpy as np, networkx as nx, pylab as p, os

a=open("opiniao.arff","rb")
vec=a.read(); a.close()
vec=vec.split("@DATA"); vec=vec[1].split()
vec=[i.split(",")[:-1] for i in vec]
v=np.float64(vec)
vec=[[float(i[0]),float(i[1])] for i in vec]

p.plot(v[0:71,0],v[0:71,1],"go")
p.plot(v[71:,0],v[71:,1],"ro"); p.show()

n=len(vec)
# Matriz de rótulos
#pos= [1,5,30,45,55]
#pos=[15,  8,  4, 29, 16]
#pos=[24, 60, 28,  2, 19]
#pos=[51,64,57,4,28] # escolhidos à dedo
foo=np.arange(72); np.random.shuffle(foo)
pos=foo[:36] # 20%

#neg = [79,90,99,120,140]
#neg = [ 93, 121, 114,  97,  96]
#neg = [ 89, 122, 140, 124,  93]
#neg=[84, 78, 79, 125, 104] ### escolhidos à dedo
foo=np.arange(72,n); np.random.shuffle(foo)
neg=foo[:36] # 20%
l=list(pos)+list(neg)

L=np.zeros((len(l),2))
L[:len(pos)][:,0]=1 # positivos
L[len(pos):][:,1]=1 # negativos


n=len(vec)

##########
# Propagação de rótulo
# Grafo totalmente conectado, com peso.
# Hiperparâmetro regulador = alfa
alfa=10.

pesos=np.zeros((n,n))
for i in xrange(0,n-1):
    for j in xrange(i+1,n):
        dist=sum((v[i]-v[j])**2)**0.5
        w=np.exp(-dist/alfa)

        pesos[i][j]=pesos[j][i]=w


# Matriz de probabilidade de transição
P=np.zeros((n,n))
for i in xrange(0,n): # linha
    peso_total=pesos[i].sum()
    P[i]=pesos[i]/peso_total
# particionando corretamente a matriz P
Pu=np.delete(P,l,0)
Puu=np.delete(Pu,l,1)

foo=np.arange(n)
bar=np.delete(foo,l)
Pul=np.delete(Pu,bar,1)

I= np.identity(Puu.shape[0])

f= np.dot( np.linalg.inv(I-Puu), np.dot(Pul,L) )

num=n-len(l)-(72 -len(neg))
pos_rec=( f[:,0]>.5)[:num].sum()
neg_rec= (f[:,1]>.5)[num:].sum()
ppos=100.*pos_rec/(n-len(l)-L[0,:].sum())
pneg=100.*neg_rec/(n-len(l)-L[1,:].sum())
p=(ppos+pneg)/2

# Precisão e cobertura
prec_p=float(pos_rec)/(pos_rec+36-neg_rec)
cob_p=float(pos_rec)/36

prec_n=float(neg_rec)/(neg_rec+36-pos_rec)
cob_n=float(neg_rec)/36

foo="porcentagem de acerto: %.2f" % ( p )
print foo
os.system("echo '"+ foo + "' >> " + "resultado0.5.txt")

foo="positivos, precisão: %.2f, cobertura: %.2f" % ( prec_p*100, cob_p*100 )
print foo
os.system("echo '"+ foo + "' >> " + "resultado0.5.txt")

foo="negativos, precisão: %.2f, cobertura: %.2f" % ( prec_n*100, cob_n*100 )
print foo
os.system("echo '"+ foo + "' >> " + "resultado0.5.txt")
os.system("echo  >> " + "resultado0.5.txt")


#print pos_rec, neg_rec
#res=str((pos_rec,neg_rec)) + " => " + str(ppos)+"% "+str(pneg)+"%" + ", acertos "+str(p) + "%"
#print res
#os.system("echo '"+ res + "' >> " + "resultado0.5.txt")














