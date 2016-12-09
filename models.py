import arcade.key
import gc
from random import randint,random
import time

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
			print(bullet.x, bullet.y, bullet.vx)
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
				bullet.random();
				print(bullet.x, bullet.y, bullet.vx)

class Bullet(Model):
	def __init__(self, world, x, y, vx, vy):
		super(). __init__(world, x, y)
		self.vx = vx
		self.vy = vy
		self.x = x
		self.y = y
		self.world = world

	def animate(self, delta):
		if (self.x < 0) or (self.x > self.world.width):
			self.vx *= -1
			print(self.vx)


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
		self.vx = 5 * (random() - 0.5)
		self.vy = 5 * random()

class World:
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.player = Player(self, width/2 , 56)
		self.bullets = Bullets(self)
		self.score = 0
		self.start_time = time.time()
		self.current_time = time.time() - self.start_time

	def animate(self, delta):
		self.player.animate(delta)
		self.bullets.animate(delta)
		self.current_time = time.time() - self.start_time


	def on_key_press(self, key, key_modifiers):
		self.player.on_key_press(key,key_modifiers)

	def on_key_release(self, key, key_modifiers):
		self.player.on_key_release(key,key_modifiers)

	


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
			self.x += 5
		if self.direction == Player.DIR_LEFT:
			if self.x < 0:
				self.x = self.world.width
			self.x -= 5
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
		if key == arcade.key.SPACE:
			self.bullets.shoot(self.x, self.y + self.height/2, 0, 3)

	def on_key_release(self, key, key_modifiers):
		if key == arcade.key.LEFT or key == arcade.key.RIGHT:
			if self.isPress == True:
				self.isPress = False
				self.switch_direction("still")
