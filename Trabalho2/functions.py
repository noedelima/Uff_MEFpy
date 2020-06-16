'''
Funções auxiliares para cálculo de treliças
utilizando Método dos Elementos Finitos

Noé de Lima <noe_lima@id.uff.br>
Última modificação: 13/06/2020
'''

# Bibliotecas importadas
from numpy import array,angle
from numpy.linalg import norm
import json

# Classe para armazenar nós
class node:
    def __init__(self,x=0,y=0,z=0,rx=False,ry=False,rz=False,tag=''):
        self.dot = array([x,y,z])
        self.supp = array([rx,ry,rz])
        self.tag = tag
        
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
        return B.transpose()*(self.EA/(L**2))*B # Matriz de Rigidez Local
        
# Classe para tratar as treliças
class trelica:
    def __init__(self, path):
        try:
            with open(path,'r') as f:
                self.file = json.load(f)
                self.n = self.file['n']
                self.barras = array(self.file['bars'])
                self.cargas = array(self.file['loads'])
                self.nos = []
                for name, value in self.file['nodes'].items():
                    no = node(value['x'],value['y'],value['z'],value['Rx'],value['Ry'],value['Rz'],name)
                    self.nos.append(no)
        except IOError as err:
            print('File Error: ' + str(err))
        except JSONDecodeError as err:
            print('JSON Error: ' + str(err))
