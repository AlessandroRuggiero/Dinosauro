from AlphaBasic import *
import pygame
import pickle
import random
import neat
import time
import os
import copy
from viz import draw_net
pygame.init()
clock = pygame.time.Clock() 
dis = (1300,700)
back = (255,255,255)
win = pygame.display.set_mode(dis)
font = pygame.font.SysFont("comicsans",30)
timer = 0
counter = 100
run = True
respawn = []
players = []
obstacles = []
speed = Vector(-8,0)
class Obstacle ():
    """is an obstacle with x,y,w,hg"""
    def __init__ (self,x,y,w,hg,fly = False):
        self.coord = Vector(x,y)
        self.w = w
        self.hg = hg
        self.fly = fly
        if self.fly:
            self.coord.y-=40
            self.hg+= 20
    def move (self,speed):
        for _ in range (4):
            self.coord+=Vector (speed.x/4,speed.y)
            for player in players:
                if collision (self.coord,player) or collision(self.coord + Vector (self.w,0),player) or collision (self.coord +Vector(0,self.hg),player) or collision (self.coord + Vector (self.w,self.hg),player):
                    player.death ()
        if self.coord.x < -self.w:
            self.death ()
    def death (self):
        global respawn
        obstacles.remove (self)
        respawn.append (random.randint(1,31))
        reword ()
    def draw (self,color = (0,0,0)):
        pygame.draw.rect(win, color, (self.coord.x,self.coord.y,self.w,self.hg))
class Player ():
    def __init__ (self,g,config):
        self.coord = Vector (100,dis[1]//2-5)
        self.w = 20
        self.hg = 20
        self.speed = 0
        self.jumping = True
        self.nn = neat.nn.FeedForwardNetwork.create(g,config)
        self.gene = g
        self.gene.fitness = 0
        self.crouching = False
    def draw (self):
        pygame.draw.rect(win, (0,0,0), (self.coord.x,self.coord.y,self.w,self.hg))
    def update (self,nearest):
        if self.crouching:
            self.hg = 10
        else :
            self.hg = 20
        self.coord.y+= self.speed
        if self.coord.y >= dis[1]-self.hg:
            self.coord.y = dis[1]-self.hg
            self.jumping = False
            if self.speed > 0:
                self.speed = 0
        else:
            self.speed+=1
        j,c = self.nn.activate ((nearest.coord.x-self.coord.x+nearest.w,nearest.w,nearest.hg,int(nearest.fly)))
        if c >= 0.5:
            self.crouching = True
        else :
            self.crouching = False
        if j >= 0.5:
            self.jump()
    def jump (self):
        if not self.jumping and not self.crouching:
            self.speed-= 15
            self.jumping = True
    def death (self):
        self.gene.fitness -= 1
        players.remove(self)
def reword ():
    for player in players:
        player.gene.fitness += 5
def start ():
    global players,obstacles,counter
    players = []
    obstacles = []
    counter = 100
    obstacles.append (Obstacle(dis[0]-200,dis[1]-15,15,15))
def draw ():
    pygame.display.update()
    win.fill(back)
    for player in players:
        player.draw ()
    for obstacle in obstacles:
        obstacle.draw ()
def events (keys):
    pass
def clickdetect():
    start()
    for player in players:
        player.jump ()
def main(genomes,config):
    global run,counter,players,obstacles,respawn
    respawn = [25,60]
    start ()
    run = True
    for _,g in genomes:
        players.append(Player(g,config))
    while run:
        if respawn:
                respawn[0]-=1
                if not respawn[0]:
                    hight = random.choice([False,True])
                    if hight:
                        w = w = random.randint (20,50)
                        hg = random.randint (70,90)
                    else:
                        w = random.randint (15,50)
                        hg = random.randint (15 if w<= 40 else 40,60  if w <= 40 else 40)
                    obstacles.append (Obstacle(dis[0]-w,dis[1]-hg,w,hg,hight))
                    respawn.pop(0)
        
        for entity in obstacles:
            entity.move (speed)
        draw ()
        #pygame.time.delay(timer)
        #clock.tick(60)
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickdetect()
        events(pygame.key.get_pressed())
        if players:
            for en in obstacles:
                if players[0].coord.x < en.coord.x + en.w:
                    nearest = en
                    nearest.draw((255,0,0))
                    tx= font.render(str(nearest.__dict__).replace ('{','').replace ('}','') + '    giocatori: ' +str( len (players)),1,(0,0,0))
                    win.blit(tx,(10,20))
                    break
            for player in players:
                player.update(nearest)
        else :
            run = False
            print ('died')
def go(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population (config)
    p.add_reporter (neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,50)
    draw_net (config,winner,view = True)
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,'config-feedforward.txt')
    go (config_path)
pygame.quit()