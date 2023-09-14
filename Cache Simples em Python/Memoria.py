from abc import abstractmethod
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

    def __init__(self, k, lines, ram):
        Memoria.__init__(self, k)
        line = [0] * (lines+2)
        self.memoria = [line] * (int(self.tamanho() / lines)) 
        self.qtd_linhas = int(self.tamanho() // lines)
        self.tam_linhas = lines
        self.ram = ram
        self.tamanhow = int(math.log2(self.tam_linhas))
        self.tamanhor = int(math.log2(self.qtd_linhas))
        self.tamanhot = int((math.log2(self.ram.tamanho())) - self.tamanhow -self.tamanhor)
        for i in range(self.qtd_linhas):
            ender_ram = i << (self.tamanhow)
            for j in range(self.tam_linhas):
                self.memoria[i][j+2] = self.ram.read(ender_ram+j)
            self.memoria[i][0] = 0
            self.memoria[i][1] = 0 

    def read(self, ender):

        w = ender & (2**self.tamanhow) -1
        r = (ender >> self.tamanhow) & (2**self.tamanhor) -1
        t = (ender >> self.tamanhow + self.tamanhor) & (2**self.tamanhot) -1
        s = ((ender >> self.tamanhow) << self.tamanhow)
        

        if self.memoria[r][0] == t:
            print("Cache Hit: " +str(ender))
            return self.memoria[r][w+2]

        if self.memoria[r][1] == 1:
            s_cache = (self.memoria[r][0] >> self.tamanhor & r) >> self.tamanhow
            for i in range(self.tam_linhas):
                self.ram.write(s_cache+i,self.memoria[r][i+2])
            self.memoria[r][1] = 0


        for i in range(self.tam_linhas):
            self.memoria[r][i+2] = self.ram.read(s+i)
        self.memoria[r][0] = t
        print("Cache Miss: " +str(ender))
        return self.memoria[r][w+2]
    
    def write(self, ender, val):
        

        w = ender & (2**self.tamanhow) -1
        r = (ender >> self.tamanhow) & (2**self.tamanhor) -1
        t = (ender >> self.tamanhow + self.tamanhor) & (2**self.tamanhot) -1
        s = ((ender >> self.tamanhow) << self.tamanhow)

        if self.memoria[r][0] == t:
            self.memoria[r][1] = 1
            self.memoria[r][w+2] = val
            print("Cache Hit: " +str(ender))
            return

        if self.memoria[r][1] == 1:
            s_cache = (self.memoria[r][0] >> self.tamanhor & r) >> self.tamanhow
            for i in range(self.tam_linhas):
                self.ram.write(s_cache+i,self.memoria[r][i+2])

        for i in range(self.tam_linhas):
            self.memoria[r][i+2] = self.ram.read(s+i)
        
        self.memoria[r][0] = t
        self.memoria[r][1] = 1
        self.memoria[r][w+2] = val
        print("Cache Miss: " +str(ender))