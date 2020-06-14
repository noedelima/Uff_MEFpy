'''
Funções auxiliares para cálculo de treliças
utilizando Método dos Elementos Finitos

Noé de Lima <noe_lima@id.uff.br>
Última modificação: 13/06/2020
'''

# Bibliotecas importadas
from numpy import array
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