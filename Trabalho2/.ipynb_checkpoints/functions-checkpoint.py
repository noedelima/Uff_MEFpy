'''
Funções auxiliares para cálculo de treliças
utilizando Método dos Elementos Finitos

Noé de Lima <noe_lima@id.uff.br>
Última modificação: 13/06/2020
'''

# Bibliotecas importadas
from numpy import array,angle,zeros
from numpy.linalg import norm
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
        self.supp = array([rx,ry,rz])
        
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
                self.cargas = array(self.file['loads'])
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
                    # Cálculo dos Vetores u e f
                    ff = array([0.,0.])
                    uu = array([0.,0.])
                    if self.nos[i].
                    self.u[i] =
                    self.f[i] =
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
