import pygame
from Constants import *

class Crook:

    def __init__(self, game, pos, v=-SPEED/2, size=PLAYER_SIZE):
        self.game = game
        self.walkImages = game.loadImage("Crook.png",4)
        self.jumpImage = game.loadImage("Crook0.png",)
        self.punchImage = game.loadImage("CrookPunch.png",)
        self.dieImages = game.loadImage("CrookDeath.png",2)
        self.dead = False
        self.pos = pos[:]
        self.punching = 0
        self.size = size
        self.state = 0 # 0 = stand, 1 = walk, 2 = jump
        self.right = 1
        if v<0:
            self.right = 0
        self.v = v
        self.jump = 0
        self.progress = 0
        self.game.playSound("Cackle.wav")
    
    def update(self, dt):
        if not self.dead:
            if self.state == 0:
                self.state = 1
            if self.punching <= 0:
                self.pos[0] += self.v*SPEED*dt
        pos = [self.pos[0]-self.size[0]/2, self.pos[1]-self.size[1]/2]
        pos[0] += -self.game.x
        if self.state == 0 and not self.dead:
            self.progress = 0
        img = self.walkImages[int(self.progress)%len(self.walkImages)]
        if self.state == 2:
            img = self.jumpImage
            self.progress = 0
        if self.state == 1 or self.dead:
            self.progress += dt/120
            if self.dead:
                img = self.dieImages[min(int(self.progress), len(self.dieImages)-1)]
                pos[1] += 4*PIXEL_RATIO
            elif self.progress >= len(self.walkImages):
                self.progress = 0
        if self.punching > 0 and not self.dead:
            self.punching -= dt/240
            img = self.punchImage
        if not self.right:
            img = pygame.transform.flip(img, 1, 0)
        self.game.screen.blit(img, pos)

    def hit(self, pos, size):
        ''' Detect collisions with person '''
        if self.dead:
            return False
        if pos[0]-size[0]/2>self.pos[0]+self.size[0]/2 or pos[0]+size[0]/2<self.pos[0]-self.size[0]/2:
            return False
        if pos[1]-size[1]/2>self.pos[1]+self.size[1]/2 or pos[1]+size[1]/2<self.pos[1]-self.size[1]/2:
            return False
        return True

    def die(self, top):
        if not self.dead:
            self.progress = 0
        self.state = 1
        self.v = -1
        self.dead = True
        self.game.score += 500
        self.game.counts[2] += 1

    def success(self):
        self.punching = 1
        self.game.playSound("VillainPunch.wav")