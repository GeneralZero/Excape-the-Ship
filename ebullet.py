import pygame
class Ebullet(object):
	def __init__(self, enemy,mr,ml,d):
		self.enemy=enemy
		self.image=pygame.image.load("energyright.png")
		self.speed=15
		self.traveled=0
		self.wait=4
		self.rect=self.image.get_rect(width=75)
		self.rect.topleft=mr
		self.d=d
		self.draw_rect=self.image.get_rect(width=75)
		if self.d=='l':
			self.image=pygame.image.load("energyleft.png")
			self.rect.topright=ml
	def update(self):
		self.wait-=1
		if self.wait<0:
			if self.draw_rect.left==0:
				self.draw_rect.left=75
			else:
				self.draw_rect.left=0
		if self.d=='l':
			self.rect.move_ip(-self.speed,0)
		else:
			self.rect.move_ip(self.speed,0)
		
	def draw(self):
		self.Game.screen.blit(self.image,self.rect,self.draw_rect)
	def update(self):
		self.wait-=1
		if self.wait<0:
			if self.draw_rect.left==0:
				self.draw_rect.left=75
			else:
				self.draw_rect.left=0
		if self.d=='l':
			self.rect.move_ip(-self.speed,0)
		else:
			self.rect.move_ip(self.speed,0)
	def draw(self):
		self.enemy.Game.screen.blit(self.image,self.rect)