import game
import pygame
import random

from pygame.locals import *


def drawText(surface, text, font, color, x, y):
    """Helper function used in many of the classes, to draw text on a
    surface"""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.x = x
    textrect.centery = y
    surface.blit(textobj, textrect)


class Word(object):

    """A moving word on the screen. Keeps track of the position and the word"""

    def __init__(self, x, y, word, max_y):
        super(Word, self).__init__()
        self.x = x
        self.y = y
        self.max_y = max_y

        self.word = word
        self.font = pygame.font.SysFont(None, 24)

        self.alive = True

    def update(self):
        self.y += 0.2

        if self.y > self.max_y:
            self.alive = False

    def test_word(self, input):
        if self.word in input:
            self.alive = False
            return 1
        else:
            return 0

    def draw(self, surf):
        drawText(surf, self.word, self.font,
                 pygame.Color('red'), self.x, self.y)


class MovingWords(game.Game):

    """Type the moving words to destroy them."""

    def __init__(self):
        super(MovingWords, self).__init__()

        self.word_list = []
        self.moving_words_list = []
        self.load_words()

        # frames til next word spawns
        self.spawn_time = 150
        self.min_time = 140
        self.spawn_timer = 149

        # only keep track of the last x chars
        self.input = []
        self.max_input_size = 20

    def evnt_hndlr(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.input.append('a')
            if event.key == K_b:
                self.input.append('b')
            if event.key == K_c:
                self.input.append('c')
            if event.key == K_d:
                self.input.append('d')
            if event.key == K_e:
                self.input.append('e')
            if event.key == K_f:
                self.input.append('f')
            if event.key == K_g:
                self.input.append('g')
            if event.key == K_h:
                self.input.append('h')
            if event.key == K_i:
                self.input.append('i')
            if event.key == K_j:
                self.input.append('j')
            if event.key == K_k:
                self.input.append('k')
            if event.key == K_l:
                self.input.append('l')
            if event.key == K_m:
                self.input.append('m')
            if event.key == K_n:
                self.input.append('n')
            if event.key == K_o:
                self.input.append('o')
            if event.key == K_p:
                self.input.append('p')
            if event.key == K_q:
                self.input.append('q')
            if event.key == K_r:
                self.input.append('r')
            if event.key == K_s:
                self.input.append('s')
            if event.key == K_t:
                self.input.append('t')
            if event.key == K_u:
                self.input.append('u')
            if event.key == K_v:
                self.input.append('v')
            if event.key == K_w:
                self.input.append('w')
            if event.key == K_x:
                self.input.append('x')
            if event.key == K_y:
                self.input.append('z')
            if event.key == K_z:
                self.input.append('y')
            if event.key == 39:
                self.input.append('ä')
            if event.key == 59:
                self.input.append('ö')
            if event.key == 91:
                self.input.append('ü')

    def update(self, delta):
        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_time:
            self.spawn_timer = 0

            if self.spawn_time > self.min_time:
                self.spawn_time -= 5

            word = Word(random.randrange(self.WINDOWHEIGHT),
                        50,
                        random.choice(self.word_list),
                        self.WINDOWWIDTH)
            self.moving_words_list.append(word)

        if len(self.input) > self.max_input_size:
            self.input = self.input[-self.max_input_size:]

        test_word = ''.join(self.input)

        # update all word objects
        for mwl in self.moving_words_list:
            mwl.test_word(test_word)
            mwl.update()

        # Filter out dead word objects
        self.moving_words_list = [x for x in self.moving_words_list if x.alive]

    def draw(self, surf):
        for mwl in self.moving_words_list:
            mwl.draw(surf)

    def load_words(self):
        file_name = 'german.dic'
        with open(file_name, 'r') as f:
            for line in f:
                if "'" not in line:
                    self.word_list.append(line.lower().strip())

if __name__ == '__main__':
    mw = MovingWords()
    mw.run()
