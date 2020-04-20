import pygame
from Constants import *

class Canvas:

    def __init__(self, game, image, pos=[0,0], size=[WIDTH, HEIGHT]):
        self.game = game
        self.image = image
        self.size = size
        self.pos = pos
        self.image = game.loadImage(image+".png",scale=1)
        # self.progress = 0
    
    def update(self, dt):
        if self.game.state == 1:
            self.pos[0] += dt*SPEED/4
        pos = [self.pos[0]-self.game.x, self.pos[1]]
        self.game.screen.blit(self.image, pos)