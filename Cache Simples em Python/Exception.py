#!/usr/bin/env python3

#
# von Neumann - Arquitetura Básica
# Todos as classes em um mesmo arquivo
# PSCF - Prof. Luiz Lima Jr.
#
# Arquitetura formada de 3 componentes básicos:
#
# 1. Memória => RAM
# 2. CPU
# 3. Entrada e Saída (IO)
#

from abc import abstractmethod
import sys

# Exceção (erro)
class EnderecoInvalido(Exception):
    def __init__(self, ender):
        self.ender = ender

    def __repr__(self):
        return self.ender




