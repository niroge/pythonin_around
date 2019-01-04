#!/usr/bin/env python3

# PythoningAround - snake simulator
# Copyright (C) 2018   <robert@battlestation>
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the
# sale, use or other dealings in this Software without prior written
# authorization.

# including the libraries...
import sys
import pygame
import _thread
import argparse
from time import sleep
from random import randrange

MAX_X = 34
MAX_Y = 23

# x * y = 782
# occupied x + y -> 68 + 42 -> 110 // x * 2 + y * 2 - 4
PIXEL_COLOR = (0xff, 0xff, 0xff)

DISPLAY_GAME = 1
DISPLAY_GAME_OVER = 2
DISPLAY_RESOLUTION = (640, 480)

difficulties = {
    'easy': 0.5,
    'normal': 0.2,
    'hardcore': 0.1,
    'extreme': 0.05,
}

# creating the objects
class GraphicsSubsystem:
    '''This subsystem manages the game's display'''
    def __init__(self, window):
        self.max_x = MAX_X
        self.max_y = MAX_Y
        self.pixel_size = 18
        
        self.display = window
        
        self.pixel_separator = 1
        self.current_display = DISPLAY_GAME
        self.pixel_color = PIXEL_COLOR
        self.food_color = (0xff, 0x00, 0x00)
        self.snake_color = (0x00, 0xff, 0x00)
        self.background_color = (0x10, 0x10, 0x10)

    def refresh_screen(self, snake_pos=[[0, 0]], fruit_pos=[1, 1]):
        try:
            self.display.fill(self.background_color)
            if self.current_display == DISPLAY_GAME:
                for x in range(self.max_x):
                    # draw the top separator
                    self.draw_pixel(x, 0)
                
                    # draw the bottom separator
                    self.draw_pixel(x, self.max_y - 1)

                for y in range(self.max_y):
                    # draw the left separator
                    self.draw_pixel(0, y)

                    # draw the right separator
                    self.draw_pixel(self.max_x, y)

                # print the snake and the fruit
                self.draw_pixel(fruit_pos[0], fruit_pos[1], self.food_color)
                
                for cell in snake_pos:
                    self.draw_pixel(cell[0], cell[1], self.snake_color)

            elif self.current_display == DISPLAY_GAME_OVER:
                green = self.snake_color
                if options['hacker_wars']:
                    # C++
                    for i in range(3, 6):
                        self.draw_pixel(i, 1, green)
                        self.draw_pixel(i, 7, green)
                    self.draw_pixel(6, 2, green)

                    for i in range(2, 7):
                        self.draw_pixel(2, i, green)

                    self.draw_pixel(6, 6, green)
                    for j in range(2):
                        for i in range(5):
                            self.draw_pixel(j * 6 + 8 + i, 4, green)
                            self.draw_pixel(j * 6 + 10, 2 + i, green)

                    # <
                    order = False
                    num = 17
                    for i in range(10, 15):
                        self.draw_pixel(num, i, green)
                        if order:
                            num += 1
                        else:
                            num -= 1
                        if num == 15:
                            order = True

                    del num
                    del order

                    # Python
                    # P
                    for i in range(18, 25):
                        self.draw_pixel(2, i, green)

                    for i in range(3, 6):
                        self.draw_pixel(i, 18, green)
                        self.draw_pixel(i, 21, green)

                    self.draw_pixel(6, 19, green)
                    self.draw_pixel(6, 20, green)

                    #Y
                    order = False
                    num = 18
                    for i in range(9, 14):
                        self.draw_pixel(i, num, green)
                        if order:
                            num -= 1
                        else:
                            num += 1
                        if num == 20:
                            order = True
                    del order
                    del num
                    for i in range(20, 25):
                        self.draw_pixel(11, i, green)

                    #T
                    for i in range(16, 21):
                        self.draw_pixel(i, 18, green)

                    for i in range(19, 25):
                        self.draw_pixel(18, i, green)

                    for i in range(0, 12, 4):
                        self.draw_pixel(i + 23, 23, green)
                        self.draw_pixel(i + 23, 24, green)
                        self.draw_pixel(i + 24, 23, green)
                        self.draw_pixel(i + 24, 24, green)
                
                else:
                    tmp = pygame.font.SysFont('Hack', 110)
                    msg = tmp.render('GAME OVER', True, (0x00, 0xff, 0x00))
                    self.display.blit(msg, (20, 140))
                    tmp = pygame.font.SysFont('Hack', 22)
                    msg = tmp.render('Press Q or ESCAPE to exit', True, (0x00, 0xff, 0x00))
                    self.display.blit(msg, (150, 280))
                    del tmp
                    del msg

            pygame.display.flip()

        except:
            sleep(1)
            exit(0)

    def draw_pixel(self, x, y, color=PIXEL_COLOR):
        pygame.draw.rect(self.display, color, pygame.Rect(self.pixel_separator + x * self.pixel_size, self.pixel_separator + y * self.pixel_size, self.pixel_size-self.pixel_separator, self.pixel_size-self.pixel_separator), 0)

        
class AudioSubsystem:
    '''This subsystem manages the audio of the game, including music'''
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('pythoning_around.mp3')
        pygame.mixer.music.play(-1)


class InputSubsystem:
    '''Manages the input from STDIN'''
    def __init__(self):
        self.end_session = False               # to change when program closes
        self.current_direction = pygame.K_RIGHT # by default go right
        self.last_direction = pygame.K_RIGHT
        self.current_char = ''
        _thread.start_new_thread(self.loop_input, ())

    def loop_input(self):
        while not self.end_session:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # self.current_char = event.key
                    # if event.key == pygame.K_UP and self.last_direction != pygame.K_DOWN:
                    #     self.current_direction = pygame.K_UP
                    # if event.key == pygame.K_DOWN and self.last_direction != pygame.K_UP:
                    #     self.current_direction = pygame.K_DOWN
                    # if event.key == pygame.K_LEFT and self.last_direction != pygame.K_RIGHT:
                    #     self.current_direction = pygame.K_LEFT
                    # if event.key == pygame.K_RIGHT and self.last_direction != pygame.K_LEFT:
                    #     self.current_direction = pygame.K_RIGHT

                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        self.end_session = True

                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        self.current_direction = event.key
                elif event.type == pygame.QUIT:
                    self.end_session = True

        pygame.quit()
        quit(0)

        
class UpdateSubsystem:
    '''This subsystem manages the entire game every tick'''
    def __init__(self, window):
        self.graphics = GraphicsSubsystem(window)
        if options['endgame']:
            print('endgame')
            self.graphics.current_display = DISPLAY_GAME_OVER
        else:
            self.graphics.current_display = DISPLAY_GAME
        #audio = AudioSubsystem()
        self.input_system = InputSubsystem()
        self.snake = [[15, 8], [16, 8]]
        self.food_pos = [17, 3]
        self.main_loop()

    def main_loop(self):
        while not self.player_lost():
            self.graphics.refresh_screen(self.snake, self.food_pos)
            sleep(difficulties[options['difficulty']])
            self.update_snake()

        self.graphics.current_display = DISPLAY_GAME_OVER
        while self.input_system.current_char != pygame.K_q and self.input_system.current_char != pygame.K_ESCAPE:
            self.graphics.refresh_screen()
        
        self.input_system.end_session = True
        sleep(0.5)

    def update_snake(self):
        eated = False
        if self.snake[-1] == self.food_pos:
            eated = True
            while self.food_pos in self.snake:
                self.food_pos = randrange((MAX_X + MAX_Y) * 2 - 4)
                self.food_pos = [(self.food_pos % MAX_X), int(self.food_pos / MAX_X) + 1]
                if self.food_pos[0] == 0:
                    self.food_pos[0] = 1
                if self.food_pos[1] == 0:
                    self.food_pos[1] = 1
                
        self.snake.append(self.snake[-1][:])
        if not eated:
            self.snake.pop(0)
        
        if self.input_system.current_direction == pygame.K_UP:
            self.snake[-1][1] -= 1

        elif self.input_system.current_direction == pygame.K_DOWN:
            self.snake[-1][1] += 1

        elif self.input_system.current_direction == pygame.K_LEFT:
            self.snake[-1][0] -= 1

        else:
            self.snake[-1][0] += 1

        self.input_system.last_direction = self.input_system.current_direction

    def player_lost(self,):
        for part in self.snake:
            if self.snake.count(part) != 1:
                return True

            if part[0] <= 0 or part[0] >= MAX_X or part[1] <= 0 or part[1] >= MAX_Y - 1:
                return True

        return False



# check command line arguments
parser = argparse.ArgumentParser(description='Retro Snake for the Open Day', epilog='Difficulties are: easy, normal, hardcore and extreme')
parser.add_argument('--endgame', '-e', help='Show the GAME OVER screen', action='store_true', default=False)
parser.add_argument('--hacker-wars', '-w', help='Print the alternative GAME OVER screen', action='store_true', default=False)
parser.add_argument('--difficulty', '-d', help='How difficult the game should be', action='store', default='easy', type=str)
options = parser.parse_args(sys.argv[1:]).__dict__
if options['difficulty'].lower() not in difficulties:
    print('[X] Difficulties: easy medium hardcore extreme')
    sys.exit(1)

# configure pygame
pygame.init()
window = pygame.display.set_mode(DISPLAY_RESOLUTION)
pygame.display.set_caption('Pythonin\' Around')

# launch the game
run = UpdateSubsystem(window)
