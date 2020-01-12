#!/usr/bin/env python3


from numpy.random import randint
import pygame, sys, time

from detection import OpenCV
from objects import *
from layout import Button, Menu, printText
from handleScore import getScore, saveScore

pygame.init()



class Game:
	w,h = 900,720
	screen = pygame.display.set_mode((w,h))
	detector = OpenCV()
	enemy_count = 20
	paused = True

	def __init__(self):
		self.player = Player(20, (255,0,0))
		self.debries = []
		self.enemies = []
		w,h = self.w,self.h
		self.high_score = getScore()[0]["score"]
		self.score = 0
		self.player_alive = True

		for i in range(self.enemy_count):
			self.enemies.append(Enemy())


		self.pause_menu = Menu((w//2-40,h//2-(20)*2),(100,60), 30,["PLAY",],[self.resume])
		self.restart_menu = Menu((w//2-40,h//2-(20)*2),(100,60), 30,["RESTART",],[self.restart])


	def update(self):
		if not self.paused:
			self.score+=.2
			pos = self.detector.get_pos()
			pos = (pos[0]*self.w/640,pos[1]*self.h/480)
			self.player.set_target(pos[0],pos[1])
			# self.player.set_target(200,300)
			self.player.update()

			ei = 0
			while ei!=self.enemy_count:
				enemy = self.enemies[ei]
				player = self.player
				damaged_enemy = enemy.hit(self.enemies)
				if enemy.exceeds_boundary(self.w,self.h):
					self.enemies.remove(enemy)
					self.enemies.append(Enemy())
				elif damaged_enemy and enemy.inside_area(0,self.w,0,self.h):
					self.enemies.remove(damaged_enemy)
					self.enemies.remove(enemy)
					self.enemies.extend([Enemy(),Enemy()])
					enemy.damage()
					for i in range(20):
						self.debries.extend([Rocks(enemy.get_pos(),8,color=randint(0,200,size=3)),Rocks(damaged_enemy.get_pos(),8,color=(200,100,50))])
					continue
					# i+=1
				else:
					ei+=1

			di = 0
			while di!=len(self.debries):
				deb = self.debries[di]
				if not deb.alive():
					self.debries.remove(deb)
				else :
					di+=1

			for e in self.enemies:
				e.update()

			for d in self.debries:
				d.update()


#-----------------------------------checking playes's collision with enemies and boundaries-----------------------

			if player.isCollide(self.enemies) or player.exceeds_boundary():
				self.player_alive = False
				self.stop()



	def draw(self,surf):
		pygame.draw.line(surf,(200,200,0),self.player.get_pos(),self.player.get_target(),2)
		pygame.draw.circle(surf,(0,100,200),self.player.get_target(),4)
		self.player.draw(surf)

		for e in self.enemies:
			e.draw(surf)

		for d in self.debries:
			d.draw(surf)

		printText(surf,(20,20),"SCORE: {}".format(int(self.score)), 30)
		printText(surf,(self.w-200 ,20),"HIGHSCORE: {}".format(self.high_score), 30)
		

		if self.paused and self.player_alive:
			self.pause_menu.draw(surf)
		elif not self.player_alive:
			self.restart_menu.draw(surf)


	def checkEvents(self,ev):
		if ev.type == pygame.QUIT:
			self.quit()
		if ev.type == pygame.KEYDOWN:
			if ev.key == pygame.K_ESCAPE:
				self.quit()


		if self.paused and self.player_alive:
			self.pause_menu.checkEvents()
		elif not self.player_alive:
			self.restart_menu.checkEvents()

	def quit(self):
		self.detector.stop()
		sys.exit()

	def resume(self):
		self.paused = False
		self.player.resume()

		for e in self.enemies:
			e.resume()

		for deb in self.debries:
			deb.resume()

	def stop(self):
		self.paused = True
		self.player.stop()

		for e in self.enemies:
			e.stop()

		for deb in self.debries:
			deb.stop()

	def restart(self):
		self.paused = False
		saveScore(int(self.score))
		self.__init__()



def main():
	clock = pygame.time.Clock()
	game = Game()
	screen = game.screen
	while True:
		clock.tick(20)
		for ev in pygame.event.get():
			game.checkEvents(ev)

		screen.fill((0,200,200))
		# if not game.paused:
		game.update()
		game.draw(screen)
		pygame.display.update()

	pygame.QUIT()


if __name__ =="__main__":
	main()