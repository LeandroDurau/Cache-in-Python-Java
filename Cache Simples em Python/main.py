from I_O import IO
from Memoria import RAM
from CPU import CPU
from Memoria import CACHE
import sys
from Exception import EnderecoInvalido

def main():
    try:
        io = IO(sys.stdin, sys.stdout)
        ram = RAM(7)
        cache = CACHE(8, ram)
        cpu = CPU(cache, io)

        inicio = 10
        ram.write(inicio, 118)
        ram.write(inicio + 1, 130)
        cpu.run(inicio)
    except EnderecoInvalido as e:
        print("Endereço inválido:", e.ender, file=sys.stderr)

if __name__ == '__main__':
    main()
