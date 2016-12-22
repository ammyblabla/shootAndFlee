import arcade.key
import gc
from random import randint,random
from time import time

GAME_MENU = 1
GAME_RUNNING = 2
GAME_OVER = 3
GAME_PAUSE = 4
GAME_TIME = 30

class Model:
	def __init__(self,world,x,y):
		self.world = world
		self.x = x
		self.y = y

	def hit(self, other, hit_sizeX, hit_sizeY):
		return (abs(self.x - other.x) <= hit_sizeX) and (abs(self.y - other.y) <= hit_sizeY)

class Bullets():
	NUM_BULLET = 8

	def __init__(self, world):
		self.world = world
		self.bulletsList = []

		for i in range(Bullets.NUM_BULLET):
			bullet = Bullet(self.world, 0, world.height, 0, 0)
			bullet.random()
			# print(bullet.x, bullet.y, bullet.vx)
			self.bulletsList.append(bullet)

	def animate(self, delta):
		for bullet in self.bulletsList:
			bullet.animate(delta)
		self.update()

	def shoot(self, x, y, vx, vy):
		bullet = Bullet(self.world, x, y, vx, vy)
		self.bulletsList.append(bullet)

	def update(self):
		for bullet in self.bulletsList:
			if bullet.is_bullet_out_of_bound():
				bullet.random()

	def addBulletByTime(self):
		if(world.current_time % 1 == 0):
			self.bulletsList.append(self.world, 0, world.height, 0, 0)
			self.bulletsList.append(self.world, 0, world.height, 0, 0)


class Bullet(Model):
	def __init__(self, world, x, y, vx, vy):
		super(). __init__(world, x, y)
		self.vx = vx
		self.vy = vy
		self.x = x
		self.y = y
		self.world = world
		self.speed = 20
		self.random()

	def animate(self, delta):
		if (self.x < 0) or (self.x > self.world.width):
			self.vx *= -1
			# print(self.vx)


		if (self.y < 0) or (self.y > self.world.height):
			self.vy -= self.vy
			self.random()

		self.x += self.vx
		self.y -= self.vy

	def is_bullet_out_of_bound(self):
		if self.y > self.world.height or self.y < 0:
			return True
		return False

	def random(self):
		self.x = 400 * random()
		self.y = self.world.height
		self.vx = self.speed * (random() - 0.5)
		self.vy = self.speed * random()


class World:
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.player = Player(self, width/2 , 56)
		self.current_state = GAME_MENU
		self.current_time = 0
		self.setup()

	def setup(self):
		self.start_time = time()
		self.current_time = (time() - self.start_time)
		self.player.setup()
		self.bullets = Bullets(self)
		self.score = 0
		self.jar = 0

	def animate(self, delta):
		if self.current_state == GAME_RUNNING:
			self.player.animate(delta)
			self.bullets.animate(delta)
			self.current_time = (time() - self.start_time)
			self.jar = (int)(self.score/4)

			if(self.current_time >= GAME_TIME):
				self.current_state = GAME_OVER

		elif self.current_state == GAME_PAUSE:
			self.start_time += delta
		# print(self.current_state)
		# print("start: " + str(self.start_time))
		# print("current: " + str(self.current_time))

	def on_key_press(self, key, key_modifiers):
		self.player.on_key_press(key,key_modifiers)
		self.on_key_press_state(key,key_modifiers)

	def on_key_release(self, key, key_modifiers):
		self.player.on_key_release(key,key_modifiers)

	def on_key_press_state(self, key, key_modifiers):
		if key == arcade.key.SPACE:
			if self.current_state == GAME_RUNNING:
				self.current_state = GAME_PAUSE
			elif self.current_state == GAME_PAUSE:
				self.current_state = GAME_RUNNING
			elif self.current_state == GAME_MENU:
				self.current_state = GAME_RUNNING
				self.start_time = time()
			elif self.current_state == GAME_OVER:
				self.setup()
				self.current_state = GAME_RUNNING

class Player(Model):
	DIR_LEFT = -1
	DIR_STILL = 0
	DIR_RIGHT = 1
	isPress = False

	def __init__(self, world, x, y):
		self.world = world
		self.LIFE = 50
		self.width = 64
		self.height = 112
		self.x = x
		self.y = y
		self.direction = Player.DIR_STILL
		self.isPress = False
		self.bullets = Bullets(self.world);
		self.speed = 20

	def setup(self):
		self.x = self.world.width/2
		self.y = 56

	def animate(self,delta):
		self.move()
		self.bullets.animate(delta)

		for bullet in self.bullets.bulletsList:
			if self.hit(bullet, 20, 60):
				self.world.score += 1
				bullet.random()

	def move(self):
		if self.direction == Player.DIR_RIGHT:
			if self.x > self.world.width:
				self.x = 0
			self.x += self.speed
		if self.direction == Player.DIR_LEFT:
			if self.x < 0:
				self.x = self.world.width
			self.x -= self.speed
		if self.direction == Player.DIR_STILL:
			self.x += 0

	def switch_direction(self, new_direction):
		if new_direction == "left":
			self.direction = Player.DIR_LEFT
		elif new_direction == "right":
			self.direction = Player.DIR_RIGHT
		elif new_direction == "still":
			self.direction = Player.DIR_STILL

	def on_key_press(self, key, key_modifiers):
		if key == arcade.key.LEFT:
			self.switch_direction("left")
			self.isPress = True
		if key == arcade.key.RIGHT:
			self.switch_direction("right")
			self.isPress = True

	def on_key_release(self, key, key_modifiers):
		if key == arcade.key.LEFT or key == arcade.key.RIGHT:
			if self.isPress == True:
				self.isPress = False
				self.switch_direction("still")
