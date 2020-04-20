import pygame
from PIL import Image
import os, sys, math, random
from Constants import *
from Player import Player
from Building import Building
from Car import Car
from Bomb import Bomb
from Alien import Alien
from Star import Star
from Boss import Boss
from BossBomb import BossBomb
from Crook import Crook
from Canvas import Canvas

exe = 1

class Game:

    def reset(self, respawn=False):
        ''' Resets the game '''
        self.player = Player(self)
        self.sidekick = Player(self, sidekick=True)
        self.x = 0
        self.lastHeight = 0
        self.darkness = pygame.Surface((WIDTH,HEIGHT))
        self.darkness.fill(pygame.Color(0,0,0))
        self.darkness.set_alpha(80)
        self.state = 0 # 0 = start, 1 = play, 2 = GG
        self.spawnx = 0
        self.blocks = []
        self.stars = []
        self.font = pygame.font.Font("font/LCD_Solid.ttf", FONT_SIZE)
        self.fontSmall = pygame.font.Font("font/LCD_Solid.ttf", FONT_SIZE)
        self.fontMed = pygame.font.Font("font/LCD_Solid.ttf", FONT_SIZE)
        self.fontBig = pygame.font.Font("font/LCD_Solid.ttf", FONT_SIZE*2)
        self.boss = False
        self.fontBold = pygame.font.Font("font/LCD_Solid.ttf", FONT_SIZE*4)
        self.bossSprite = None
        self.score = 0
        self.finalscore = 0
        self.counts = [0,0,0,0]
        self.finalcounts = [0,0,0,0]
        if respawn:
            self.stars.append(Canvas(self, "EmptySplash", [0,0]))
        else:
            self.stars.append(Canvas(self, "Splash", [0,0]))
        self.enemies = []
        self.blocks.append(Building(self, 0, (3000,1)))
        self.blocks = sorted(self.blocks, key=lambda x:-x.size[1])

    def ui(self):
        if self.state == 1:
            caption = self.font.render("Score: "+str(int(self.score)), True, (255,255,255))
            self.screen.blit(caption, (SCALE/2,SCALE/2))
        h = self.x / (SCALE*1000) - BOSS_H
        if h > 0 and self.state == 1:
            speed = .02
            s = ""
            if h < speed*2:
                s = '"Beware my new weapons!"'
            elif h < speed*3:
                s = '"Red-onite Bombs to defeat you..."'
            elif h < speed*4:
                s = '"And Blue-tonium Bombs for your sidekick!"'
            elif h < speed*5:
                s = '"With my Red-onite powered shield,"'
            elif h < speed*6:
                s = '"There is no way you can ever stop me!"'
            caption = self.font.render(s, True, (255,255,255))
            self.screen.blit(caption, (SCALE/2+FONT_SIZE*2,SCALE/2+int(2.4*FONT_SIZE)))
            if h < speed*6:
                caption = self.font.render("Professor Purple:", True, (255,0,255))
                self.screen.blit(caption, (SCALE/2,SCALE/2+int(FONT_SIZE*1.2)))
        elif self.state == 2 or self.state == 3:
            self.screen.blit(self.darkness, (0,0))
            if self.state == 2:
                caption = self.fontBold.render("Game Over", True, (255,255,255))
                self.screen.blit(caption, (WIDTH/2-FONT_SIZE*11,SCALE))
            else:
                caption = self.fontBold.render(" Victory", True, (255,255,255))
                self.screen.blit(caption, (WIDTH/2-FONT_SIZE*11,SCALE))
            caption = self.fontBig.render("Score: "+str(int(self.finalscore)), True, (255,255,255))
            self.screen.blit(caption, (int(FONT_SIZE*2.2),SCALE+FONT_SIZE*4.5))
            if self.finalcounts[0]:
                caption = self.fontMed.render("Speeding Taxis Stopped: "+str(int(self.finalcounts[0])), True, (255,255,255))
                self.screen.blit(caption, (FONT_SIZE*4,SCALE+FONT_SIZE*7))
            if self.finalcounts[1]:
                caption = self.fontMed.render("Deadly Bombs Defused: "+str(int(self.finalcounts[1])), True, (255,255,255))
                self.screen.blit(caption, (FONT_SIZE*4,SCALE+FONT_SIZE*9))
            if self.finalcounts[2]:
                caption = self.fontMed.render("Supervillains Subdued: "+str(int(self.finalcounts[2])), True, (255,255,255))
                self.screen.blit(caption, (FONT_SIZE*4,SCALE+FONT_SIZE*11))
            if self.finalcounts[3]:
                caption = self.fontMed.render("Alien Invaders Repelled: "+str(int(self.finalcounts[3])), True, (255,255,255))
                self.screen.blit(caption, (FONT_SIZE*4,SCALE+FONT_SIZE*13))
            if self.state == 3:
                caption = self.fontMed.render("Professor Purple: Defeated", True, (255,255,255))
                self.screen.blit(caption, (FONT_SIZE*4,SCALE+FONT_SIZE*15))
            elif self.finalscore == 0:
                caption = self.fontSmall.render("  Don't forget to protect your sidekick!", True, (255,255,255))
                self.screen.blit(caption, (int(FONT_SIZE*2.2),SCALE+FONT_SIZE*15))
            else:
                caption = self.fontSmall.render("But you didn't keep your sidekick alive...", True, (255,255,255))
                self.screen.blit(caption, (int(FONT_SIZE*2.2),SCALE+FONT_SIZE*15))
            caption = self.font.render("[Press Enter to Play Again]", True, (255,255,255))
            self.screen.blit(caption, (WIDTH/2-FONT_SIZE*8,SCALE+FONT_SIZE*17))
    
    def update(self, dt, keys):
        ''' Updates the game by a timestep and redraws graphics '''
        if dt>100:
            return
        if (self.state == 1 or self.state == 3) and not self.sidekick.captured:
            self.x += dt*SPEED/2
            self.sidekick.pos[0] += dt*SPEED/2
            if self.boss and self.state == 1:
                if self.bossSprite.state == 1:
                    self.sidekick.pos[0] += dt*SPEED/10
                elif self.sidekick.pos[0]-self.x > SCALE:
                    self.sidekick.pos[0] -= dt*SPEED/2.2
            if self.sidekick.state == 0:
                self.sidekick.state = 1
        # User input
        move = [0,FALL_SPEED*dt]
        drop = False
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.player.state==2:
                # move[1]*=2
                pass
            else:
                drop = True
        if self.player.jump > 0:
            move[1] -= 2*JUMP_SPEED*dt*self.player.jump/JUMP
            self.player.jump -= dt
            if self.player.jump <= 0:
                self.player.jump = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.player.state == 0:
                self.player.state = 1
            self.player.right = 1
            if self.state == 1 and not self.sidekick.captured and not self.player.stun:
                move[0] += SPEED*dt*1.4
            elif not self.player.stun:
                move[0] += SPEED*dt
            if self.player.pos[0]>=self.x+WIDTH-35:
                move[0] = self.x+WIDTH-20 - self.player.pos[0]
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.player.state == 0:
                self.player.state = 1
            self.player.right = 0
            if self.state == 1 and not self.sidekick.captured and not self.player.stun:
                move[0] -= SPEED*dt*.8
            elif not self.player.stun:
                move[0] -= SPEED*dt
        else:
            if self.player.state == 1:
                self.player.state = 0
        if self.player.pos[0] < self.x+30:
            move[0] += self.x+30-self.player.pos[0]
            if self.player.state == 0:
                self.player.state = 1
            if self.state==1:
                self.player.right = 1
        self.player.pos[0] += move[0]
        self.player.pos[1] += move[1]

        # Collisions
        self.fall(self.player, move, dt, False, drop)
        if not self.sidekick.captured:
            self.fall(self.sidekick, [0,FALL_SPEED*dt], dt)
        for enemy in self.enemies:
            if isinstance(enemy, Crook):
                self.fall(enemy, [0,FALL_SPEED*dt], dt)
        for enemy in self.enemies:
            if enemy.hit(self.player.pos, [16*PIXEL_RATIO,40*PIXEL_RATIO]):
                if isinstance(enemy, Boss):
                    if not self.player.stun:
                        self.playSound("VillainPunch.wav")
                    self.player.stunPlayer()
                    enemy.shield = 1
                elif isinstance(enemy, BossBomb) and enemy.blue==False:
                    if self.player.pos[0] < enemy.pos[0]+enemy.size[0]/2:
                        self.player.stunPlayer(1)
                    else:
                        self.player.stunPlayer(-1)
                    enemy.success()
                else:
                    enemy.die(self.player.state==2)
                    if not isinstance(enemy, Bomb):
                        self.playSound("SuperPunch.wav")
                    self.player.punch(enemy.pos[0]+enemy.size[0]/2 - self.player.pos[0])
            elif enemy.hit(self.sidekick.pos, [16*PIXEL_RATIO,40*PIXEL_RATIO]) and (self.sidekick.state == 1 or self.sidekick.captured) and not self.sidekick.dead:
                if isinstance(enemy, Boss):
                    enemy.die(False)
                    self.sidekick.punch(1)
                elif isinstance(enemy, BossBomb) and enemy.blue==False:
                    pass
                elif not isinstance(enemy, Alien):
                    self.sidekick.die()
                    enemy.success()
                elif enemy.lock == self.sidekick:
                    self.sidekick.pos[0] = -HEIGHT
                    self.sidekick.die()
                    enemy.success()

        # Sidekick AI
        if self.sidekick.state != 2:
            for block in self.blocks:#602
                if block.check(self.sidekick.pos[0]+SCALE*3, self.sidekick.pos[1]-SCALE*4, self.sidekick.pos[1]-SCALE*1):
                    self.sidekick.state = 2
                    self.sidekick.progress = 0
                    self.sidekick.jump = JUMP*8.8/10
                    self.sidekick.platform = None
                    self.playSound("Jump.wav")
                    break
        for enemy in self.enemies:
            if isinstance(enemy, Crook):
                if enemy.state != 2 and not enemy.dead:
                    for block in self.blocks:
                        if enemy.v > 0 and block.check(enemy.pos[0]+SCALE*5, enemy.pos[1]-SCALE*4, enemy.pos[1]-SCALE*1):
                            enemy.state = 2
                            enemy.progress = 0
                            enemy.jump = JUMP*8.8/10
                            self.playSound("Jump.wav")
                        if enemy.v < 0 and block.check(enemy.pos[0]-SCALE*1, enemy.pos[1]-SCALE*4, enemy.pos[1]-SCALE*1):
                            enemy.state = 2
                            enemy.progress = 0
                            enemy.jump = JUMP*8.8/10
                            self.playSound("Jump.wav")
        
        # Graphics
        self.screen.fill((1,53,70))
        for star in self.stars:
            star.update(dt)
        for block in self.blocks:
            block.update(dt)
        for enemy in self.enemies:
            if not isinstance(enemy, Alien):
                enemy.update(dt)
        self.sidekick.update(dt)
        self.player.update(dt)
        for enemy in self.enemies:
            if isinstance(enemy, Alien):
                enemy.tractor(dt)
        for enemy in self.enemies:
            if isinstance(enemy, Alien):
                enemy.update(dt)
        self.ui()
        self.spawnBuildings()

    def keyPressed(self, key):
        ''' Respond to a key press event '''
        if key==pygame.K_RETURN:
            if self.state != 1:
                if self.state == 2 or self.state == 3:
                    self.reset(True)
                self.playSound("Begin.wav")
                self.state = 1
        if key==pygame.K_UP or key==pygame.K_w:
            if self.player.state != 2:
                self.player.state = 2
                self.player.progress = 0
                self.player.jump = JUMP
                self.playSound("SuperJump.wav")

    def fall(self, person, move, dt, applyfall=True, drop=False):
        if applyfall:
            if person.jump > 0:
                move[1] -= 2*JUMP_SPEED*dt*person.jump/JUMP
                person.jump -= dt
            if person.jump <= 0:
                person.jump = 0
            person.pos[1] += move[1]
        falling = 1
        for block in self.blocks:
            if drop and block.size[1] > SCALE:
                continue
            hit = block.hit(person.pos, [16*PIXEL_RATIO,40*PIXEL_RATIO], move[1])
            if hit:
                person.pos[1] -= hit
                falling = 0
                person.platform = block
                if person.state == 2:
                    person.state = 0
                    # self.playSound("Land.wav")
                break
        if falling:
            person.state = 2

    def spawnBuildings(self):
        if self.state != 1 and self.state != 3:
            return
        h = min(1, self.x / (SCALE*1000))
        if h > BOSS_H:
            if not self.boss:
                self.bossSprite = Boss(self)
                self.enemies.append(self.bossSprite)
            self.boss = True
        if random.random()<.04:
            self.stars.append(Star(self, [self.x+WIDTH, random.random()*HEIGHT*.9]))
        if int(self.x/(5*SCALE)) > self.spawnx:
            h = min(1, self.x / (SCALE*1000))
            print(round(h,3))
            self.spawnx = int(self.x/(5*SCALE))
            # Cleanup offscreen
            for building in self.blocks[:]:
                if building.pos[0] + building.size[0]<self.x:
                    self.blocks.remove(building)
            for star in self.stars[:]:
                if star.pos[0] + star.size[0]<self.x:
                    self.stars.remove(star)
            for enemy in self.enemies[:]:
                if enemy.pos[0] + enemy.size[0]<self.x and enemy.v <= 0:
                    self.enemies.remove(enemy)
                elif enemy.pos[0]>self.x+WIDTH and enemy.v > 0:
                    self.enemies.remove(enemy)
            if random.random()<0.9:
                height = 6+3*int(random.random()*4)
                if height == self.lastHeight:
                    return
                self.lastHeight = height
                width = 6+3*int(random.random()*3)
                building = Building(self, (self.x+WIDTH)/SCALE, (width,height))
                self.blocks.append(building)
                self.blocks = sorted(self.blocks, key=lambda x:-x.size[1])
                if not self.boss:
                    # Bomb spawning
                    if random.random()<0.1+h*.3:
                        dx = int(max(0, random.random()*(width-3)/3))
                        dy = int(max(0, random.random()*(height-3)/3))
                        self.enemies.append(Bomb(self, (self.x+WIDTH+dx*SCALE*3, HEIGHT-height*SCALE)))
                    # Alien spawning
                    if random.random()<(h-.3)*.6:
                        self.enemies.append(Alien(self, building))
                elif self.bossSprite.state == 1 and not self.bossSprite.dead:
                    x = self.bossSprite.pos[0] + self.bossSprite.size[0]/2
                    y = HEIGHT*.52
                    if random.random()<0.5:
                        bomb = BossBomb(self, [x,y], building, True)
                    else:
                        bomb = BossBomb(self, [x,y], building, False)
                    self.enemies.append(bomb)
            if not self.boss:
            # Car spawning
                count = 0
                for enemy in self.enemies:
                    if isinstance(enemy, Car):
                        count+=1
                if random.random()*(4*h)+1 < count:
                    pass
                elif random.random()<.4:
                    self.enemies.append(Car(self, self.x, -.2))
                elif random.random()<(.4/.6):
                    self.enemies.append(Car(self, self.x, 1))
                # Villain spawning
                count = 0
                for enemy in self.enemies:
                    if isinstance(enemy, Crook):
                        count+=1
                if count <= h*2-0.5:
                    if random.random() < .2+h*.2:
                        self.enemies.append(Crook(self, [self.x+WIDTH+200,0], -.2))
                    if random.random() < .2+h*.2:
                        self.enemies.append(Crook(self, [self.x-200,0], .8))

    def loadLevel(self, name):
        ''' Reads a level from a text file '''
        if exe:
            path = os.path.join(os.path.dirname(sys.executable), 'levels')
        else:
            path = os.path.join(os.path.dirname(__file__), 'levels')
        grid = []
        with open(os.path.join(path, name), 'r') as file:
            for y, line in enumerate(file):
                grid.append([])
                for x, char in enumerate(line):
                    if char == "1": # Block
                        if y>0 and len(grid[y-1])>x and grid[y-1][x]:
                            b = grid[y-1][x]
                            b.kill()
                            grid[y].append(Block(self,
                                                 [x*SCALE, y*SCALE-b.size[1]/2],
                                                 [SCALE, SCALE+b.size[1]]))
                        else:
                            grid[y].append(Block(self, [x*SCALE, y*SCALE],
                                                 [SCALE, SCALE]))
                    else:
                        grid[y].append(False)
                    if char == "*": # Player
                        self.origin = [WIDTH/2-x*SCALE, HEIGHT/2-y*SCALE]
                    if char == "_": # Platform
                        Block(self, [x*SCALE, (y+.45)*SCALE], [SCALE, SCALE*.1])
                    if char == "!": # Enemy
                        Enemy(self, [x*SCALE, y*SCALE])
                    if char == "0": # Boss (2x2, squares above and to the right)
                        Boss(self, self.level, [x*SCALE, (y-.5)*SCALE])

################################################################################
    
    def __init__(self, name):
        ''' Initialize the game '''
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0, 30'
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        icon = self.loadImage("Icon.png", scale=1)
        icon.set_colorkey((255,0,0))
        pygame.display.set_icon(icon.convert_alpha())
        self.audio = {}
        self.playMusic("Partners_in_Crimefighting.wav")
        self.playSound("AlienEnter.wav", False)
        self.playSound("Begin.wav", False)
        self.playSound("BombBeep.wav", False)
        self.playSound("Boom.wav", False)
        self.playSound("CabEnter.wav", False)
        self.playSound("Crunch.wav", False)
        self.playSound("Land.wav", False)
        self.playSound("Lose.wav", False)
        self.playSound("Snip.wav", False)
        self.playSound("SuperJump.wav", False)
        self.playSound("SuperPunch.wav", False)
        self.playSound("TractorBeam.wav", False)
        self.playSound("TractorBeamStart.wav", False)
        self.playSound("VillainPunch.wav", False)

        self.reset()
        self.run()

    def run(self):
        ''' Iteratively call update '''
        clock = pygame.time.Clock()
        self.pause = False
        while not self.pause:
            for event in pygame.event.get():
                if event.type is pygame.KEYDOWN:
                    self.keyPressed(event.key)
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            dt = clock.tick(TIME_STEP)
            self.update(dt, pygame.key.get_pressed())
            pygame.display.update()
    
    def loadImage(self, name, number=1, scale=PIXEL_RATIO):
        ''' Loads an image or list of images '''
        if not hasattr(self, "images"):
            self.images = {}
        elif name in self.images:
            return self.images[name]
        if exe:
            path = os.path.join(os.path.dirname(sys.executable), 'images')
        else:
            path = os.path.join(os.path.dirname(__file__), 'images')
        if number==1:
            img = pygame.image.load(os.path.join(path, name))
            img = pygame.transform.scale(img, [scale*img.get_width(), scale*img.get_height()])
        else:
            img = []
            for i in range(number):
                key = name[:-4]+str(i)+name[-4:]
                img.append(pygame.image.load(os.path.join(path, key)))
                img[-1] = pygame.transform.scale(img[-1], [scale*img[-1].get_width(), scale*img[-1].get_height()])
        self.images[name] = img
        return img

    def playMusic(self, name):
        ''' Plays the given background track '''
        if exe:
            path = os.path.join(os.path.dirname(sys.executable), 'audio')
        else:
            path = os.path.join(os.path.dirname(__file__), 'audio')
        pygame.mixer.music.load(os.path.join(path, name))
        pygame.mixer.music.play(-1)
        
    def playSound(self, name, play=True):
        ''' Plays the given sound effect ''' 
        if name in self.audio:
            sound = self.audio[name]
        else:
            if exe:
                path = os.path.join(os.path.dirname(sys.executable), 'audio')
            else:
                path = os.path.join(os.path.dirname(__file__), 'audio')        
            sound = pygame.mixer.Sound(os.path.join(path, name))
            self.audio[name] = sound
        if play:
            sound.play()


if __name__ == '__main__':
    game = Game("Sidekick")
