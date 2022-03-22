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
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.group = pygame.sprite.Group()
        self.bombes = bombes
        self.size = size
        self.finished = False

    def start(self, x: int, y: int):
        rnd_grid = [[random.random() for _ in range(self.size)] for _ in range(self.size)]

        for i in range(3):
            for j in range(3):
                if self.size > y + i and 0 <= y + i - 1 and self.size > x + j and 0 <= x + j - 1:
                    rnd_grid[y + (i - 1)][x + (j - 1)] = 0

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
    def __init__(self, screen_pos, grid_pos, grille):
        self.screen_pos = screen_pos
        self.grid_pos = grid_pos
        self.is_discovered = False
        self.is_bombe = False
        self.nb_bombes = 0
        self.sprite = None
        self.grille = grille


class Globals:
    # STATICS
    GRID_SIZE = 50
    ISIZE = WIDTH, HEIGHT = 900, 700
    CASE_SIZE = 600 / GRID_SIZE
    BOMBES = 5
    GRID = Grid(GRID_SIZE, BOMBES)

    # GLOBAL VARIABLES
    run = True


class Colors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)


class Pygame:
    @staticmethod
    def image(name: str, size: tuple):
        return pygame.transform.scale(pygame.image.load(f'./ressources/normal/{name}.png'), size)


#############
#  FUNCTION #
#############
def main():
    pygame.init()
    screen = pygame.display.set_mode(Globals.ISIZE)

    while Globals.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.run = False

        screen.fill(Colors.WHITE)
        rect = pygame.rect.Rect(150, 50, 600, 600)
        pygame.draw.rect(screen, Colors.BLACK, rect)

        y, yi = 0, 0
        while y < 600:
            x, xi = 0, 0
            while x < 600:
                img = Pygame.image('cell-covered', (Globals.CASE_SIZE, Globals.CASE_SIZE))
                screen.blit(img, (150+x, 50+y))
                x += Globals.CASE_SIZE
                xi += 1
            y += Globals.CASE_SIZE
            yi += 1
        pygame.display.flip()


#############
# LANCEMENT #
#############
if __name__ == "__main__":
    argv = sys.argv[2:]  # Eviter le python et nom du programe
    if 1 <= len(argv) <= 2:
        Globals.grid_size = int(argv[0])
        Globals.bombes = int(argv[1])
    main()