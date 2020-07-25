#!/usr/bin/python3
import pygame, sys
import math
pygame.init()

scr_w, scr_h = 900, 800
screen = pygame.display.set_mode((scr_w, scr_h))


class Ray:
  def __init__(self, source, angle):
    self.angle = angle
    self.p1 = (int(source.x), int(source.y))
    self.p2 = self.create_p2(angle, None)
    self.draw_cords = self.p2
  
  def collide(self, wall):
    p2 = (-1, -1)
    if wall:
      slp1 = (wall.p1[1] - wall.p2[1])/(wall.p1[0] - wall.p2[0])
      intc1 = wall.p1[1] - slp1*wall.p1[0]
      try:
        slp2 = (self.p1[1] - self.p2[1])/(self.p1[0] - self.p2[0])
      except:
        slp2 = float('inf')
      intc2 = self.p1[1] - slp2*self.p1[0]
      if slp2 - slp1 == 0:
        x = float('inf')
      else:
        x = (intc1 - intc2)/(slp2 - slp1)
      y = slp1*x + intc1
      if (wall.p1[0]<=x and x<=wall.p2[0]) or (wall.p2[0]<=x and x<=wall.p1[0]):
        if (wall.p1[1]<=y and y<wall.p2[1]) or (wall.p2[1]<=y and y<=wall.p1[1]):
          if (self.p1[0]<x and x<self.p2[0]) or (self.p2[0]<=x and x<=self.p1[0]):
            if (self.p1[1]<=y and y<self.p2[1]) or (self.p2[1]<=y and y<=self.p1[1]):
              p2 = (x, y)
    return p2

  def collide_walls(self, walls):
    ls = {}
    for wall in walls:
      p2 = self.collide(wall)
      length = math.sqrt(math.pow( (self.p1[0] - p2[0]), 2) + math.pow( (self.p1[1] - p2[1]), 2))
      ls[length] = p2

    keys = list(ls.keys())
    num = min(keys)
    return ls[num]
      

  def create_p2(self, angle, walls):
    length = math.sqrt(2)*scr_w # hypotenus
    p2 = 0
    if 0 <= angle and angle < math.pi/2: # first quad
      x = math.cos(angle) * length
      y = math.sin(angle) * length
      p2 = (int(self.p1[0] + x), int(self.p1[1] - y))
    elif math.pi/2 <= angle and angle < math.pi: # second quad
      angle = math.pi - angle
      x = math.cos(angle) * length
      y = math.sin(angle) * length
      p2 = (int(self.p1[0] - x), int(self.p1[1] - y))     
    elif math.pi <= angle and angle < (3*math.pi/2): # third quad
      angle = angle - math.pi
      x = math.cos(angle) * length
      y = math.sin(angle) * length
      p2 = (int(self.p1[0] - x), int(self.p1[1] + y)) 
    elif (3*math.pi/2) <= angle and angle < 2*math.pi: # forth quad
      angle = (2*math.pi) - angle
      x = math.cos(angle) * length
      y = math.sin(angle) * length
      p2 = (int(self.p1[0] + x), int(self.p1[1] + y)) 
    
    coll_cords = 0
    if walls:
      coll_cords = self.collide_walls(walls)
    if coll_cords != None and coll_cords != (-1, -1):
      self.draw_cords = coll_cords
    else:
      self.draw_cords = p2
    return p2
  
  def update_source(self, pos, walls):
    self.p1 = (pos[0], pos[1])
    self.p2 = self.create_p2(self.angle, walls)

  def __str__(self):
    return f'angle: {self.angle}'


class Wall:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
    self.draw(screen)

  def draw(self, surface):
    pygame.draw.line(surface, (255, 255, 255), self.p1, self.p2)


class Source:
  def __init__(self):
    self.x = scr_w//2
    self.y = scr_h//2
    self.rays = self.create_rays(100)
    self.draw(screen)

  def create_rays(self, num): 
    rays = [] 
    div = (2*math.pi)/num
    angle = 0
    for i in range(num):
      rays.append(Ray(self, angle))
      angle+=div
    return rays
  
  def draw_rays(self, surface):
    for ray in self.rays:
      pygame.draw.line(surface, (255, 0, 255), ray.p1, ray.draw_cords)

  def update_rays(self, pos, walls):
    for ray in self.rays:
      ray.update_source(pos, walls)

  def update_pos(self, pos, walls):
    self.x = pos[0]
    self.y = pos[1]
    self.update_rays(pos, walls)
    self.draw(screen)
    self.draw_rays(screen)
 
  def draw(self, surface):
    pygame.draw.circle(surface, (0, 255, 255), (self.x, self.y), 5)


wall = Wall((500, 500), (30, 89))
wall2 = Wall((500, 10), (10, 500))
wall3 = Wall((800, 100), (600, 400))
wall4 = Wall((800, 800), (600, 500))
sc = Source()

def run():
  global wall
  walls = [wall, wall2, wall3, wall4]
  while(True):
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          sys.exit()
    
    pygame.display.flip()
    screen.fill((0,0,0))
    mspos = pygame.mouse.get_pos()
    sc.update_pos(mspos, walls)
    for wall in walls:
      wall.draw(screen)


if __name__ == '__main__':
  run()
