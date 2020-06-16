'''
Funções auxiliares para cálculo de treliças
utilizando Método dos Elementos Finitos

Noé de Lima <noe_lima@id.uff.br>
Última modificação: 13/06/2020
'''

# Bibliotecas importadas
from numpy import array,sqrt,sin,cos,arctan
import json

# Classe para armazenar nós
class node:
    def __init__(self,x=0,y=0,z=0,rx=False,ry=False,rz=False,tag=''):
        self.x = x
        self.y = y
        self.z = z
        self.Rx = rx
        self.Ry = ry
        self.Rz = rz
        self.tag = tag
        
# Classe para armazenar barras
class bar:
    def __init__(self,no1,no2,EA,tag=''):
        self.dx = no2.x - no1.x # Delta x da barra
        self.dy = no2.y - no1.y # Delta y da barra
        self.L = sqrt(self.dx**2 + self.dy**2)
        self.a = arctan(self.dy/self.dx) # Ângulo alpha da barra
        self.EA = EA
        
# Função para calcular a Matriz de Rotação T
def mat_T(a=0):
    T = array([
        [cos(a)**2, sin(a)*cos(a), -cos(a)**2, -sin(a)*cos(a)],
        [sin(a)*cos(a), sin(a)**2, -sin(a)*cos(a), -sin(a)**2],
        [-cos(a)**2, -sin(a)*cos(a), cos(a)**2, sin(a)*cos(a)],
        [-sin(a)*cos(a), -sin(a)**2, sin(a)*cos(a), sin(a)**2],
    ])
    return T

# Classe para tratar as treliças
class trelica:
    def __init__(self, path):
        self.file = None
        self.n = 0
        self.barras = array([[0]])
        self.cargas = array([[0]])
        self.nos = []
        try:
            with open(path,'r') as f:
                self.file = json.load(f)
                self.n = self.file['n']
                self.barras = array(self.file['bars'])
                self.cargas = array(self.file['loads'])
                for name, value in self.file['nodes'].items():
                    no = node(value['x'],value['y'],value['z'],value['Rx'],value['Ry'],value['Rz'],name)
                    self.nos.append(no)
        except IOError as err:
            print('File Error: ' + str(err))
        except JSONDecodeError as err:
            print('JSON Error: ' + str(err))
        finally:
            return