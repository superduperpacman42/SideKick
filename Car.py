import pygame
from Constants import *

class Car:

    def __init__(self, game, x, v, size=(53*PIXEL_RATIO,31*PIXEL_RATIO)):
        self.game = game
        self.size = size
        self.dead = False
        self.v = v
        self.image = game.loadImage("Taxi.png")
        self.flashImage = game.loadImage("TaxiFlash.png")
        self.deadImage = game.loadImage("DeadTaxi.png")
        self.deadImageTop = game.loadImage("DeadTaxiTop.png")
        self.progress = 0
        # self.game.playSound("Horn.wav")
        if v>0:
            self.pos = [x-100-size[0], HEIGHT-SCALE-size[1]+PIXEL_RATIO*2]
        else:
            self.pos = [x+WIDTH+100, HEIGHT-SCALE-size[1]+PIXEL_RATIO*2]
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.flashImage = pygame.transform.flip(self.flashImage, 1, 0)
            self.deadImage = pygame.transform.flip(self.deadImage, 1, 0)
            self.deadImageTop = pygame.transform.flip(self.deadImageTop, 1, 0)
    
    def update(self, dt):
        if not self.dead:
            self.pos[0] += self.v*SPEED*dt
        pos = [self.pos[0]-self.game.x, self.pos[1]]
        if self.dead:
            if self.top:
                self.game.screen.blit(self.deadImageTop, pos)
            else:
                self.game.screen.blit(self.deadImage, pos)                
        else:
            self.progress += dt/480
            if self.progress >= 1:
                self.game.screen.blit(self.flashImage, pos)
                if self.progress >= 1.2:
                    self.progress = 0
            else:
                self.game.screen.blit(self.image, pos)

    def hit(self, pos, size):
        ''' Detect collisions with person '''
        if self.dead:
            return False
        if pos[0]-size[0]/2>self.pos[0]+self.size[0] or pos[0]+size[0]/2<self.pos[0]:
            return False
        if pos[1]-size[1]/2>self.pos[1]+self.size[1] or pos[1]+size[1]/2<self.pos[1]:
            return False
        return True

    def die(self, top):
        self.dead = True
        self.v = -1
        self.top = top
        self.game.score += 100
        self.game.counts[0] += 1

    def success(self):
        self.game.playSound("Crunch.wav")
        pass