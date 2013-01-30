import pygame
import platforms
import sprite
import enemy
import bullet
import ebullet
import background
import menu
import time
import os


class Game(object):
	def __init__(self):
		os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'
		pygame.init()
		self.screen = pygame.display.set_mode((1350,900), pygame.FULLSCREEN)
		self.clock=pygame.time.Clock()
		self.screen_rect=self.screen.get_rect()
		self.hole_image=pygame.image.load('Images/largepit.png')
		
		self.door=pygame.image.load('Images/door.png')

		self.blacksquare=pygame.image.load('Images/black.png')
		self.menu=menu.Menu(self)
		
		self.background=background.Background(self)
		self.reset()
	
	def reset(self):
		self.hole_rect=self.hole_image.get_rect()
		self.hole_rect.topleft=(4613,720)
		self.door_rect=self.door.get_rect()
		self.door_rect.topleft=(9200,0)
		self.bullet_list=[]
		self.vertical = []
		self.horozontal = []
		self.objects=[]
		self.enemy_list=[]
		self.create_world()
		self.game_ending=False
		self.create_enemy()
		self.wait_shoot=0
		self.game_over=False
		self.game_menu =True
		self.sprite=sprite.Sprite(self)

	def shoot(self):
		self.wait_shoot=30
		d='r'
		if self.sprite.shoot == -1:
			d='l'
		tempb=bullet.Bullet(self,d)
		self.bullet_list.append(tempb)
		self.objects.append(tempb)
	
	
	def create_world(self):
		self.objects.append(platforms.Platforms(self, 'b',(1175,630)))
		self.objects.append(platforms.Platforms(self, 'p',(1415,497)))
		self.objects.append(platforms.Platforms(self, 'p',(2069,630)))
		self.objects.append(platforms.Platforms(self, 'b',(2344,525)))
		self.objects.append(platforms.Platforms(self, 'p',(2575,400)))
		self.objects.append(platforms.Platforms(self, 'p',(3325,400)))
		self.objects.append(platforms.Platforms(self, 'p',(3725,400)))
		self.objects.append(platforms.Platforms(self, 'b',(4513,630)))
		self.objects.append(platforms.Platforms(self, 'b',(4868,630)))
		self.objects.append(platforms.Platforms(self, 'p',(5320,665)))
		self.objects.append(platforms.Platforms(self, 'b',(5722,630)))
		self.objects.append(platforms.Platforms(self, 'b',(5822,630)))
		self.objects.append(platforms.Platforms(self, 'p',(5920,665)))
		self.objects.append(platforms.Platforms(self, 'p',(5920,590)))
		self.objects.append(platforms.Platforms(self, 'b',(6305,630)))
		self.objects.append(platforms.Platforms(self, 'p',(6652,458)))
		self.objects.append(platforms.Platforms(self, 'b',(6892,348)))
		self.objects.append(platforms.Platforms(self, 'p',(7182,458)))
		self.objects.append(platforms.Platforms(self, 'b',(7844,630)))
		self.objects.append(platforms.Platforms(self, 'b',(7944,630)))
		self.objects.append(platforms.Platforms(self, 'b',(8042,630)))
		self.objects.append(platforms.Platforms(self, 'b',(7944,520)))
		self.objects.append(platforms.Platforms(self, 'b',(8042,520)))
		self.objects.append(platforms.Platforms(self, 'b',(8042,410)))
		self.objects.append(platforms.Platforms(self, 'p',(8272,410)))
		self.objects.append(platforms.Platforms(self, 'b',(8786,630)))
		
	def do_en(self,e):
		self.enemy_list.append(e)
		self.objects.append(e)
	
	def create_enemy(self):
		self.do_en(enemy.Enemy(self,0,(1470,742),90))
		self.do_en(enemy.Enemy(self,1,(2625,735),90))
		self.do_en(enemy.Enemy(self,2,(3900,740),90))
		self.do_en(enemy.Enemy(self,3,(7200,460),60))
		self.do_en(enemy.Enemy(self,4,(8270,740),90))
		
		
		
	def process_input(self):
		if self.sprite.lives<0:
			self.game_over=True
		events=pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.game_over = True
				elif event.key == pygame.K_RIGHT:
					self.horozontal.append(pygame.K_RIGHT)
					self.sprite.motionx.acceleration = .5
				elif event.key == pygame.K_LEFT:
					self.horozontal.append(pygame.K_LEFT)
					self.sprite.motionx.acceleration = -.5
				elif event.key == pygame.K_UP:
					self.vertical.append(pygame.K_UP)
					self.sprite.motiony.acceleration -= .5
				elif event.key == pygame.K_SPACE and self.wait_shoot<0:
					self.shoot()

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					self.horozontal.remove(pygame.K_RIGHT)
					self.sprite.motionx.acceleration = -.5
				elif event.key == pygame.K_LEFT:
					self.horozontal.remove(pygame.K_LEFT)
					self.sprite.motionx.acceleration = .5
				elif event.key == pygame.K_UP:
					self.vertical.remove(pygame.K_UP)
					self.sprite.motiony.acceleration += .6
					
	def update_objects(self,x):
		for o in self.objects:
			o.rect.move_ip(-x,0)
		self.hole_rect.move_ip(-x,0)
		self.door_rect.move_ip(-x,0)
	
	def update_world(self):
		self.music_gamePlay = pygame.mixer.music.play(-1)
		if self.game_ending==True:
			self.sprite.d_update()
		else:
			self.sprite.update()
		self.wait_shoot-=1
		colliding_bullets=[]
		for b in self.bullet_list:
			bcol=b.rect.collidelist(self.objects)
			if bcol!=-1 and isinstance(self.objects[bcol],platforms.Platforms)==True:
				self.bullet_list.remove(b)
				self.objects.remove(b)
		for b in self.bullet_list:
			b.update()
			colliding_bullets=sorted(b.rect.collidelistall(self.bullet_list), reverse=True)
			if len(colliding_bullets)>1:
				for c in colliding_bullets:
					self.objects.remove(self.bullet_list[c])
					del self.bullet_list[c]
			if b.rect.right>self.screen.get_rect().right or b.rect.left<self.screen.get_rect().left:
				self.bullet_list.remove(b)
				self.objects.remove(b)
			if b.rect.colliderect(self.sprite.rect):
				self.bullet_list.remove(b)
				self.objects.remove(b)
				self.game_ending=True
		for e in self.enemy_list:
			e.update()
			ekill_bullets=sorted(e.rect.collidelistall(self.bullet_list), reverse=True)
			if len(ekill_bullets)!=0:
				for ek in ekill_bullets:
					self.objects.remove(self.bullet_list[ek])
					del self.bullet_list[ek]
					self.objects.remove(e)
					self.enemy_list.remove(e)
		
	def win(self):
		win=pygame.image.load("Images/win.png")
		win_rect=win.get_rect()
		win_rect.topleft=(0,0)
		self.screen.blit(win,win_rect)
		pygame.display.flip()
		pygame.time.wait(4000)
		
		self.game_menu =True
		self.reset()
				
	def lose(self):
		lose=pygame.image.load("Images/gameover.png")
		lose_rect=lose.get_rect()
		lose_rect.topleft=(0,0)
		self.screen.blit(lose,lose_rect)
		pygame.display.flip()
		pygame.time.wait(4000)
		self.game_menu =True
		self.reset()
	
	def draw_world(self):
		self.background.draw()
		self.screen.blit(self.door,self.door_rect)
		self.screen.blit(self.hole_image,self.hole_rect)
		
		for o in self.objects:
			o.draw()
		if self.game_ending==True:
			self.sprite.d_draw()
		else:
			self.sprite.draw()
		self.screen.blit(self.blacksquare,self.door_rect)	
		pygame.display.flip()
game=Game()
while game.game_over==False:
	while game.game_over==False and game.game_menu ==True :
		game.menu.update()
		game.menu.process_input()
	game.clock.tick(50)
	game.process_input()
	game.update_world()
	game.draw_world()

	
