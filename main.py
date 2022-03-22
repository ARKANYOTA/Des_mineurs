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
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


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

        # éviter de tomber direct sur une bombe et d'avoir des bombes juste a coté
        for i in range(3):
            for j in range(3):
                if self.size > y+i and 0 <= y+i-1 and self.size > x+j and 0 <= x+j-1:
                    rnd_grid[y+(i-1)][x+(j-1)] = 0

        # Récupère les self.bombes plus grandes valeurs pour les mettre dans la grille 
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
    
    def count_nb_de_voisins_bombes(self, x, y):
        voisins_bombes = 0
        for i in range(3):
            for j in range(3):
                if self.size > y+i and 0 <= y+i-1 and self.size > x+j and 0 <= x+j-1:
                     voisins_bombes += self.grid[y+(i-1)][x+(j-1)].is_bombe
        return voisins_bombes

    def case_press(self, x, y):
        if self.grid[x][y].is_discovered:
            print("Case déjà découverte, Rejouez")
            return
        if self.grid[x][y].is_bombe:
            self.finished = True
            print("Vous avez perdu")
            return
        nb_de_bombdes_autour = self.count_nb_de_voisins_bombes(x, y)
        if nb_de_bombdes_autour == 0:
            for i in range(3):
                for j in range(3):
                    if self.size > y+i and 0 <= y+i-1 and self.size > x+j and 0 <= x+j-1:
                        self.case_press(y+(i-1), x+(j-1))
        
        self.grid[x][y].nb_bombes = nb_de_bombdes_autour
        






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
    debug = False


#############
#  FUNCTION #
#############
def main():
    GLOBALS.grid.start(0, 0)
    GLOBALS.grid.case_press(5, 5)
    if debug:
        print(GLOBALS.bombes)
        print(GLOBALS.grid_size)
        print(GLOBALS.debug)


#############
# LANCEMENT #
#############
if __name__ == "__main__":
    argv = sys.argv[1:]  # Eviter le python et nom du programe
    if '--help' in argv:
        print("[-] Usage: python main.py [--help] [--debug] [[grid_size] [nb_de_bombdes]]")
        exit(0)
    if '--debug' in argv:
        del argv[argv.index("--debug")]
        GLOBALS.debug = True
    if 2 <= len(argv):
        GLOBALS.grid_size = argv[0]
        GLOBALS.bombes = argv[1]
    elif 1 <= len(argv):
        print("[-] Usage: python main.py [--help] [--debug] [[grid_size] [nb_de_bombdes]]")
        print(f"\t\\Default: Size={GLOBALS.grid_size}, bombes={GLOBALS.bombes}")
    main()
