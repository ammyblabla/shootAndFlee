import arcade
import arcade.key

from models import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GAME_MENU = 1
GAME_RUNNING = 2
GAME_OVER = 3
GAME_PAUSE = 4

GAME_TIME = 30

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)


    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
    	super().__init__(width, height)

    	arcade.set_background_color(arcade.color.BLACK)

    	self.world = World(width, height)
    	self.player_sprite = ModelSprite('images/jar1.png',model=self.world.player)
    	self.background = arcade.load_texture("images/background.jpg")
    	self.bullet_sprites = []

    	self.current_state = GAME_MENU

    def on_draw(self):     
    	arcade.start_render()
    	arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT //2,self.background.width,self.background.height, self.background, 0)

    	if self.world.current_state == GAME_MENU:
            self.draw_menu()
    	elif self.world.current_state == GAME_RUNNING:
        	self.draw_game()
    	elif self.world.current_state == GAME_PAUSE:
        	self.draw_pause()
    	else:
    		self.draw_game_over()
    		self.setup()

    def setup(self):
    	# del self.bullet_sprites[:]
    	self.bullet_sprites.clear()

    def draw_game(self):
    	self.update()
    	# self.player_sprite.draw()
    	self.draw_player()
    	for sprite in self.bullet_sprites:
    		sprite.draw()
    	arcade.draw_text("time: "+str(GAME_TIME - round(self.world.current_time,2)), self.width-155, self.height-30, arcade.color.WHITE, 20)	
    	arcade.draw_text("Jar: "+str(self.world.jar), self.width-155, self.height-60, arcade.color.WHITE, 20)

    def draw_player(self):
    	jar = self.world.score % 4
    	self.player_sprite = ModelSprite('images/jar'+str(self.world.score%4)+'.png',model=self.world.player)
    	self.player_sprite.draw()

    def draw_game_over(self):
        output = "Game Over"
        arcade.draw_text(output, 175, 400, arcade.color.WHITE, 36)

        output = "Space to restart"
        arcade.draw_text(output, 175, 300, arcade.color.WHITE, 24)

        output = "Jar: " + str(self.world.jar)
        arcade.draw_text(output, 175, 200, arcade.color.WHITE, 24)

    def draw_pause(self):
        output = "Pause"
        arcade.draw_text(output, 150, 400, arcade.color.WHITE, 36)

    def draw_menu(self):
        output = "water jar game"
        arcade.draw_text(output, 125, 400, arcade.color.WHITE, 36)

    def animate(self, delta):
    	self.world.animate(delta)

    def on_key_press(self, key, key_modifiers):
    	self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
    	self.world.on_key_release(key, key_modifiers)

    def update(self):
    	for bullet in self.world.bullets.bulletsList:
    		if bullet.isToxic == False:
        		self.bullet_sprites.append(ModelSprite('images/bullet.png',model=bullet))
    		elif bullet.isToxic == True:
        		self.bullet_sprites.append(ModelSprite('images/bullet_toxic.png',model=bullet))

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
