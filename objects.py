
import pygame
from math import sin, cos, atan2, pi, sqrt
import random

def dist(x1,y1,x2,y2):
	return ((x1-x2)**2 + (y1-y2)**2)**0.5

class Player:
	def __init__(self,size,color):
		self.pos = (200,200)
		self.size = size
		self.pre_vel = (0,0)
		self.vel = (0,0)
		self.max_vel = (7,7)
		self.color = color
		self.target = (100,100)
		self.isdead = False
		self.isstop = False

	def update(self):
		if not self.isstop:
			x,y = self.pos
			tx,ty = self.target
			vx,vy = self.vel
			pvx,pvy = self.pre_vel
			ax = .003*(tx - x)
			ay = .003*(ty - y)

			vx+=ax
			vy+=ay

			self.set_vel(vx,vy)

			self.pre_vel = (vx,vy)
			x+=vx
			y+=vy
			self.set_pos(x,y)

	def isCollide(self, enemies):
		x,y = self.get_pos()
		size = self.get_size()
		for e in enemies:
			e_x, e_y = e.get_pos()
			e_size = e.get_size()
			if dist(x,y,e_x,e_y)<size+e_size:
				self.isdead = True
				return True

	def exceeds_boundary(self):
		x,y = self.get_pos()
		s  = self.get_size()
		w,h = pygame.display.get_surface().get_size()
		if x+s>w or x-s<0 or y+s>h or y-s<0:
			self.isdead = True
			return True

	def get_size(self):
		return self.size

	def get_pos(self):
		return self.pos

	def stop(self):
		self.isstop = True

	def resume(self):
		self.isstop = False




	def draw(self,surf):
		pygame.draw.circle(surf,self.color,self.pos,self.size)

	def set_target(self,x,y):
		tx,ty = self.target
		if dist(x,y,tx,ty)>100:
			self.target = (int(x),int(y))

	def get_target(self):
		return self.target

	def set_pos(self,x,y):
		self.pos = (int(x),int(y))

	def get_pos(self):
		return self.pos

	def set_vel(self,x,y):
		mvx,mvy = self.max_vel
		x = max(-mvx,min(x,mvx))
		y = max(-mvy,min(y,mvy))
		self.vel = (x,y)

	def get_vel(self):
		return self.vel




class Enemy:
	def __init__(self,pos=None,size=20,color=(0,200,0)):
		self.w,self.h = (w,h) = pygame.display.get_surface().get_size()
		self.size = random.randint(size-3,size+3)
		self.pos = (x,y) = (random.randint(0,w),random.randint(0,h))
		self.points = []
		self.color = color
		self.vel = (random.randint(-6,6),random.randint(-6,6))
		self.life = 3
		self.isstop = False
		self.boundry_margin = margin = 60


		if self.vel[0]==0 and self.vel[1]==0:
			self.vel = (1,1)

		sides = ["top","right","bottom","left"]
		side = sides[random.randint(0,3)]
		if side == "top":
			self.pos = (x,y) = (random.randint(0,w),-margin)
		elif side == "right":
			self.pos = (x,y) = (w+margin,random.randint(0,h))
		elif side == "bottom":
			self.pos = (x,y) = (random.randint(0,w),h+margin)
		elif side == "left":
			self.pos = (x,y) = (-margin,random.randint(0,h))

		if pos:
			self.pos = pos


		self.generate_points()

	def generate_points(self):
		points = []
		x,y = self.pos
		size = self.size
		n = random.randint(8,10)  # random no. of vertices for polygon
		for i in range(n):
			xi = x + size*cos(2*pi*i/n) + random.random()*size*.5	#random shape of polygons
			yi = y + size*sin(2*pi*i/n) + random.random()*size*.5

			points.append((int(xi), int(yi)))
		self.points = points


	def update(self):

		if not self.isstop:
			x,y = self.pos
			x += self.vel[0]
			y += self.vel[1]
			self.pos = (x,y)
			points = []
			for i,j in self.points:
				i += self.vel[0]
				j += self.vel[1]
				points.append((int(i), int(j)))
			self.points = points

	def draw(self,surf):
		pygame.draw.polygon(surf,self.color, self.points, 0)
		# pygame.draw.circle(surf,self.color, self.pos, self.size, 1)

	def exceeds_boundary(self,w,h):
		x,y = self.pos
		margin = self.boundry_margin
		return x>w+margin or x<-margin or y>h+margin or y<-margin

	def inside_area(self,w1,w2,h1,h2):
		x,y = self.pos
		return w1<x<w2 and h1<y<h2

	def hit(self,enemies):
		sx,sy = self.get_pos()
		ss = self.get_size()
		for e in enemies:
			ex,ey = e.get_pos()
			es = e.get_size()
			if dist(ex,ey,sx,sy)<es+ss and e!= self:
				return e
		return None


	def get_pos(self):
		return self.pos

	def get_size(self):
		return self.size

	def get_life(self):
		return self.life

	def damage(self):
		self.life -= 1

	def stop(self):
		self.isstop = True

	def resume(self):
		self.isstop = False


class Rocks(Enemy):
	def __init__(self,pos,size,color=(0,200,0)):
		self.pos = pos
		self.size = random.randint(2,size)
		self.color = color
		# self.vel = (random.randint(-6,6),random.randint(-6,6))
		ang = random.uniform(0,2*pi)
		self.vel = (6*sin(ang),6*cos(ang))
		self.life = 12
		self.age = 0

		self.isstop = False

	def update(self):
		if not self.isstop:
			x,y = self.pos
			vx,vy = self.vel
			x += vx
			y += vy

			# vx+=random.randint(-4,4)
			# vy+=random.randint(-4,4)
			self.vel = (vx,vy)
			self.set_pos(x,y)

			self.size-=.6 if self.size>1 else 0

			self.age+=1
			

	def draw(self,surf):
		pygame.draw.circle(surf, self.color, self.pos,int(self.size))

	def alive(self):
		return self.age<self.life

	def set_pos(self,x,y):
		self.pos = (int(x),int(y))