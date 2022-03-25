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
import os

sys.setrecursionlimit(10000)

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


#############
#  CLASSES  #
#############
class Globals:
    # STATICS
    GRID_SIZE = 50
    ISIZE = WIDTH, HEIGHT = 900, 700
    CASE_SIZE = 600 / GRID_SIZE
    BOMBES = 100
    GRID = None

    # GLOBAL VARIABLES
    run = True
    menu = 0


class Colors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    BG = pygame.Color(200, 200, 200)


class Fonts:
    _ = pygame.font.init()
    TITLE = pygame.font.SysFont('calibri', 64, True, False)
    BUTTON = pygame.font.SysFont('calibri', 50, True, False)


def image(name: str, size: tuple):
    return pygame.transform.scale(pygame.image.load(f'./ressources/{name}.png'), size)


class Images:

    @staticmethod
    def getCovered():
        return image('cell-covered', (Globals.CASE_SIZE, Globals.CASE_SIZE))

    @staticmethod
    def getFlagged():
        return image('cell-flagged', (Globals.CASE_SIZE, Globals.CASE_SIZE))

    @staticmethod
    def getMine():
        return image('mine', (Globals.CASE_SIZE, Globals.CASE_SIZE))

    @staticmethod
    def getMineExploded():
        return image('mine-exploded', (Globals.CASE_SIZE, Globals.CASE_SIZE))

    @staticmethod
    def getButton():
        return image('button', (256, 128))

    @staticmethod
    def getCell(bombes: int):
        return image(f'cell-{bombes}', (Globals.CASE_SIZE, Globals.CASE_SIZE))


class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, image: pygame.surface.Surface, pos: tuple):
        super(Sprite, self).__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Button(Sprite):
    def __init__(self, text: str, pos: tuple):
        img: pygame.Surface = Images.getButton()
        txt = Fonts.BUTTON.render(text, False, (100, 100, 100))
        self.text = text

        x_percent = img.get_size()[0] * 0.8 / txt.get_size()[0]
        txt = pygame.transform.scale(txt, (int(txt.get_size()[0] * x_percent), int(txt.get_size()[1] * x_percent)))

        if txt.get_size()[1] > img.get_size()[1]:
            y_percent = (img.get_size()[1] * 0.9) / txt.get_size()[1]
            txt = pygame.transform.scale(txt, (int(txt.get_size()[0] * y_percent), int(txt.get_size()[1] * y_percent)))
        img.blit(txt, ((img.get_size()[0]-txt.get_size()[0])/2, (img.get_size()[1]-txt.get_size()[1])/2))
        super(Button, self).__init__(img, pos)


class MainMenu(pygame.sprite.Group):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.bg = Colors.BG
        title = Sprite(Fonts.TITLE.render('Le Jeu des Mineurs', Colors.BLACK, False), (200, 70))
        test_button = Button('Jouer', (160, 200))
        play_button = Button('Challenges', (460, 200))
        challenge_button = Button('Leaderboard', (160, 400))
        leaderboard_button = Button('Quitter', (460, 400))

        self.add(title, test_button, play_button, challenge_button, leaderboard_button)


class GameMenu(pygame.sprite.Group):
    def __init__(self):
        super(GameMenu, self).__init__()
        self.bg = Colors.WHITE
        r = pygame.rect.Rect(0, 0, 270, 600)
        s = pygame.surface.Surface((r.w, r.h))
        s.fill(Colors.BG)
        rect = Sprite(s, (620, 90))
        self.add(rect)



class Grid(pygame.sprite.Group):
    def __init__(self, size: int, bombes: int):
        super().__init__()
        self.bombes = bombes
        self.size = size
        self.finished = False
        self.exploded = False
        self.started = False
        self.bombes_list = []

        self.grid = []
        y, yi = 0, 0
        while y < 600:
            self.grid.append([])
            x, xi = 0, 0
            while x < 600:
                img = image('cell-covered', (Globals.CASE_SIZE, Globals.CASE_SIZE))
                self.grid[yi].append(Case(img, (10 + x, 90 + y), (xi, yi), self))
                x += Globals.CASE_SIZE
                xi += 1
            y += Globals.CASE_SIZE
            yi += 1

    def start(self, x: int, y: int):
        self.started = True
        rnd_grid = [[random.random() for _ in range(self.size)] for _ in range(self.size)]

        # éviter de tomber direct sur une bombe et d'avoir des bombes juste a coté
        for i in range(3):
            for j in range(3):
                if self.size >= y + i and 0 <= y + i - 1 and self.size >= x + j and 0 <= x + j - 1:
                    rnd_grid[y + (i - 1)][x + (j - 1)] = 0

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
            self.bombes_list.append(coords)
        self.case_press(x, y)

    def is_finished(self):
        b = True
        for row in self.grid:
            for case in row:
                if not case.is_discovered:
                    b = False
        return self.finished or b

    def count_near_bombes(self, x, y):
        voisins_bombes = 0
        for i in range(3):
            for j in range(3):
                if self.size >= y + i and 0 <= y + i - 1 and self.size >= x + j and 0 <= x + j - 1:
                    voisins_bombes += int(self.grid[y + (i - 1)][x + (j - 1)].is_bombe)  # Ajoute 1 si bombe, sinon 0
        return voisins_bombes

    def case_press(self, x, y):
        if 0 <= x < Globals.GRID_SIZE and 0 <= y < Globals.GRID_SIZE and not self.is_finished():
            case = self.grid[y][x]
            if not self.started:
                self.start(x, y)  # placer les bombes sur le terrain
            if case.is_flag:
                # print("Enlever le drapeau avant de découvrir la case")
                return
            if case.is_discovered:
                # print("Case déjà découverte, Rejouez")
                return
            if case.is_bombe:
                self.finished = True
                case.is_discovered = True
                self.exploded = True
                case.image = Images.getMineExploded()
                for coord in self.bombes_list:
                    self.grid[coord[1]][coord[0]].image = Images.getMineExploded()
                # print("Vous avez perdu, Dommage")
                return
            case.is_discovered = True
            nb_bombes = self.count_near_bombes(x, y)
            case.nb_bombes = nb_bombes
            case.image = Images.getCell(nb_bombes)
            if nb_bombes == 0:
                for i in range(3):
                    for j in range(3):
                        if self.size >= y + i and 0 <= y + i - 1 and self.size >= x + j and 0 <= x + j - 1:
                            if not self.grid[y + (i - 1)][x + (j - 1)].is_discovered:
                                self.case_press(x + (j - 1), y + (i - 1))

    def case_press_flag(self, x, y):
        if 0 <= x < Globals.GRID_SIZE and 0 <= y < Globals.GRID_SIZE and not self.is_finished() and self.started:
            case = self.grid[y][x]
            if case.is_flag:
                case.is_flag = False
                case.image = Images.getCovered()
                return
            if case.is_discovered:
                # print("Case déjà découverte, Pourquoi mettre un drapeau ?")
                return
            case.is_flag = True
            case.image = Images.getFlagged()

    def __repr__(self):
        textout = ""
        for row in self.grid:
            for case in row:
                textout += f'{case} '
            textout += "\n"
        return textout


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
        self.is_flag = False
        self.rect = self.image.get_rect()

        self.rect.x = self.screen_pos[0]
        self.rect.y = self.screen_pos[1]

    def __repr__(self):
        if os.name == 'posix':
            if self.is_discovered:
                if self.is_bombe:
                    return "\033[32m\u2622\033[0m"
                if self.nb_bombes == 0:
                    return " "
                return f'\033[34m{self.nb_bombes}\033[0m'
            if self.is_flag:
                return "\033[33m\u2691\033[0m"
            return "\033[31m\u25A1\033[0m"
        else:
            if self.is_discovered:
                if self.is_bombe:
                    return "\u2622"
                if self.nb_bombes == 0:
                    return " "
                return str(self.nb_bombes)
            if self.is_flag:
                return "\u2691"
            return "\u25A1"


#############
#  FUNCTION #
#############
def main():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode(Globals.ISIZE)
    Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
    
    menus = [MainMenu(), GameMenu()]
    prev_menu = Globals.menu
    while Globals.run:
        if prev_menu != Globals.menu:
            prev_menu = Globals.menu
            if prev_menu == 1:
                Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                xPos, yPos = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed(3)
                if Globals.menu == 1:
                    x, y = int((xPos - 10) // Globals.CASE_SIZE), int((yPos - 90) // Globals.CASE_SIZE)
                    if click[0]:
                        Globals.GRID.case_press(x, y)
                    elif click[2]:
                        Globals.GRID.case_press_flag(x, y)
                for sprite in menus[Globals.menu].sprites():
                    if isinstance(sprite, Button) and sprite.rect.collidepoint(xPos, yPos) and click[0]:
                        sprite: Button
                        if sprite.text == 'Quitter':
                            Globals.run = False
                        elif sprite.text == 'Jouer':
                            Globals.menu = 1
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                        elif sprite.text == 'Challenges':
                            Globals.menu = 2
                        elif sprite.text == 'Leaderboard':
                            Globals.menu = 3
                        elif sprite.text == 'Home':
                            Globals.menu = 0

        screen.fill(menus[Globals.menu].bg)

        if Globals.menu == 1:
            Globals.GRID.draw(screen)
        menus[Globals.menu].draw(screen)

        pygame.display.flip()
        pygame.time.wait(50)


#############
# LANCEMENT #
#############
if __name__ == "__main__":
    argv = sys.argv[1:]  # Éviter le python et nom du programme
    if '--help' in argv:
        print("[-] Usage: python main.py [--help] [--debug] [[GRID_SIZE] [nb_de_bombes]]")
        exit(0)
    if '--debug' in argv:
        del argv[argv.index("--debug")]
        Globals.debug = True
    if 2 <= len(argv):
        Globals.GRID_SIZE = int(argv[0])
        Globals.BOMBES = int(argv[1])
    elif 1 <= len(argv):
        print("[-] Usage: python main.py [--help] [--debug] [[GRID_SIZE] [nb_de_bombes]]")
        print(f"\t\\Default: Size={Globals.GRID_SIZE}, bombes={Globals.BOMBES}")
    main()
