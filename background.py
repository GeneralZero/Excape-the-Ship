import pygame
import time
class Background(object):
	def __init__(self, Game):
		self.Game=Game
		pygame.init()
		self.mainsurf=pygame.image.load("BG.png").convert()
		self.rect=self.Game.screen.get_rect()
		self.draw_rect=self.mainsurf.get_rect(width=1350)
		
	def update_background(self,x):
		self.draw_rect.move_ip(.5*x,0)
		if self.draw_rect.right>4050:
			self.draw_rect.left=0
		if self.draw_rect.left<0:
			self.draw_rect.right=4050
	
	def draw(self):
		self.Game.screen.blit(self.mainsurf, self.rect, self.draw_rect )



	