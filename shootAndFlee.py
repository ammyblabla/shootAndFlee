import arcade
 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
 
class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
    	super().__init__(width, height)

    	arcade.set_background_color(arcade.color.BLACK)
    	
    	self.player = arcade.Sprite('images/rocket1.png')
    	self.player.set_position(100, 100)

    def on_draw(self):
    	arcade.start_render()
    	self.player.draw()

    def animate(self, delta):
    	player = self.player

    	if player.center_x > SCREEN_WIDTH:
    		player.center_x = 0
    	self.player.set_position(self.player.center_x + 5, self.player.center_y)

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()