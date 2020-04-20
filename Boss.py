import pygame
from Constants import *

class Boss:

    def __init__(self, game, v=-1, size=(100*PIXEL_RATIO,162*PIXEL_RATIO)):
        self.game = game
        self.size = size
        self.dead = False
        self.v = v
        self.image = game.loadImage("ProfessorPurple.png", 8)
        self.shieldImage = game.loadImage("Shield.png",)
        self.deadImage = game.loadImage("AlienDead.png")
        self.progress = 0
        self.state = 0
        self.pos = [self.game.x + WIDTH + SCALE*10, HEIGHT-self.size[1]-SCALE/2]
        self.game.playSound("Cackle.wav")
        self.shield = 0
    
    def update(self, dt):
        if self.pos[0] < self.game.x + WIDTH - self.size[0] or self.state > 0:
            if self.game.x / (SCALE*1000) - BOSS_H > 0.12:
                self.state = 1
            else:
               self.state = 0.5
            self.pos[0] += SPEED*dt/2
        pos = [self.pos[0]-self.game.x, self.pos[1]]
        if self.shield > 0:
            self.shield -= dt/120
            self.game.screen.blit(self.shieldImage, [pos[0]-40*PIXEL_RATIO, pos[1]-18*PIXEL_RATIO])
            if self.shield < 0:
                self.shield = 0
        if self.dead:
            self.game.screen.blit(self.deadImage, pos)
            self.progress += dt/120
            if self.progress >= 1:
                self.game.enemies.remove(self)
        else:
            img = self.image[int(self.progress)%len(self.image)]
            self.game.screen.blit(img, pos)
            if self.state != 0:
                self.progress += dt/120
            if self.progress >= len(self.image):
                self.progress = 0

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
        self.pos[1] -= 5*PIXEL_RATIO
        self.progress = 0
        self.v = -1
        self.game.score += 10000
        self.game.state = 3
        self.game.finalscore = self.game.score
        self.game.finalcounts = self.game.counts[:]
        self.game.playSound("Boom.wav")

    def success(self):
        pass