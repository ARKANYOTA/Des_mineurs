#!/usr/bin/env python
# vim: set sw=4 sts=4 et fdm=marker:
# ┎━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Nom:Carlisi Nolan, Billotte Théodore TG 04 ┃
# ┃ Fichier: main.py                           ┃
# ┃ Exercice Des Mineurs (M. Rive)             ┃
# ┖━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#############
#  IMPORTS  #
#############
import random

import pygame
import sys


#############
#  CLASSES  #
#############
class Grid:
    def __init__(self, size: int, bombes: int):
        self.grid = [[Case() for _ in range(size)] for _ in range(size)]
        self.bombes = bombes
        self.size = size
        self.finished = False

    def start(self, x: int, y: int):
        rnd_grid = [[random.random() for _ in range(self.size)] for _ in range(self.size)]

        for i in range(3):
            for j in range(3):
                if self.size > y+i and 0 <= y+i-1 and self.size > x+j and 0 <= x+j-1:
                    rnd_grid[y+(i-1)][x+(j-1)] = 0

        for bombe in range(self.bombes):
            m = 0
            coords = ()
            for i in range(len(rnd_grid)):
                M = max(rnd_grid[i])
                if M > m:
                    m = M
                    coords = (rnd_grid[i].index(M), i)
            self.grid[coords[1]][coords[0]].is_bombe = True
            rnd_grid[coords[1]][coords[0]] = 0

    def is_finished(self):
        b = True
        for row in self.grid:
            for case in row:
                if not case.is_discovered:
                    b = False
        return self.finished or b


class Case:
    def __init__(self):
        self.is_discovered = False
        self.is_bombe = False
        self.nb_bombes = 0
        self.sprite = None


class GLOBALS:
    grid_size = 10
    bombes = 5
    grid = Grid(grid_size, bombes)


#############
#  FUNCTION #
#############
def main():
    GLOBALS.grid.start(0, 0)


#############
# LANCEMENT #
#############
if __name__ == "__main__":
    argv = sys.argv[1:]  # Eviter le python et nom du programe
    if 1 <= len(argv) <= 2:
        GLOBALS.grid_size = argv[0]
        GLOBALS.nb_de_debombes = argv[1]
    main()
