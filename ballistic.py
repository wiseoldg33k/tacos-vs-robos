import arcade
import os
import math


SCREEN_WIDTH = 800 * 3
SCREEN_HEIGHT = 600 * 3
SCREEN_TITLE = "Tacos vs Robos"

TACOS_SCALE_FACTOR = .10
ROCK_SCALE_FACTOR = .3
CROSSHAIR_SCALING = .2
SPRITE_SCALING_LASER = 1

GROUND_LEVEL = SCREEN_HEIGHT // 18

BULLET_SPEED = 35


class Player(arcade.Sprite):

    def update(self):
        super().update()

class Projectile(arcade.Sprite):

    def update(self):
        super().update()

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AMAZON)

        self.score = 0
        self.remaining_tacos = 5


    def spawn_tacos(self, x, y, angle, x_diff, y_diff):
        tacos = Projectile('tacos.png', TACOS_SCALE_FACTOR)
        tacos.center_x = x
        tacos.center_y = y
        tacos.angle = math.degrees(angle)

        self.bullet_list.append(tacos)

        speed_x, speed_y = self.get_speed()
        tacos.change_x = math.cos(angle) * speed_x
        tacos.change_y = math.sin(angle) * speed_y

        tacos.physics_engine = arcade.PhysicsEnginePlatformer(tacos, self.wall_list, 0.1)

    def get_speed(self):
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y

        dest_x = self.crosshair_sprite.center_x
        dest_y = self.crosshair_sprite.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        speed_x = BULLET_SPEED * (x_diff / SCREEN_WIDTH)
        speed_y = BULLET_SPEED * (y_diff / SCREEN_HEIGHT)
        return speed_x, speed_y
    
    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.crosshair_sprite.center_x = x
        self.crosshair_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse moves.
        """

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y

        dest_x = x
        dest_y = y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        if -70 <= math.degrees(angle) < 90:
            if self.remaining_tacos > 0:
                self.remaining_tacos -= 1
                self.spawn_tacos(start_x, start_y, angle, x_diff, y_diff)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        
        zombie = Player('character_zombie_idle.png')
        zombie.center_x = SCREEN_WIDTH // 10
        zombie.bottom = GROUND_LEVEL
        self.player_list.append(zombie)
        self.player_sprite = zombie

        robot = Player('character_robot_idle.png')
        robot.center_x = 9 * SCREEN_WIDTH // 10
        robot.bottom = GROUND_LEVEL
        self.player_list.append(robot)
        self.opponent_sprite = robot

        self.crosshair_sprite = arcade.Sprite("crosshair.png", CROSSHAIR_SCALING)
        self.player_list.append(self.crosshair_sprite)


        rock = arcade.Sprite('rock_2.png', ROCK_SCALE_FACTOR)
        rock.center_x = SCREEN_WIDTH // 2
        rock.bottom = GROUND_LEVEL // 2
        self.obstacle_list.append(rock)
        self.obstacle = rock
        

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.obstacle_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()

        output = f"Score: {self.score} | Remaining tacos: {self.remaining_tacos}"
        arcade.draw_text(output, SCREEN_WIDTH//3, SCREEN_HEIGHT * .9, arcade.color.BLACK, 24)

        if self.remaining_tacos <= 0:
            arcade.draw_text('GAME OVER', SCREEN_WIDTH//3, SCREEN_HEIGHT //2, arcade.color.RED, 74, bold=True)


    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        for bullet in self.bullet_list:

            bullet.physics_engine.update()

            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.kill()

            if arcade.check_for_collision(bullet, self.obstacle):
                bullet.kill()
                
            if arcade.check_for_collision(bullet, self.opponent_sprite):
                self.score += 1
                bullet.kill()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()