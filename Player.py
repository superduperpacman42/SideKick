import pygame
from Constants import *
from Canvas import Canvas

class Player:

    def __init__(self, game, pos=[WIDTH/2-33,HEIGHT-SCALE*4.5], size=PLAYER_SIZE, sidekick=False):
        self.game = game
        self.walkImages = game.loadImage("Hero.png",4)
        self.jumpImage = game.loadImage("HeroJump.png",2)
        self.fallImage = game.loadImage("HeroFly.png",)
        self.punchImage = game.loadImage("HeroPunch.png",)
        self.punchUpImage = game.loadImage("HeroPunchUp.png",)
        self.punchDownImage = game.loadImage("HeroPunchDown.png",)
        self.dead = False
        self.platform = None
        self.stun = 0
        self.stunDirection = 1
        self.punching = 0
        self.punchState = 0
        self.captured = False
        self.pos = pos[:]
        if sidekick:
            self.walkImages = game.loadImage("Side.png",4)
            self.jumpImage = game.loadImage("SideJump.png",2)
            self.fallImage = game.loadImage("SideFall.png",)
            self.dieImages = game.loadImage("SideDeath.png",2)
            self.punchImage = game.loadImage("SidePunch.png",)
        else:
            self.pos[0]+=65
        self.size = size
        self.state = 0 # 0 = stand, 1 = walk, 2 = jump
        self.right = 1
        self.jump = 0
        self.progress = 0
    
    def update(self, dt):
        if self.stun > 0:
            self.stun -= dt/120
            self.pos[0] -= dt*SPEED*self.stun*4*self.stunDirection
            if self.stun <= 0:
                self.stun = 0
        pos = [self.pos[0]-self.size[0]/2, self.pos[1]-self.size[1]/2]
        pos[0] += -self.game.x
        if self.state == 0:
            self.progress = 0
        img = self.walkImages[int(self.progress)%len(self.walkImages)]
        if self.state == 2:
            if 2*JUMP_SPEED*self.jump/JUMP > FALL_SPEED:
                img = self.jumpImage[int(self.progress)%len(self.jumpImage)]
            else:
                img = self.fallImage
            self.progress += dt/60
            if self.progress >= len(self.jumpImage):
                self.progress = 0
        if self.state == 1 or self.dead:
            self.progress += dt/120
            if self.dead:
                img = self.dieImages[min(int(self.progress), len(self.dieImages)-1)]
                pos[1] += 4*PIXEL_RATIO
            elif self.progress >= len(self.walkImages):
                self.progress = 0
        if self.punching > 0:
            self.punching -= dt/240
            if self.punchState == 2:
                if self.jump > 0:
                    img = self.punchUpImage
                else:
                    img = self.punchDownImage
            else:
                img = self.punchImage
            if self.punching < 0:
                self.punching = 0
        if not self.right:
            img = pygame.transform.flip(img, 1, 0)
        self.game.screen.blit(img, pos)

    def stunPlayer(self, stunDirection=1):
        self.stun = 1
        self.stunDirection = stunDirection

    def die(self):
        self.game.state = 2
        if not self.dead:
            self.progress = 0
            self.game.finalscore = self.game.score
            self.game.finalcounts = self.game.counts[:]
            self.game.stars.append(Canvas(self.game, "EmptySplash", (self.game.x/2,0)))
            self.dead = True
            self.game.playMusic("Partners_in_Crimefighting.wav")
        
    def punch(self, dx):
        self.punching = 1
        self.progress = 0
        self.punchState = self.state
        if self.punchState != 2 and dx != 0:
            self.right = dx > 0