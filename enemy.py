import pygame
import math
import ebullet
class Enemy(object):
	def __init__(self, Game,i,tp,pathnum):
		self.Game=Game
		self.imageleft=pygame.image.load("enemylmsheet.png")
		self.imageright=pygame.image.load("enemyrmsheet.png")
		self.imageshoot=pygame.image.load("enemyshoot.png")
		self.rect=pygame.Rect(0,0,110,150)
		self.rect.bottomleft=tp
		self.is_moving=[0,0,0,1]#up,down,left,right
		self.speed=5
		self.frame=0
		self.i=i
		self.animation_rate=10
		self.lives=3
		self.imagetemp=self.imageleft
		self.animation_counter=0
		self.draw_rect=pygame.Rect(0,0,110,150)
		self.path_dist=0
		self.pathnum=pathnum
		self.moved=0
		self.is_shooting=False
		self.wait_shoot=30
	
	def eshoot(self):
		d=0
		if self.is_moving[3]==1:
			d='r'
		else:
			d='l'
		tempb=ebullet.Ebullet(self,self.rect.midright,self.rect.midleft,d)
		self.Game.bullet_list.append(tempb)
		self.Game.objects.append(tempb)
	
	
	def update(self):
		self.wait_shoot-=1
		dist=self.rect.centery-self.Game.sprite.rect.centery
		if (dist<25 and dist>-25) and ((self.is_moving[3]==1 and self.rect.centerx<self.Game.sprite.rect.centerx) or (self.is_moving[2]==1 and self.rect.centerx>self.Game.sprite.rect.centerx)) and self.wait_shoot<0 and abs(self.rect.centerx-self.Game.sprite.rect.centerx)<700 and self.Game.game_ending!=True:
			self.is_shooting=True
		
		if self.is_moving[3]==1:
			self.rect.move_ip(self.speed,0)
			self.imagetemp=self.imageright
			self.moved+=1
			if self.moved>self.pathnum:
				self.moved=0
				self.is_moving=[0,0,1,0]
		if self.is_moving[2]==1:
			self.rect.move_ip(-self.speed,0)
			self.imagetemp=self.imageleft
			self.moved+=1
			if self.moved>self.pathnum:
				self.moved=0
				self.is_moving=[0,0,0,1]
		if self.is_shooting and self.wait_shoot<0:
			self.imagetemp=self.imageshoot
			self.eshoot()
			self.wait_shoot=25
			self.is_shooting=False
			
		if self.is_moving[0]==1 or self.is_moving[1]==1 or self.is_moving[2]==1 or self.is_moving[3]==1:
			self.animation_counter+=1
			if self.animation_counter>self.animation_rate:
				self.animation_counter=0
				self.frame+=1
				if self.frame>3:
					self.frame=0
				self.draw_rect.left=self.frame*110
		else:
			self.frame=0
			self.draw_rect.left=self.frame*110
	def draw(self):
		self.Game.screen.blit(self.imagetemp, self.rect, self.draw_rect)
			