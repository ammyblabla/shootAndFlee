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
		self.width = 64
		self.height = 112		

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
		self.bullets = Bullets(self.world);

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
		self.bullets.animate(delta)

	def switch_direction(self, new_direction):
		if new_direction == "left":
			self.direction = Player.DIR_LEFT
		elif new_direction == "right":
			self.direction = Player.DIR_RIGHT
		elif new_direction == "still":
			self.direction = Player.DIR_STILL

	# def shoot(self):
	# 	bullet = Bullet(self.world, self.x, self.y + self.height/2, 0, 3)
	# 	self.bullets.append(bullet)

	def on_key_press(self, key, key_modifiers):
		if key == arcade.key.LEFT:
			self.switch_direction("left")
			self.isPress = True
		if key == arcade.key.RIGHT:
			self.switch_direction("right")
			self.isPress = True
		if key == arcade.key.SPACE:
			self.bullets.shoot(self.x, self.y + self.height/2, 0, 3)
			print("shoot")

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
	def __init__(self, world, x, y, vx, vy):
		super(). __init__(world, x, y)
		self.vx = vx
		self.vy = vy

	def animate(self, delta):
		if (self.x < 0) or (self.x > self.world.width):
			self.vx -= self.vx

		if (self.y < 0) or (self.y > self.world.width):
			self.vy -= self.vy

		self.x += self.vx
		self.y += self.vy

class Bullets():
	def __init__(self, world):
		print("build")
		self.bulletsList = []
		self.world = world

	def animate(self, delta):
		for bullet in self.bulletsList:
			bullet.animate(delta);

	def shoot(self, x, y, vx, vy):
		bullet = Bullet(self.world, x, y, vx, vy)
		self.bulletsList.append(bullet)