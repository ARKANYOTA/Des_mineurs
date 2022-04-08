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
import time

import pygame
import sys
import os

sys.setrecursionlimit(10000)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


#############
#  CLASSES  #
#############
class Globals:
    # STATICS
    GRID_SIZE = 12
    GRID_WIDTH_OR_HEIGHT = 600
    ISIZE = WIDTH, HEIGHT = 900, 700
    CASE_SIZE = GRID_WIDTH_OR_HEIGHT / GRID_SIZE
    BOMBES = 5
    GRID = None
    FPS = 30

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
    GO = pygame.Color(200, 210, 150)


class Fonts:
    _ = pygame.font.init()
    TITLE = pygame.font.SysFont('calibri', 64, True, False)
    BUTTON = pygame.font.SysFont('calibri', 50, True, False)
    GO = pygame.font.SysFont('calibri', 32, True, False)


def image(name: str, size: tuple, angle: int =0, x_flip: bool = False, y_flip: bool = False):
    return pygame.transform.flip(pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f'./ressources/{name}.png'), angle), size), x_flip, y_flip)


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
    def getButton(size=(256, 128)):
        return image('button', size)

    @staticmethod
    def getCell(bombes: int):
        return image(f'cell-{bombes}', (Globals.CASE_SIZE, Globals.CASE_SIZE))


class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, image: pygame.surface.Surface, pos: tuple, name: str=''):
        super(Sprite, self).__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Button(Sprite):
    def __init__(self, pos: tuple, text: str='', btn_image='button', size: tuple=(256, 128), angle: int=0, x_flip: bool=False, y_flip: bool=False, font: pygame.font.Font = Fonts.BUTTON, name: str=''):
        img: pygame.Surface = image(btn_image, size, angle, x_flip, y_flip)
        txt = font.render(text, False, (100, 100, 100))
        self.image = btn_image
        self.text = text
        self.name = name

        if text != '':
            x_percent = img.get_size()[0] * 0.8 / txt.get_size()[0]
            txt = pygame.transform.scale(txt, (int(txt.get_size()[0] * x_percent), int(txt.get_size()[1] * x_percent)))

            if txt.get_size()[1] > img.get_size()[1]:
                y_percent = (img.get_size()[1] * 0.9) / txt.get_size()[1]
                txt = pygame.transform.scale(txt, (int(txt.get_size()[0] * y_percent), int(txt.get_size()[1] * y_percent)))
            img.blit(txt, ((img.get_size()[0] - txt.get_size()[0]) / 2, (img.get_size()[1] - txt.get_size()[1]) / 2))
        super(Button, self).__init__(img, pos, name=name)


class MainMenu(pygame.sprite.Group):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.bg = Colors.BG
        title = Sprite(Fonts.TITLE.render('Le Jeu des Mineurs', Colors.BLACK, False), (200, 70))
        play_button = Button((160, 200), text='Jouer')
        challenge_button = Button((460, 200), text='Challenges')
        leaderboard_button = Button((160, 400), text='Leaderboard')
        quit_button = Button((460, 400), text='Quitter')

        self.add(title, play_button, challenge_button, leaderboard_button, quit_button)


class GameMenu(pygame.sprite.Group):
    def __init__(self):
        super(GameMenu, self).__init__()
        self.bg = Colors.BG
        s = pygame.surface.Surface((270, 600))
        s.fill(Colors.GO)

        quit = Button((750, 20), text='Retour', size=(100, 50))
        title = Sprite(Fonts.TITLE.render('Le Jeu des Mineurs', Colors.BLACK, False), (200, 10))
        rect = Sprite(s, (620, 90))

        time = Sprite(Fonts.TITLE.render('Temps :', Colors.BLACK, False), (630, 150))
        time_t = Sprite(Fonts.TITLE.render('00:00', Colors.BLACK, False), (640, 220))
        mines = Sprite(Fonts.TITLE.render('Mines :', Colors.BLACK, False), (630, 320))
        mines_t = Sprite(Fonts.TITLE.render(str(Globals.BOMBES - Globals.GRID.flags), Colors.BLACK, False), (640, 390))

        self.add(rect, title, quit, time, mines, time_t, mines_t)


class ChallengeMenu(pygame.sprite.Group):
    def __init__(self):
        super(ChallengeMenu, self).__init__()
        self.bg = Colors.BG

        quit = Button((750, 20), text='Retour', size=(100, 50))
        title = Sprite(Fonts.TITLE.render('Le Jeu des Mineurs', Colors.BLACK, False), (200, 10))

        facile = Button((160, 200), text='Facile')
        normal = Button((460, 200), text='Normal')
        difficile = Button((160, 400), text='Difficile')
        impossible = Button((460, 400), text='Impossible')

        self.add(quit, title, facile, normal, difficile, impossible)


class CreationMenu(pygame.sprite.Group):
    def __init__(self):
        super(CreationMenu, self).__init__()
        self.bg = Colors.BG

        quit = Button((750, 20), text='Retour', size=(100, 50))
        creation = Button((300, 500), text='Créer la partie', size=(300, 100), name='create')
        title = Sprite(Fonts.TITLE.render('Le Jeu des Mineurs', Colors.BLACK, False), (200, 10))
        affBombes = Sprite(Fonts.TITLE.render('BOMBES', Colors.BLACK, False), (450, 300))
        affSize = Sprite(Fonts.TITLE.render('CASES', Colors.BLACK, False), (450, 400))

        addMine = Button((360, 300), btn_image='arrow', size=(64, 64), name='addMine')
        remMine = Button((160, 300), btn_image='arrow', size=(64, 64), x_flip=True, name='remMine')
        addSize = Button((360, 400), btn_image='arrow', size=(64, 64), name='addSize')
        remSize = Button((160, 400), btn_image='arrow', size=(64, 64), x_flip=True, name='remSize')

        bombes = Sprite(Fonts.BUTTON.render(str(Globals.BOMBES), Colors.BLACK, False), (260, 310))
        size = Sprite(Fonts.BUTTON.render(str(Globals.GRID_SIZE), Colors.BLACK, False), (260, 410))

        self.add(quit, creation, title, addMine, remMine, addSize, remSize, bombes, size, affSize, affBombes)


class LeaderboardMenu(pygame.sprite.Group):
    def __init__(self):
        super(LeaderboardMenu, self).__init__()
        self.bg = Colors.BG

        quit = Button((750, 20), text='Retour', size=(100, 50))
        title = Sprite(Fonts.TITLE.render('Le Jeu des Mineurs', Colors.BLACK, False), (200, 10))

        self.add(quit, title)

class WinMenu(pygame.sprite.Group):
    def __init__(self):
        super(WinMenu, self).__init__()
        self.bg = Colors.BG
        replay = Button((650, 600), text='Rejouer', size=(200, 75), name='replay')
        text = Sprite(Fonts.GO.render('Vous avez gagné !', Colors.BLACK, False), (635, 550))

        self.add(replay, text)

class GameOverMenu(pygame.sprite.Group):
    def __init__(self):
        super(GameOverMenu, self).__init__()
        self.bg = Colors.BG
        replay = Button((650, 600), text='Rejouer', size=(200, 75), name='replay')
        text = Sprite(Fonts.GO.render('Vous avez perdu !', Colors.BLACK, False), (635, 550))

        self.add(replay, text)

class Grid(pygame.sprite.Group):
    def __init__(self, size: int, bombes: int):
        super().__init__()
        self.bombes = bombes
        self.flags = 0
        self.size = size
        self.finished = False
        self.exploded = False
        self.started = False
        self.bombes_list = []
        self.time = 0

        self.grid = []
        y, yi = 0, 0
        while y < Globals.GRID_WIDTH_OR_HEIGHT:
            self.grid.append([])
            x, xi = 0, 0
            while x < Globals.GRID_WIDTH_OR_HEIGHT:
                img = image('cell-covered', size=(Globals.CASE_SIZE, Globals.CASE_SIZE))
                self.grid[yi].append(Case(img, (10 + x, 90 + y), (xi, yi), self))
                x += Globals.CASE_SIZE
                xi += 1
            y += Globals.CASE_SIZE
            yi += 1

    def start(self, x: int, y: int):
        self.started = True
        self.time = time.time()
        rnd_grid = [[random.random() for _ in range(self.size)] for _ in range(self.size)]
        Globals.menus[1].sprites()[6].image = Fonts.TITLE.render(str(self.bombes - self.flags), True, Colors.BLACK)

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
        for row in self.grid:
            for case in row:
                if not (case.is_bombe or case.is_discovered):
                    return False
        return True

    def count_near_bombes(self, x, y):
        voisins_bombes = 0
        for i in range(3):
            for j in range(3):
                if self.size >= y + i and 0 <= y + i - 1 and self.size >= x + j and 0 <= x + j - 1:
                    voisins_bombes += int(self.grid[y + (i - 1)][x + (j - 1)].is_bombe)  # Ajoute 1 si bombe, sinon 0
        return voisins_bombes

    def count_near_flags(self, x, y):
        voisins_flags = 0
        for i in range(3):
            for j in range(3):
                if self.size >= y + i and 0 <= y + i - 1 and self.size >= x + j and 0 <= x + j - 1:
                    voisins_flags += int(self.grid[y + (i - 1)][x + (j - 1)].is_flag)  # Ajoute 1 si bombe, sinon 0
        return voisins_flags

    def case_press(self, x, y, bymachine=False):
        if 0 <= x < Globals.GRID_SIZE and 0 <= y < Globals.GRID_SIZE and not self.is_finished():
            case: Case = self.grid[y][x]
            if not self.started:
                self.start(x, y)  # placer les bombes sur le terrain
            if case.is_flag and not bymachine:
                # print("Enlever le drapeau avant de découvrir la case")
                return
            if case.is_discovered and not bymachine:
                if case.nb_bombes == self.count_near_flags(x, y):
                    for i in range(3):
                        for j in range(3):
                            if self.size >= y + i and 0 <= y + i - 1 and self.size >= x + j and 0 <= x + j - 1 and not self.grid[y + (i - 1)][x + (j - 1)].is_flag:
                                self.case_press(x + (j - 1), y + (i - 1), bymachine=True)
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
            elif not self.finished:
                # case.is_discovered = True
                nb_bombes = self.count_near_bombes(x, y)
                case.nb_bombes = nb_bombes
                case.image = Images.getCell(nb_bombes)
                if nb_bombes == 0:
                    self.flood_fill(x, y)
                else:
                    self.grid[y][x].is_discovered = True
            if self.is_finished():
                for bombe in self.bombes_list:
                    self.grid[bombe[1]][bombe[0]].image = Images.getMine()

    def case_press_flag(self, x, y):
        if 0 <= x < Globals.GRID_SIZE and 0 <= y < Globals.GRID_SIZE and not self.is_finished() and not self.finished and self.started:
            case = self.grid[y][x]
            if case.is_flag:
                self.flags -= 1
                case.is_flag = False
                case.image = Images.getCovered()
            elif not case.is_discovered:
                self.flags += 1
                case.is_flag = True
                case.image = Images.getFlagged()
            else: return
            Globals.menus[1].sprites()[6].image = Fonts.TITLE.render(str(self.bombes - self.flags), True, Colors.BLACK)

    def inside(self, x, y):
        return 0 <= y < self.size and 0 <= x < self.size

    def flood_fill(self, x, y):
        """
        Flood-fill (node):
          1. Set Q to the empty queue or stack.
          2. Add node to the end of Q.
          3. While Q is not empty:
          4.   Set n equal to the first element of Q.
          5.   Remove first element from Q.
          6.   If n is Inside:
                 Set the n
                 Add the node to the west of n to the end of Q.
                 Add the node to the east of n to the end of Q.
                 Add the node to the north of n to the end of Q.
                 Add the node to the south of n to the end of Q.
          7. Continue looping until Q is exhausted.
          8. Return.
        """
        Q = []  # Queue
        Q.append((x, y))
        while len(Q) != 0:
            x, y = Q.pop(0)
            case = self.grid[y][x]
            if self.inside(x, y) and not case.is_discovered:
                case.is_discovered = True
                nb_bombes = self.count_near_bombes(x, y)
                case.nb_bombes = nb_bombes
                case.image = Images.getCell(nb_bombes)
                if nb_bombes == 0:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if not (j == 0 and i == 0):
                                if self.inside(x + i, y + j) and (not self.grid[y + j][x + i].is_discovered):
                                    Q.append((x + i, y + j))
        return

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
    screen = pygame.display.set_mode(Globals.ISIZE)
    Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)

    menus = [MainMenu(), GameMenu(), ChallengeMenu(), CreationMenu(), LeaderboardMenu(), WinMenu(), GameOverMenu()]
    Globals.menus = menus
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
                    if not Globals.GRID.is_finished() and not Globals.GRID.finished:
                        x, y = int((xPos - 10) / Globals.CASE_SIZE), int((yPos - 90) / Globals.CASE_SIZE)
                        if click[0]:
                            Globals.GRID.case_press(x, y)
                        elif click[2]:
                            Globals.GRID.case_press_flag(x, y)
                    elif (Globals.GRID.is_finished() and menus[-1].sprites()[0].rect.collidepoint(xPos, yPos) and click[0]) or (Globals.GRID.finished and menus[-2].sprites()[0].rect.collidepoint(xPos, yPos) and click[0]):
                        Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                for sprite in menus[Globals.menu].sprites():
                    if isinstance(sprite, Button) and sprite.rect.collidepoint(xPos, yPos) and click[0]:
                        sprite: Button
                        if sprite.text == 'Quitter':
                            Globals.run = False
                        if sprite.text == 'Jouer':
                            Globals.menu = 3
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                        if sprite.text == 'Challenges':
                            Globals.menu = 2
                        if sprite.text == 'Leaderboard':
                            Globals.menu = 4
                        if sprite.text == 'Retour':
                            Globals.menu = 0
                        if sprite.text == 'Facile':
                            Globals.GRID_SIZE = 10
                            Globals.BOMBES = 15
                            Globals.CASE_SIZE = Globals.GRID_WIDTH_OR_HEIGHT / Globals.GRID_SIZE
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                            Globals.menu = 1
                        if sprite.text == 'Normal':
                            Globals.GRID_SIZE = 20
                            Globals.BOMBES = 60
                            Globals.CASE_SIZE = Globals.GRID_WIDTH_OR_HEIGHT / Globals.GRID_SIZE
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                            Globals.menu = 1
                        if sprite.text == 'Difficile':
                            Globals.GRID_SIZE = 30
                            Globals.BOMBES = 150
                            Globals.CASE_SIZE = Globals.GRID_WIDTH_OR_HEIGHT / Globals.GRID_SIZE
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                            Globals.menu = 1
                        if sprite.text == 'Impossible':
                            Globals.GRID_SIZE = 40
                            Globals.BOMBES = 300
                            Globals.CASE_SIZE = Globals.GRID_WIDTH_OR_HEIGHT / Globals.GRID_SIZE
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                            Globals.menu = 1
                        if sprite.name == 'addMine':
                            if Globals.BOMBES < Globals.GRID_SIZE ** 2 // 2:
                                Globals.BOMBES += 1
                                menus[3].sprites()[7].image = Fonts.BUTTON.render(str(Globals.BOMBES), Colors.BLACK, False)
                        if sprite.name == 'remMine':
                            if Globals.BOMBES > 1:
                                Globals.BOMBES -= 1
                                menus[3].sprites()[7].image = Fonts.BUTTON.render(str(Globals.BOMBES), Colors.BLACK, False)
                        if sprite.name == 'addSize':
                            if Globals.GRID_SIZE < 100:
                                Globals.GRID_SIZE += 1
                                menus[3].sprites()[8].image = Fonts.BUTTON.render(str(Globals.GRID_SIZE), Colors.BLACK, False)
                        if sprite.name == 'remSize':
                            if Globals.GRID_SIZE > 5:
                                Globals.GRID_SIZE -= 1
                                menus[3].sprites()[8].image = Fonts.BUTTON.render(str(Globals.GRID_SIZE), Colors.BLACK, False)
                        if sprite.name == 'create':
                            Globals.CASE_SIZE = Globals.GRID_WIDTH_OR_HEIGHT / Globals.GRID_SIZE
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)
                            Globals.menu = 1
                        if sprite.name == 'replay':
                            Globals.GRID = Grid(Globals.GRID_SIZE, Globals.BOMBES)

        if Globals.menu == 1 and Globals.GRID.started and not Globals.GRID.finished and not Globals.GRID.is_finished():
            t = round(time.time() - Globals.GRID.time)
            s = ('0' + str(t // 60))[-2:] + ':' + ('0' + str(t % 60))[-2:]
            menus[1].sprites()[5].image = Fonts.TITLE.render(s, Colors.BLACK, False)

        screen.fill(menus[Globals.menu].bg)

        menus[Globals.menu].draw(screen)
        if Globals.menu == 1:
            Globals.GRID.draw(screen)
            if Globals.GRID.is_finished():
                menus[-2].draw(screen)
            if Globals.GRID.finished:
                menus[-1].draw(screen)

        pygame.display.flip()
        pygame.time.wait(1000 // Globals.FPS)


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
        Globals.CASE_SIZE = Globals.GRID_WIDTH_OR_HEIGHT / Globals.GRID_SIZE
        Globals.BOMBES = int(argv[1])
    elif 1 <= len(argv):
        print("[-] Usage: python main.py [--help] [--debug] [[GRID_SIZE] [nb_de_bombes]]")
        print(f"\t\\Default: Size={Globals.GRID_SIZE}, bombes={Globals.BOMBES}")
    main()
