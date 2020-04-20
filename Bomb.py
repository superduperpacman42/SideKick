import pygame
from Constants import *

class Bomb:

    def __init__(self, game, pos, size=(40*PIXEL_RATIO,40*PIXEL_RATIO)):
        self.game = game
        self.size = size
        self.progress = 0
        self.v = 0
        self.state = 0 # 0 = fused, 1 = defused, 2 = boom
        self.image0 = game.loadImage("BombFused.png",4)
        self.image1 = game.loadImage("BombDefused.png")
        self.image2 = game.loadImage("Bomb.png",2)
        self.pos = pos
        self.game.playSound("BombBeep.wav")
    
    def update(self, dt):
        pos = [self.pos[0]-self.game.x, self.pos[1]]
        if self.state == 0:
            self.progress += dt/120
            img = self.image0[min(int(self.progress), len(self.image0)-1)]
            self.game.screen.blit(img, pos)
            if self.progress >= len(self.image0):
                self.progress = 0
        elif self.state == 1:
            self.game.screen.blit(self.image1, pos)
        elif self.state == 2:
            self.progress += dt/240
            img = self.image2[min(int(self.progress), len(self.image2)-1)]
            self.game.screen.blit(img, pos)  

    def hit(self, pos, size):
        ''' Detect collisions with person '''
        if self.state != 0:
            return False
        if pos[0]-size[0]/2>self.pos[0]+self.size[0] or pos[0]+size[0]/2<self.pos[0]:
            return False
        if pos[1]-size[1]/2>self.pos[1]+self.size[1] or pos[1]+size[1]/2<self.pos[1]:
            return False
        return True

    def die(self, top):
        self.state = 1
        self.progress = 0
        self.game.score += 200
        self.game.counts[1] += 1
        self.game.playSound("Snip.wav")

    def success(self):
        self.state = 2
        self.progress = 0
        self.game.playSound("Boom.wav")