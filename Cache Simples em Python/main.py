from I_O import IO
from Memoria import RAM
from CPU import CPU
from Memoria import CACHE, Cache_real
import sys
from Exception import EnderecoInvalido

def main():
    try:
        io = IO()
        ram = RAM(22)   # 4M de RAM (2**22)
        cache = Cache_real(4 * 2**10, 64, ram) # total cache = 4K, cacheline = 64
        cpu = CPU(cache, io)

        inicio = 0

        print("Programa 1")
        ram.write(inicio, 118)
        ram.write(inicio+1, 130)
        cpu.run(inicio)

        print("\nPrograma 2")
        cache.write(inicio, 4155)
        cache.write(inicio+1, 4165)
        cpu.run(inicio)
    except EnderecoInvalido as e:
	    print("Endereco inválido:", e.ender, file=sys.stderr)
if __name__ == '__main__':
    main()
