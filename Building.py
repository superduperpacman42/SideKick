import pygame
import random
from Constants import *

class Building:

    def __init__(self, game, x, size):
        self.game = game
        self.size = (size[0]*SCALE, size[1]*SCALE)
        self.pos = [x*SCALE, HEIGHT-size[1]*SCALE+PIXEL_RATIO]
        x = int(150-size[1]*6000/HEIGHT)
        self.color = pygame.Color(x,x,int(x*1.2))
        self.windows = []
        if self.size[1] == SCALE:
            self.color = (50,50,50)
        # self.progress = 0
    
    def update(self, dt):
        # if self.game.state == 1:
        #     self.pos[0] += (self.size[1]/SCALE-3)*dt*SPEED/60
        # img = self.sprite[int(self.progress)%len(self.walkImages)]
        # self.game.screen.blit(img, pos)
        # self.progress += dt/120
        # if self.progress >= len(self.walkImages):
        #     self.progress = 0
        pos = [self.pos[0]-self.game.x, self.pos[1]]
        pygame.draw.rect(self.game.screen, self.color, pygame.Rect(pos,self.size))
        pygame.draw.rect(self.game.screen, (0,0,0), pygame.Rect(pos,self.size), PIXEL_RATIO)
        if self.size[1] == SCALE:
            return
        for x in range(int(self.size[0]/(3*SCALE))):
            for y in range(int(self.size[1]/(3*SCALE))):
                i = x*int(self.size[1]/(3*SCALE))+y
                if i >= len(self.windows):
                    self.windows += [random.random()<0.2]
                # pos2 = [pos[0] + PIXEL_RATIO*x*SCALE + SCALE/PIXEL_RATIO+12*PIXEL_RATIO, pos[1] + PIXEL_RATIO*y*SCALE + SCALE/PIXEL_RATIO + 6*PIXEL_RATIO]
                pos2 = [pos[0] + 3*x*SCALE + SCALE/3+9*3, pos[1] + 3*y*SCALE + SCALE/3 + 5*3]
                pos3 = [pos2[0] - PIXEL_RATIO, pos2[1] - PIXEL_RATIO]
                pygame.draw.rect(self.game.screen, (0,0,0), pygame.Rect(pos3,(6*PIXEL_RATIO+2*PIXEL_RATIO,8*PIXEL_RATIO+2*PIXEL_RATIO)))
                if random.random() < 0.0005:
                    self.windows[i] = not self.windows[i]
                if self.windows[i]:
                    pygame.draw.rect(self.game.screen, (25,25,25), pygame.Rect(pos2,(6*PIXEL_RATIO,8*PIXEL_RATIO)))
                else:
                    pygame.draw.rect(self.game.screen, (200,200,50), pygame.Rect(pos2,(6*PIXEL_RATIO,8*PIXEL_RATIO)))

    def hit(self, pos, size, deltay):
        ''' Detect collisions of platform '''
        if pos[0]-size[0]/2>self.pos[0]+self.size[0] or pos[0]+size[0]/2<self.pos[0]:
            return False
        dy = (pos[1]+size[1]/2)-self.pos[1]
        if dy >= 0 and dy <= deltay+.01:
            return dy
        return False

    def check(self, x, ymin, ymax):
        if x>self.pos[0]+self.size[0] or x<self.pos[0]:
            return False
        return ymin <= self.pos[1] and ymax >= self.pos[1]
