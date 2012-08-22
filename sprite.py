import pygame
import enemy
import time
import ebullet

def signum(num):
	num = (num / abs(num))
	return num

class Motion(object):
	def __init__(self, max_velocity, initial_vel=0.0, initial_accel=0.0, gravity = 0.0):
		self.velocity = initial_vel
		self.acceleration = initial_accel
		self.max_velocity = max_velocity
		self.gravity = .015
		
	def update(self):
		self.velocity += self.acceleration	
		if abs(self.velocity) > self.max_velocity:
			self.velocity = self.max_velocity *signum(self.velocity)
			

class Sprite(object):
	def __init__(self, Game):
		self.image_width = 110
		self.image_hight = 150
		self.image_frames = 3
		self.Game=Game
		self.motionx = Motion(9)
		self.motiony = Motion(3.5)
		self.images = {}
		self.images[pygame.K_DOWN] = pygame.image.load("charjumpleft.png").convert_alpha() # jump left
		self.images[pygame.K_UP] = pygame.image.load("charjumpright.png").convert_alpha() #jump right
		self.images[pygame.K_LEFT] = pygame.image.load("lmsheet.png").convert_alpha()
		self.images[pygame.K_RIGHT] = pygame.image.load("rmsheet.png").convert_alpha()
		self.rect=pygame.Rect(0,0,self.image_width,self.image_hight)
		self.rect.bottom=Game.screen_rect.bottom - 400
		self.rect.right = Game.screen_rect.right /2
		self.is_moving=[0,0,0,0]#up,down,left,right
		self.frame=0
		self.danimation_rate=40
		self.animation_rate=10
		self.lives=3
		self.animation_counter=0
		self.dimage=self.dimage=pygame.image.load("ld.png")
		self.draw_rect=pygame.Rect(0,0,self.image_width,self.image_hight)
		self.last_horozontal = 0
		self.velocityx = 1
		self.shoot = 0
		self.pie = 0
		
	def d_update(self):
		if self.motionx.velocity>0:
			self.dimage=pygame.image.load("rd.png")
		self.animation_counter+=1
		if self.animation_counter>self.danimation_rate:
			self.danimation_counter=0
			if self.frame>4:
				self.Game.lose() 
			else:
				self.frame+=1
			self.draw_rect.left=self.frame*110
				
	
	def d_draw(self):
		self.Game.screen.blit(self.dimage,self.rect,self.draw_rect)
	
	def update(self):
		if self.rect.right>self.Game.door_rect.centerx+30:
			self.Game.win()
		xcol=self.rect.inflate(-50,-20).move(self.motionx.velocity,0).collidelist(self.Game.objects)
		ycol=self.rect.inflate(-50,-20).move(0,self.motiony.velocity).collidelist(self.Game.objects)
		
		if self.rect.bottom>self.Game.screen_rect.bottom - 165 and (self.rect.centerx>self.Game.hole_rect.right-325 or self.rect.centerx<self.Game.hole_rect.left):
			ycol = -5
			self.motiony.gravity = 0
			self.motiony.velocity = 0 
			self.motiony.acceleration =0
			self.rect.bottom= 735
		if xcol !=-1 and isinstance(self.Game.objects[xcol],enemy.Enemy)==False and isinstance(self.Game.objects[xcol],ebullet.Ebullet)==False:
			self.motionx.velocity=0
		if ycol !=-1 and isinstance(self.Game.objects[ycol],enemy.Enemy)==False and isinstance(self.Game.objects[ycol], ebullet.Ebullet)==False:
			
			if self.motiony.velocity >= 0 and ycol != -5:
				tmp_rect = self.rect.inflate(-50,-20)
				tmp_rect.bottom =  self.Game.objects[ycol].rect.top-1
				self.rect = tmp_rect.inflate(50, 20)
			else:
				self.pie = 1
			self.motiony.velocity=0
			self.motiony.gravity = 0
			self.motiony.acceleration=0
		if (self.rect.left >= self.Game.objects[ycol].rect.right -10 and self.motionx.acceleration > 0 )  or  (self.rect.right <= self.Game.objects[ycol].rect.left +10 and self.motionx.acceleration < 0):
			if len(self.Game.vertical) > 0 :
				self.motiony.gravity = .015
			self.pie = 0
		if (ycol == -1 or ycol >= 1)  and self.pie == 0 :
			self.motiony.gravity = .01
			self.motiony.acceleration += self.motiony.gravity
		if (self.rect.left >= self.Game.objects[ycol].rect.right +10 and self.motionx.acceleration > 0 )  or  (self.rect.right <= self.Game.objects[ycol].rect.left and self.motionx.acceleration < 0):
			if len(self.Game.vertical) > 0 :
				self.motiony.gravity = .015
			else:
				self.motiony.gravity = .05
			self.pie = 0
					
		
		if self.rect.move(self.motionx.velocity, 0).centerx>375 and self.rect.move(self.motionx.velocity, 0).centerx<975 and xcol==-1 and ycol==-1 or self.Game.door_rect.left<self.rect.right:
			self.rect.move_ip(self.velocityx*self.motionx.velocity,0)
		else:
			self.Game.update_objects(self.velocityx*self.motionx.velocity)
		self.Game.background.update_background(self.velocityx*self.motionx.velocity)
		self.velocityx = 1
		if self.rect.right > self.Game.screen_rect.right:
			self.rect.right = self.Game.screen_rect.right
			self.motionx.velocity = 0 
			self.motionx.acceleration =0	
		if self.rect.left<self.Game.screen_rect.left:
			self.rect.left=self.Game.screen_rect.left
			self.motionx.velocity = 0 
			self.motionx.acceleration =0	
		if self.rect.top<self.Game.screen_rect.top:
			self.rect.top=self.Game.screen_rect.top
		if self.rect.bottom>self.Game.screen_rect.bottom - 165 and (self.rect.centerx>self.Game.hole_rect.right-325 or self.rect.centerx<self.Game.hole_rect.left):
			self.motiony.gravity = 0
			self.motiony.velocity = 0 
			self.motiony.acceleration =0
			self.rect.bottom=self.Game.screen_rect.bottom - 165			
		if self.rect.bottom>self.Game.screen_rect.bottom:
			self.Game.game_ending=True
					
		if abs(self.motionx.velocity) > 0 or (len(self.Game.vertical) > 0 and self.motiony.velocity < 0 ):
			self.animation_counter+=1
			if self.animation_counter>self.animation_rate:
				self.animation_counter=0
				self.frame+=1
				if self.frame>self.image_frames -1:
					self.frame=0
				self.draw_rect.left=self.frame*self.image_width
		if self.motiony.velocity != 0 :
			self.motiony.gravity = .015
			if (ycol == -1 or ycol > 1)  and self.pie == 0 :
				self.motiony.gravity = 0
			self.motiony.acceleration += self.motiony.gravity
			self.velocityx = .75
		if self.motionx.velocity != 0.0 :
			self.shoot = signum(self.motionx.velocity) * 1
			if len(self.Game.horozontal) == 0: 
				self.last_horozontal = signum(self.motionx.velocity) * 1
		if (round(abs(self.motionx.velocity)) == 0 or  round(abs(self.motionx.velocity)) == 1) and  len(self.Game.horozontal) == 0:
			self.motionx.velocity = 0
			self.motionx.acceleration = 0
		self.motionx.update()
		self.motiony.update()
		self.rect.move_ip(0,self.motiony.velocity)

	def draw(self):		
		if self.motiony.velocity < 0  and len(self.Game.vertical) > 0 :
			if self.motionx.velocity > 0 :
				self.Game.screen.blit(self.images[pygame.K_UP], self.rect, self.draw_rect)
			elif self.motionx.velocity < 0:
				self.Game.screen.blit(self.images[pygame.K_DOWN], self.rect, self.draw_rect)
			elif self.motionx.velocity == 0:
				if self.last_horozontal ==-1:
					self.Game.screen.blit(self.images[pygame.K_DOWN], self.rect, self.draw_rect)
				elif self.last_horozontal ==1:
					self.Game.screen.blit(self.images[pygame.K_UP], self.rect, self.draw_rect)
				else:
					self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)	
		elif self.motiony.velocity > 0:
			if self.motionx.velocity > 0 :
				self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)
			elif self.motionx.velocity < 0:
				self.Game.screen.blit(self.images[pygame.K_LEFT], self.rect, self.draw_rect)
			elif self.motionx.velocity == 0:
				if self.last_horozontal ==-1:
					self.Game.screen.blit(self.images[pygame.K_LEFT], self.rect, self.draw_rect)
				elif self.last_horozontal ==1:
					self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)
				else:
					self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)	
		elif self.motiony.velocity == 0  :
			if self.motionx.velocity > 0 :
				self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)
			elif self.motionx.velocity < 0:
				self.Game.screen.blit(self.images[pygame.K_LEFT], self.rect, self.draw_rect)
			elif self.motionx.velocity == 0:
				if self.last_horozontal ==-1:
					self.Game.screen.blit(self.images[pygame.K_LEFT], self.rect, self.draw_rect)
				elif self.last_horozontal ==1:
					self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)
				else:
					self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)

			
		else:
			self.Game.screen.blit(self.images[pygame.K_RIGHT], self.rect, self.draw_rect)