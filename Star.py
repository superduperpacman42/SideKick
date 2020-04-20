import pygame
from Constants import *

class Star:

    def __init__(self, game, pos, size=[6, 6]):
        self.game = game
        self.size = size
        self.pos = pos
        # self.progress = 0
    
    def update(self, dt):
        if self.game.state == 1:
            self.pos[0] += dt*SPEED/4
        pos = [self.pos[0]-self.game.x, self.pos[1]]
        pygame.draw.rect(self.game.screen, (255,255,200), pygame.Rect(pos,self.size))