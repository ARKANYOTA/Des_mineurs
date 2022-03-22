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
class Globals:
    # STATICS
    GRID_SIZE = 50
    ISIZE = WIDTH, HEIGHT = 900, 700
    CASE_SIZE = 600 / GRID_SIZE
    BOMBES = 5
    GRID = None

    # GLOBAL VARIABLES
    run = True


class Colors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)


class Pygame:
    @staticmethod
    def image(name: str, size: tuple):
        return pygame.transform.scale(pygame.image.load(f'./ressources/normal/{name}.png'), size)


class Grid(pygame.sprite.Group):
    def __init__(self, size: int, bombes: int):
        super().__init__()
        self.bombes = bombes
        self.size = size
        self.finished = False

        y, yi = 0, 0
        while y < 600:
            x, xi = 0, 0
            while x < 600:
                img = Pygame.image('cell-covered', (Globals.CASE_SIZE, Globals.CASE_SIZE))
                case = Case(img, (150+x, 50+y), (xi, yi), self)
                x += Globals.CASE_SIZE
                xi += 1
            y += Globals.CASE_SIZE
            yi += 1

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


class Case(pygame.sprite.DirtySprite):
    def __init__(self, image, screen_pos, grid_pos, grille):
        super().__init__(grille)
        self.image = image
        self.screen_pos = screen_pos
        self.grid_pos = grid_pos
        self.is_discovered = False
        self.is_bombe = False
        self.nb_bombes = 0
        self.sprite = None
        self.grille = grille
        self.rect = self.image.get_rect()

        self.rect.x = self.screen_pos[0]
        self.rect.y = self.screen_pos[1]


#############
#  FUNCTION #
#############
def main():
    pygame.init()
    screen = pygame.display.set_mode(Globals.ISIZE)
    Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)

    while Globals.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.run = False

        Globals.GRID.draw(screen)
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
