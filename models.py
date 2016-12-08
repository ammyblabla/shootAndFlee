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


class World:
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.player = Player(self, width/2 , 0)
		self.enemy = Enemy(self, width/2, height)

	def animate(self, delta):
		self.player.animate(delta)

	def on_key_press(self, key, key_modifiers):
		if key == arcade.key.LEFT:
			self.player.switch_direction("left")
		if key == arcade.key.RIGHT:
			self.player.switch_direction("right")
		self.player.isPress = True

	def on_key_release(self, key, key_modifiers):
		if key == arcade.key.LEFT or key == arcade.key.RIGHT:
			if self.player.isPress == True:
				self.player.isPress = False
				self.player.switch_direction("still")

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

class Enemy(Charactor):
	def __init__(self, world, x, y):
		super().__init__(world,x,y)
		self.world = world
		self.x = x
		self.y = y

