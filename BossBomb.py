import pygame
from Constants import *
import random

class BossBomb:

    def __init__(self, game, pos, building, blue=False, size=(35*PIXEL_RATIO,32*PIXEL_RATIO)):
        self.game = game
        self.size = size
        self.progress = 0
        self.v = 0
        self.building = building
        self.ground = random.random() < 0.3
        self.state = 0 # 0 = fused, 1 = defused, 2 = boom
        self.blue = blue
        self.arc = 1
        if blue:
            self.image0 = game.loadImage("BlueBomb.png",2)
            self.image1 = game.loadImage("BlueBombDefused.png")
        else:
            self.image0 = game.loadImage("RedBomb.png",2)
            self.image1 = game.loadImage("RedBombDefused.png")
        self.image2 = game.loadImage("Boom.png",)
        self.pos = pos
        self.game.playSound("BombBeep.wav")
    
    def update(self, dt):
        if self.game.bossSprite.dead:
            self.state = 1
        if self.pos[0] < self.building.pos[0]+self.building.size[0]/2-self.size[0]/2:
            self.pos[0] += SPEED*dt/2
        else:
            if self.arc <= 1:
                self.arc -= dt/600
                self.pos[1] -= SPEED*self.arc*dt
            if self.arc < 0:
                if self.ground:
                    if self.pos[1] > HEIGHT-SCALE-self.size[1]:
                        self.pos[1] = HEIGHT-SCALE-self.size[1]
                        self.arc = 2
                elif self.pos[1] > self.building.pos[1]-self.size[1]:
                    self.pos[1] = self.building.pos[1]-self.size[1]
                    self.arc = 2
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
            self.game.screen.blit(self.image2, pos)  
            if self.progress >= 1:
                self.game.enemies.remove(self)

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
        self.game.playSound("Snip.wav")

    def success(self):
        self.state = 2
        self.progress = 0
        self.game.playSound("Boom.wav")