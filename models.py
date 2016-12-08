import arcade.key

class Model:
	def __init__(self,world,x,y):
		self.world = world
		self.x = x
		self.y = y

class Charactor(Model):
	def __init__(self, world, x, y):
		super().__init__(world,x,y)
		self.world = world
		self.x = x
		self.y = y
		self.bullets = []


class World:
	NUM_ENEMY = 8

	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.player = Player(self, width/2 , 56)
		
		self.enemies = []
		self.NUM_ENEMY = 8
		no_enemy = 0
		
		for i in range(World.NUM_ENEMY):
			enemy = Enemy(self, no_enemy * width / World.NUM_ENEMY + 32, height - 32)
			self.enemies.append(enemy)
			no_enemy += 1

	def animate(self, delta):
		self.player.animate(delta)

	def on_key_press(self, key, key_modifiers):
		self.player.on_key_press(key,key_modifiers)

	def on_key_release(self, key, key_modifiers):
		self.player.on_key_release(key,key_modifiers)

class Player(Charactor):
	DIR_LEFT = -1
	DIR_STILL = 0
	DIR_RIGHT = 1
	isPress = False

	def __init__(self, world, x, y):
		super().__init__(world,x,y)
		self.world = world
		self.x = x
		self.y = y
		self.direction = Player.DIR_STILL
		self.isPress = False

	def animate(self,delta):
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
		if key == arcade.key.RIGHT:
			self.switch_direction("right")
		self.isPress = True

	def on_key_release(self, key, key_modifiers):
		if key == arcade.key.LEFT or key == arcade.key.RIGHT:
			if self.isPress == True:
				self.isPress = False
				self.switch_direction("still")

class Enemy(Charactor):
	def __init__(self, world, x, y):
		super().__init__(world,x,y)
		self.world = world
		self.x = x
		self.y = y

class Bullet(Model):
	def __init__(self, world, x, y):
		super(). __init__(world, x, y, 0)
		self.vx = 1
		self.vy = 1
	
	def animate(self, delta):
		if (self.x < 0) or (self.x > self.world.width):
			self.vx -= self.vx

		if (self.y < 0) or (self.y > self.world.width):
			self.vy -= self.vy

		self.x += self.vx
		self.y += self.vy

