import pygame

class Platforms(object):
	def __init__(self,Game,bp,tp):
		self.Game=Game
		if bp=='b':
			self.image=pygame.image.load("Images/box2.png")
		if bp == 'p':
			self.image=pygame.image.load("Images/pipe2.png")
		if bp == 's':
			self.image=pygame.image.load("Images/boxfun.png")
		if bp == 'sh':
			self.image=pygame.image.load("Images/smallpit.png")
		if bp == 'lh':
			self.image=pygame.image.load("Images/largepit.png")
		self.rect=self.image.get_rect()
		self.rect.topleft=tp
	def draw(self):
		self.Game.screen.blit(self.image,self.rect)
