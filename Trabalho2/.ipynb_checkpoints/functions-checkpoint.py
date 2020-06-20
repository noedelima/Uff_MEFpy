'''
Funções auxiliares para cálculo de treliças
utilizando Método dos Elementos Finitos

Noé de Lima <noe_lima@id.uff.br>
Última modificação: 13/06/2020
'''

# Bibliotecas importadas
from numpy import angle,array,delete,isnan,nan,zeros
from numpy.linalg import norm,solve
import json

# Classe para armazenar nós
class node:
    def __init__(self,x=0,y=0,z=0,tag=''):
        self.dot = array([x,y,z])
        self.l = zeros([3])
        self.u = zeros([3])
        self.s = array([False,False,False])
        self.tag = tag
    
    def support(self,rx,ry,rz):
        self.s = array([rx,ry,rz])
        
    def load(self,fx,fy,fz):
        self.l = array([fx,fy,fz])
        
# Classe para armazenar barras
class bar:
    def __init__(self,no1,no2,EA,tag=''):
        self.at = no1.dot # Origem da barra
        self.vec = no2.dot - no1.dot # Vetor (x,y) da barra
        self.EA = EA # Módulo de Elasticidade x área da seção transversal
        self.tag = tag # Nome de referência para a barra
    def K(self):
        L = norm(self.vec)
        dx = self.vec[0]
        dy = self.vec[1]
        B = array([[-dx,-dy,dx,dy]])/L
        return B.T*(self.EA/L)*B # Matriz de Rigidez Local
    
    def K11(self):
        L = norm(self.vec)
        B = array([[self.vec[0],self.vec[1]]])/L
        return B.T*(self.EA/L)*B
    
    def K12(self):
        return -K11(self)
    
    def K21(self):
        return -K11(self)
    
    def K22(self):
        return K11(self)
        
# Classe para tratar as treliças
class trelica:
    def __init__(self, path):
        try:
            with open(path,'r') as f:
                self.file = json.load(f)
                self.n = self.file['n']
                EA = array(self.file['bars'])
                cargas = array(self.file['loads'])
                self.nos = []
                self.barras = []
                self.K = zeros([2*self.n,2*self.n])
                self.f = zeros([2*self.n])
                self.u = zeros([2*self.n])
                for name, value in self.file['nodes'].items():
                    no = node(value['x'],
                              value['y'],
                              value['z'],
                              name)
                    no.support(value['Rx'],
                              value['Ry'],
                              value['Rz'],)
                    self.nos.append(no)
                for i in range(self.n):
                    no.load(cargas[i][0],
                              cargas[i][1],
                              cargas[i][2],)
                    # Cálculo dos Vetores u e f
                    ff = array([self.nos[i].l[0],self.nos[i].l[1]])
                    uu = array([nan,nan])
                    if self.nos[i].s[0]:
                        uu[0] = 0
                        ff[0] = nan
                    if self.nos[i].s[1]:
                        uu[1] = 0
                        ff[1] = nan
                    self.f[2*i:2*i+2] = ff
                    self.u[2*i:2*i+2] = uu
                    for j in range(i,self.n):
                        if EA[i,j]:
                            barra = bar(self.nos[i],self.nos[j],EA[i,j])
                            # Cálculo da Matriz k
                            self.barras.append(barra)
                            k = barra.K11()
                            self.K[2*i:2*i+2,2*i:2*i+2] += k
                            self.K[2*i:2*i+2,2*j:2*j+2] -= k
                            self.K[2*j:2*j+2,2*i:2*i+2] -= k
                            self.K[2*j:2*j+2,2*j:2*j+2] += k
        except IOError as err:
            print('File Error: ' + str(err))
            return None
        except JSONDecodeError as err:
            print('JSON Error: ' + str(err))
            return None
        finally:
            return
        
    def deslocamentos(self):
        K,u,f = self.K,self.u,self.f
        change = True
        m = 2*self.n
        while change:
            change = False
            for i in range(m):
                if isnan(f[i]):
                    f -= u[i]*K[:,i]
                    K[:,i] = zeros(m)
                    K[i,i] = -1
                    K = delete(K,i,0)
                    K = delete(K,i,1)
                    u = delete(u,i)
                    f = delete(f,i)
                    change = True
                    m -= 1
                    break
        u = solve(K,f)
        k = 0
        for i in range(2*self.n):
            if isnan(self.u[i]):
                self.u[i] = u[k]
                k += 1
        self.f = self.K.dot(self.u)
        for i in range(self.n):
            self.nos[i].load(self.f[2*i],self.f[2*i+1],0.)