from abc import abstractmethod
from Exception import EnderecoInvalido

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