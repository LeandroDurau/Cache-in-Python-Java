from abc import abstractmethod
import copy
from Exception import EnderecoInvalido
import math
import numpy as np

class Memoria:
    def __init__(self, capacidade):
        self._capacidade = capacidade

    def verifica_endereco(self, ender):
        if (ender < 0) or (ender >= self._capacidade):
            raise EnderecoInvalido(ender)

    def tamanho(self):
        return self._capacidade

    # métodos abstratos devem ser sobrescritos pelas subclasses

    @abstractmethod
    def read(self, ender): pass

    @abstractmethod
    def write(self, ender, val): pass


class RAM(Memoria):
    def __init__(self, k):
        Memoria.__init__(self, 2**k)
        self.memoria = [0] * self.tamanho()

    def read(self, ender):
        super().verifica_endereco(ender)
        return self.memoria[ender]

    def write(self, ender, val):
        super().verifica_endereco(ender)
        self.memoria[ender] = val

class CACHE(Memoria):

    def __init__(self, k, ram):
        Memoria.__init__(self, k)
        self.memoria = [0] * self.tamanho()
        self.inicio = ram.tamanho() + 1
        self.RAM = ram


    def read(self, ender):

        if  ender < self.inicio or ender >= self.inicio + self.tamanho():
            print("Cache Miss: "+ str(ender ))
            self.RAM.verifica_endereco(ender)
            for i in range(self.tamanho()):
                if self.inicio != self.RAM.tamanho() + 1:
                    self.RAM.write(self.inicio + i, self.memoria[i])
                self.memoria[i] = self.RAM.read(ender + i)

            self.inicio = ender
        else:
            print("Cache Hit: " +str(ender))
        return self.memoria[ender - self.inicio]

    def write(self, ender, val):
        if  ender < self.inicio or ender >= self.inicio + self.tamanho():
            print("Cache Miss "+ str(ender))
            self.RAM.verifica_endereco(ender)
            for i in range(self.tamanho()):
                if self.inicio != self.RAM.tamanho() + 1:
                    self.RAM.write(self.inicio + i, self.memoria[i])
                self.memoria[i] = self.RAM.read(ender + i)

            self.inicio = ender
        else:
            print("Cache Hit: "+ str(ender))
        self.memoria[ender - self.inicio] = val



class Cache_real(Memoria):

    #Construtor
    def __init__(self, k, lines, ram):
        Memoria.__init__(self, k)
        #Criando Array do Cache
        self.memoria = []
        for i in range(int(self.tamanho() / lines)):
            #Populando Cache com Lines
            self.memoria.append([-math.inf] * (lines+2)) 

        #Variaveis Uteis
        self.qtd_linhas = int(self.tamanho() // lines)
        self.tam_linhas = lines
        self.ram = ram
        #Calculo w r t
        self.tamanhow = int(math.log2(lines))
        self.tamanhor = int(math.log2(self.qtd_linhas))
        self.tamanhot = int((math.log2(self.ram.tamanho())) - self.tamanhow -self.tamanhor)
        

    #Read na Cache
    def read(self, ender):

        #Calculos dos w r t s para o Endereço
        w = ender & (2**self.tamanhow) -1
        r = (ender >> self.tamanhow) & (2**self.tamanhor) -1
        t = (ender >> (self.tamanhow + self.tamanhor)) & (2**self.tamanhot) -1
        s = ((ender >> self.tamanhow) << self.tamanhow)
        
        #Cache Hit
        if self.memoria[r][0] == t: #Primeiro endereço = Tag
            return self.memoria[r][w+2]

        #Cache Miss
        tag_anterior = self.memoria[r][0]

        #Caso Cache foi modificada
        if self.memoria[r][1] == 1: #Segundo endereço = Modif
            #Localização do Bloco da Cache
            s_cache = ((self.memoria[r][0] << self.tamanhor) | r) << self.tamanhow
            #Escrevendo na Ram
            for i in range(self.tam_linhas):
                self.ram.write(s_cache+i,self.memoria[r][i+2])
            self.memoria[r][1] = 0

        #Pega informação da Ram
        for i in range(self.tam_linhas):
            self.memoria[r][i+2] = self.ram.read(s+i)

        #Atualiza Tag
        self.memoria[r][0] = t
        
        #Print do cache miss caso ja tenha informações na cache
        if tag_anterior != -math.inf:
            s_anteiror = ((tag_anterior<<self.tamanhor) | r)<<self.tamanhow
            print(f'MISS: {ender} L{r}->[{s_anteiror}..{s_anteiror +(2**self.tamanhow-1)} ] | [{s}..{s+(2**self.tamanhow-1)}]->L{r} ')
            #retorna informaçao pedida
            return self.memoria[r][w+2]
        
        print(f'MISS: {ender} [{s}..{s+(2**self.tamanhow-1)}]->L{r} ')
        #retorna informaçao pedida
        return self.memoria[r][w+2]
    
    #Write na Cache
    def write(self, ender, val):
        
        #Calculos dos w r t s para o Endereço
        w = ender & (2**self.tamanhow) -1
        r = (ender >> self.tamanhow) & (2**self.tamanhor) -1
        t = (ender >> self.tamanhow + self.tamanhor) & (2**self.tamanhot) -1
        s = ((ender >> self.tamanhow) << self.tamanhow)

        #Cache Hit
        if self.memoria[r][0] == t: #Primeiro endereço = Tag
            self.memoria[r][1] = 1
            self.memoria[r][w+2] = val
            return
        
        #Cache Miss
        tag_anterior = self.memoria[r][0]

        #Caso Cache foi modificada
        if self.memoria[r][1] == 1: #Segundo endereço = Modif
            #Localização do Bloco da Cache
            s_cache = ((self.memoria[r][0] << self.tamanhor) | r) << self.tamanhow
            #Escrevendo na Ram
            for i in range(self.tam_linhas):
                self.ram.write(s_cache+i,self.memoria[r][i+2])
            self.memoria[r][1] = 0

        #Pega informação da Ram
        for i in range(self.tam_linhas):
            self.memoria[r][i+2] = self.ram.read(s+i)
        
        #Atualiza tag
        self.memoria[r][0] = t
        #Atualiza Modif
        self.memoria[r][1] = 1
        #Atualiza valor
        self.memoria[r][w+2] = val

        #Print do cache miss caso ja tenha informações na cache
        if tag_anterior != -math.inf:
            s_anteiror = ((tag_anterior<<self.tamanhor) + r)<<self.tamanhow
            print(f'MISS: {ender} L{r}->[{s_anteiror}..{s_anteiror +(2**self.tamanhow-1)}] | [{s}..{s+(2**self.tamanhow-1)}]->L{r} ')
            return
        print(f'MISS: {ender} [{s}..{s+(2**self.tamanhow-1)}]->L{r} ')