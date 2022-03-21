#!/usr/bin/env python
# vim: set sw=4 sts=4 et fdm=marker:
#┎━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ Nom:Carlisi Nolan, Billotte Théodore TG 04 ┃
#┃ Fichier: main.py                           ┃
#┃ Exercice Des Mineurs                       ┃
#┖━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#############
#  IMPORTS  #
#############
import pygame
import sys


#############
#  CLASSES  #
#############
class Grid:
    def __init__(self, size):
        self.grid = [[0]*size for i in range(size)]


class Case:
    def __init__(self):
        self.is_bombe = False
        self.nb_de_bombe_autour = None
        self.is_visible = False


class GLOBALS:
    grid_size = 10
    nb_de_bombes = 5
    grid = Grid(grid_size)


#############
#  FUNCTION #
#############
def main():
    print("Hello")


#############
# LANCEMENT #
#############
if __name__ == "__main__":
    argv = sys.argv[1:]  # Eviter le python et nom du programe
    if 1 <= len(argv) <= 2:
        GLOBALS.grid_size = argv[0]
        GLOBALS.nb_de_debombes = argv[1]
    main()
