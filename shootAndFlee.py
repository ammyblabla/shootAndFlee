import arcade
import arcade.key

from models import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

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
    	self.player_sprite = ModelSprite('images/rocket1.png',model=self.world.player)

    	self.bullet_sprites = []

    def on_draw(self):
    	arcade.start_render()
    	self.update()
    	self.player_sprite.draw()
    	for sprite in self.bullet_sprites:
    		sprite.draw()
    	arcade.draw_text("score: "+str(self.world.score), self.width-150, self.height-30, arcade.color.WHITE, 20)
    	arcade.draw_text("time: "+str(round(self.world.current_time,2)), self.width-150, self.height-60, arcade.color.WHITE, 20)


    def animate(self, delta):
    	self.world.animate(delta)

    def on_key_press(self, key, key_modifiers):
    	self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
    	self.world.on_key_release(key, key_modifiers)

    def update(self):
    	for bullet in self.world.player.bullets.bulletsList:
        	self.bullet_sprites.append(ModelSprite('images/bullet.png',model=bullet))

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
