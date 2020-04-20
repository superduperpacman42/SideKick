import pygame
from Constants import *

class Alien:

    def __init__(self, game, building, v=-1, size=(100*PIXEL_RATIO,31*PIXEL_RATIO)):
        self.game = game
        self.size = size
        self.dead = False
        self.v = v
        self.building = building
        self.image = game.loadImage("Alien.png")
        self.deadImage = game.loadImage("AlienDead.png")
        self.tractorImage = game.loadImage("Tractor.png")
        self.flickerImage = game.loadImage("TractorFlicker.png")
        self.progress = 0
        self.lock = False
        self.state = 0
        self.pos = [building.pos[0]+building.size[0]/2-size[0]/2, -SCALE*5]
        self.game.playSound("AlienEnter.wav")
    
    def update(self, dt):
        pos = [self.pos[0]-self.game.x, self.pos[1]]
        if not self.dead:
            if self.state==0 and self.building.pos[1] - self.pos[1] > SCALE*10:
                self.pos[1] += SPEED*dt/2
            elif self.state==0:
                self.state = 1
                self.game.playSound("TractorBeamStart.wav")
            if self.state == 2:
                self.pos[1] -= SPEED*dt/2
        if self.dead:
            self.game.screen.blit(self.deadImage, pos)
            self.progress += dt/120
            if self.progress >= 1:
                self.game.enemies.remove(self)
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

    def tractor(self, dt):
        if self.state==1 and not self.dead:
            pos = [self.pos[0]-self.game.x, self.pos[1]]
            self.progress += dt/480
            if self.progress >= 1:
                self.game.screen.blit(self.flickerImage, pos)
                if self.progress >= 1.2:
                    self.progress = 0
            else:
                self.game.screen.blit(self.tractorImage, pos)
        sk = self.game.sidekick
        if sk.platform == self.building and not self.dead:
            if abs(self.pos[0]+self.size[0]/2 - sk.pos[0]) < .2*SCALE:
                if not self.lock:
                    self.game.playSound("TractorBeam.wav")
                self.lock = self.game.sidekick
                self.lock.captured = True
        if self.lock:
            self.lock.pos[1] -= .3*SPEED*dt


    def die(self, top):
        self.dead = True
        self.pos[1] -= 15*PIXEL_RATIO
        self.progress = 0
        self.v = -1
        self.game.score += 1000
        self.game.counts[3] += 1
        self.game.playSound("Boom.wav")
        if self.lock:
            self.lock.captured = False
            self.lock = None

    def success(self):
        self.state = 2
        self.game.playSound("Lose.wav")