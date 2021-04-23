"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

This is the program for breakout.py to import
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel, GLine
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
from campy.gui.events.timer import pause
from campy.graphics.gimage import GImage

# Constants
BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 15  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 111  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 60  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.

NUM_LIVES = 5  # Number of attempts

# Global variables
score = 0


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):
        self.__ball_radius = ball_radius
        self.__paddle_offset = paddle_offset
        self.__times = 0
        self.__brick_cols = brick_cols
        self.__brick_rows = brick_rows
        self.win = False   # to verify the status of win
        self.lose = False  # to verify the status of lose
        self.__paddle_width = paddle_width
        self.__paddle_height = paddle_height
        self.__count = 0     # count for attack
        self.win_label = GLabel('You Win the Game!')
        self.attack = GLabel('ATTACK: ' + str(20 - self.__count))
        self.level_2_label = GLabel('LEVEL 2')
        self.drop = GRect(10, 25)
        self.img = GImage('godzilla.jpeg')    # import img
        self.attack_bricks = []               # list for random bricks
        self.__drop_vx = 0                      # bricks' vx
        self.__drop_vy = random.randint(3, 10)  # bricks' vy

        # Create a graphical window, with some extra space
        self.__window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.__window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.__window_width, height=self.__window_height, title='BREAKOUT GAME')

        # Run animation of loading
        self.loading()

        # Draw bricks
        brick_x = 0
        brick_y = BRICK_OFFSET
        for i in range(self.__brick_rows):
            pause(10)
            brick_y += brick_height + brick_spacing
            for j in range(self.__brick_cols):
                pause(10)
                brick_x = j * (brick_width + brick_spacing)
                brick = GRect(brick_width, brick_height, x=brick_x, y=brick_y)
                brick.filled = True
                brick.color = 'white'
                brick.fill_color = 'tomato'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 2:
                    brick.fill_color = 'coral'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 3:
                    brick.fill_color = 'darkorange'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 4:
                    brick.fill_color = 'gold'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 5:
                    brick.fill_color = 'yellowgreen'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 6:
                    brick.fill_color = 'mediumseagreen'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 7:
                    brick.fill_color = 'cornflowerblue'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 8:
                    brick.fill_color = 'steelblue'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 9:
                    brick.fill_color = 'mediumpurple'
                if (brick.y - brick_offset) / (brick_height + brick_spacing) >= 10:
                    brick.fill_color = 'orchid'
                self.window.add(brick)

        # Create a paddle
        pause(30)
        self.__paddle = GRect(paddle_width, paddle_height, x=(self.__window_width - paddle_width) // 2,
                            y=self.__window_height - paddle_offset - paddle_height)
        self.__paddle.filled = True
        self.__paddle.color = 'slategray'
        self.__paddle.fill_color = 'slategray'
        self.window.add(self.__paddle)

        # Center a filled ball in the graphical window
        pause(30)
        self.__ball = GOval(ball_radius * 2, ball_radius * 2, x=(self.__window_width - ball_radius * 2) // 2,
                          y=(self.__window_height - ball_radius * 2) // 2)
        self.__ball.filled = True
        self.__ball.color = 'rosybrown'
        self.__ball.fill_color = 'rosybrown'
        self.window.add(self.__ball)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners
        onmouseclicked(self.start)
        onmousemoved(self.follow)

        # Create a score board
        pause(30)
        self.score_label = GLabel('SCORE: ' + str(score))
        self.score_label.font = 'Helvetica-20-bold'
        self.score_label.color = 'darkslateblue'
        self.window.add(self.score_label, x=20, y=self.__window_height - 10)

        # Create lives board
        pause(30)
        self.chance = GOval(20, 20)
        live = GLabel('LIVES: ')
        live.font = 'Helvetica-20-bold'
        live.color = 'tomato'
        self.window.add(live, x=self.__window_width - 300 - self.chance.width, y=self.__window_height - 10)
        self.__chance_y = self.__window_height - 38
        for i in range(NUM_LIVES):
            self.__chance_x = self.__window_width - 230 + i * (self.chance.width + 15)
            self.chance = GOval(25, 25, x=self.__chance_x, y=self.__chance_y)
            self.chance.filled = True
            self.chance.color = 'tomato'
            self.chance.fill_color = 'tomato'
            self.window.add(self.chance)

        # Create level board
        pause(30)
        self.level_1 = GLabel('LEVEL 1')
        self.level_1.font = 'Helvetica-20-bold'
        self.level_1.color = 'indianred'
        self.window.add(self.level_1, x=(self.window.width - self.level_1.width) // 2, y=37)

        # Create line above the brick offset
        pause(30)
        self.line = GLine(0, BRICK_OFFSET - 5, self.__window_width, BRICK_OFFSET - 5)
        self.line.color = 'dimgray'
        self.window.add(self.line)

    def follow(self, event):
        """
        The mouse event that make the paddle follow the mouse
        """
        if self.window.width - self.__paddle.width // 2 >= event.x >= self.__paddle.width // 2:
            self.__paddle.x = event.x - self.__paddle.width // 2

    def start(self, event):
        """
        The mouse event that start the breakout game by a mouse click
        """
        # If not win
        if self.__times != NUM_LIVES:
            # if the ball is at the start position
            if self.__ball.x == (self.window.width - self.__ball_radius * 2) // 2 and \
                    self.__ball.y == (self.window.height - self.__ball_radius * 2) // 2 or \
                    self.__ball.x == (
                    self.__window_width - self.__ball.width) // 2 and self.__ball.y == self.__paddle_offset - 50:
                # To create random velocity
                self.__dx = random.randint(1, MAX_X_SPEED)
                self.__dy = INITIAL_Y_SPEED
                if random.random() > 0.5:
                    self.__dx = -self.__dx

    def win_or_lose(self):
        """
        The function to check the player is win or lose
        """
        # If hasn't win and hasn't lose
        if score != self.__brick_rows * self.__brick_cols and self.__times != NUM_LIVES:
            pass
        else:
            # If is win
            if score == self.__brick_rows * self.__brick_cols:
                self.win = True
                self.win_label.font = 'Helvetica-60-bold'
                self.win_label.color = 'darkslategrey'
                self.window.add(self.win_label, x=(self.__window_width - self.win_label.width) // 2,
                                y=self.__window_height // 2)
                self.window.remove(self.__ball)
                pause(1000)
                self.window.remove(self.win_label)
            # If is lose
            elif self.__times == NUM_LIVES:
                self.lose = True
                lose_label = GLabel('Game Over :(')
                lose_label.font = 'Helvetica-60-bold'
                lose_label.color = 'darkslategrey'
                self.window.add(lose_label, x=(self.__window_width - lose_label.width) // 2,
                                y=(self.__window_height * 1.5 - lose_label.height) // 2)

    def final_score_board(self):
        """
        The function that create a final score board
        """
        self.window.clear()
        score_board = GLabel('SCORE BOARD')
        score_board.color = 'maroon'
        score_board.font = 'Helvetica-40-bold'
        self.window.add(score_board, x=(self.__window_width - score_board.width) // 2, y=self.__window_height // 5.5)
        score_1 = 300
        score_2 = 250
        score_3 = 150
        score_4 = 100
        score_5 = 50
        score_1_label = GLabel('1..............................' + str(score_1))
        score_2_label = GLabel('2..............................' + str(score_2))
        score_3_label = GLabel('3..............................' + str(score_3))
        score_4_label = GLabel('4..............................' + str(score_4))
        score_5_label = GLabel('5..............................' + str(score_5))
        score_1_label.font = 'Helvetica-30-bold'
        score_2_label.font = 'Helvetica-30-bold'
        score_3_label.font = 'Helvetica-30-bold'
        score_4_label.font = 'Helvetica-30-bold'
        score_5_label.font = 'Helvetica-30-bold'
        score_1_label.color = 'slategray'
        score_2_label.color = 'slategray'
        score_3_label.color = 'slategray'
        score_4_label.color = 'slategray'
        score_5_label.color = 'slategray'
        space = 50
        self.window.add(score_1_label, x=self.__window_width // 4, y=(score_board.y + space) * 1.3)
        self.window.add(score_2_label, x=self.__window_width // 4, y=(score_board.y + space) * 1.8)
        self.window.add(score_3_label, x=self.__window_width // 4, y=(score_board.y + space) * 2.3)
        self.window.add(score_4_label, x=self.__window_width // 4, y=(score_board.y + space) * 2.8)
        self.window.add(score_5_label, x=self.__window_width // 4, y=(score_board.y + space) * 3.3)
        # Check the final score is bigger than which score and substitute it
        # ( A small question: the .text attribute is not work )
        if score >= score_1:
            score_1 = score
            # score_1_label.text = '1..............................' + str(score_1)
            self.window.remove(score_1_label)
            score_1_label_new = GLabel('1..............................' + str(score_1))
            score_1_label_new.color = 'crimson'
            score_1_label_new.font = 'Helvetica-30-bold'
            self.window.add(score_1_label_new, x=self.__window_width // 4, y=(score_board.y + space) * 1.3)
        elif score >= score_2:
            score_2 = score
            self.window.remove(score_2_label)
            score_2_label_new = GLabel('2..............................' + str(score_2))
            score_2_label_new.color = 'crimson'
            score_2_label_new.font = 'Helvetica-30-bold'
            self.window.add(score_2_label_new, x=self.__window_width // 4, y=(score_board.y + space) * 1.8)
        elif score >= score_3:
            score_3 = score
            self.window.remove(score_3_label)
            score_3_label_new = GLabel('3..............................' + str(score_3))
            score_3_label_new.color = 'crimson'
            score_3_label_new.font = 'Helvetica-30-bold'
            self.window.add(score_3_label_new, x=self.__window_width // 4, y=(score_board.y + space) * 2.3)
        elif score >= score_4:
            score_4 = score
            self.window.remove(score_4_label)
            score_4_label_new = GLabel('4..............................' + str(score_4))
            score_4_label_new.color = 'crimson'
            score_4_label_new.font = 'Helvetica-30-bold'
            self.window.add(score_4_label_new, x=self.__window_width // 4, y=(score_board.y + space) * 2.8)
        else:
            score_5 = score
            # Not sure why the label can not use text method to change
            # score_1_label.text = '1..............................' + str(score_1)
            self.window.remove(score_5_label)
            score_5_label_new = GLabel('5..............................' + str(score_5))
            score_5_label_new.color = 'crimson'
            score_5_label_new.font = 'Helvetica-30-bold'
            self.window.add(score_5_label_new, x=self.__window_width // 4, y=(score_board.y + space) * 3.3)

    def paddle_or_bricks(self):
        """
        Identify the ball hits the paddle or bricks
        if paddle, change the ball's dy to -dy
        if bricks, remove the bricks and change the ball's dy to -dy
        """
        global score
        if not self.win:  # Win = False
            if self.__ball.y > self.window.height // 2:  # If the ball is at the lower side
                self.__dy = -self.__dy
            if self.__ball.y < self.window.height // 2:  # If the ball is at the upper side
                if self.window.remove(self.window.get_object_at(self.__ball.x, self.__ball.y)) or \
                        self.window.remove(
                            self.window.get_object_at(self.__ball.x + self.__ball_radius * 2, self.__ball.y)) or \
                        self.window.remove(
                            self.window.get_object_at(self.__ball.x, self.__ball.y + self.__ball_radius * 2)) or \
                        self.window.remove(self.window.get_object_at(self.__ball.x + self.__ball_radius * 2,
                                                                     self.__ball.y + self.__ball_radius * 2)):
                    score += 1
                    self.score_label.text = 'SCORE: ' + str(score)  # Change score
                self.__dy = -1.005 * self.__dy
            if score == (self.__brick_rows * self.__brick_cols) // 2:  # To verify the qualification of next level
                self.window.remove(self.level_1)
                self.level_2()

    def collision(self):
        """
        Check for collision by 4 point (ball.x,ball.y), (ball.x + ball_radius, ball.y),
        (ball.x, ball_radius+ball.y), and (ball.x + ball_radius, ball_radius+ball.y)
        """
        if self.__ball.y >= PADDLE_OFFSET:
            if self.window.get_object_at(self.__ball.x, self.__ball.y) is not None:
                if score >= 150:
                    self.paddle_or_godzilla()
                else:
                    self.paddle_or_bricks()
            elif self.window.get_object_at(self.__ball.x + self.__ball_radius * 2, self.__ball.y) is not None:
                if score >= 150:
                    self.paddle_or_godzilla()
                else:
                    self.paddle_or_bricks()
            elif self.window.get_object_at(self.__ball.x, self.__ball.y + self.__ball_radius * 2) is not None:
                if self.window.get_object_at(self.__ball.x + self.__ball_radius * 2,
                                             self.__ball.y + self.__ball_radius * 2) is not None:
                    if score >= 150:
                        self.paddle_or_godzilla()
                    else:
                        self.paddle_or_bricks()
            elif self.window.get_object_at(self.__ball.x, self.__ball.y + self.__ball_radius * 2) is None:
                if self.window.get_object_at(self.__ball.x + self.__ball_radius * 2,
                                             self.__ball.y + self.__ball_radius * 2) is not None:
                    if score >= 150:
                        self.paddle_or_godzilla()
                    else:
                        self.paddle_or_bricks()
            elif self.window.get_object_at(self.__ball.x + self.__ball_radius * 2,
                                           self.__ball.y + self.__ball_radius * 2) is None:
                if self.window.get_object_at(self.__ball.x, self.__ball.y + self.__ball_radius * 2) is not None:
                    if score >= 150:
                        self.paddle_or_godzilla()
                    else:
                        self.paddle_or_bricks()

    def set_ball(self):
        """
        Reset the ball
        """
        self.__dx = 0
        self.__dy = 0
        self.__ball.x = (self.__window_width - self.__ball_radius * 2) // 2
        self.__ball.y = (self.__window_height - self.__ball_radius * 2) // 2
        onmouseclicked(self.start)

    def ball_move(self):
        """
        Let the ball move among the walls
        """
        if not self.lose:
            self.__ball.move(self.__dx, self.__dy)
            if self.__ball.x <= 0 or self.__ball.x + self.__ball.width >= self.window.width:
                self.__dx = -self.__dx
            if self.__ball.y <= BRICK_OFFSET - 5:
                self.__dy = -self.__dy
            # The player missed the ball
            if self.__ball.y > self.__window_height - self.__paddle_offset:
                self.__times += 1
                self.set_ball()
                self.change_life()

    def change_life(self):
        """
        When the player misses the ball, one life will be eliminate
        Method 1: change the color to white, but remain the outline
        Method 2: remove the ball
        """
        for i in range(NUM_LIVES):
            self.__chance_x = self.__window_width - 230 + (NUM_LIVES - self.__times) * (self.chance.width + 15)
            self.chance = GOval(25, 25, x=self.__chance_x, y=self.__chance_y)
            self.chance.filled = True
            self.chance.color = 'tomato'
            self.chance.fill_color = 'white'
            self.window.add(self.chance)

    # 座標加上 self.chance.height//2
    # chance_x = self.window_width - 230 + (NUM_LIVES - self.times) * (self.chance.width + 15) + self.chance.height//2
    # chance_y = self.window_height - 38 + self.chance.height//2
    # self.window.remove(self.window.get_object_at(chance_x, chance_y))

    def end_game(self):
        """
        The break for the while loop
        :return: Boolean, True
        """
        if self.win or self.lose:
            return True

    def loading(self):
        """
        The animation of loading
        """
        background = GRect(self.window.width, self.window.height)
        self.window.add(background)
        loading = GLabel('LOADING FOR BREAKOUT')
        loading.font = 'Helvetica-40-bold'
        loading.color = 'indianred'
        self.window.add(loading, x=(self.__window_width - loading.width) // 2, y=self.__window_height // 2.2)
        space = self.__window_width // 8.4
        for i in range(7):
            dot_x = space
            dot_y = self.__window_height // 1.8
            dot = GOval(self.__ball_radius * 3.2, self.__ball_radius * 3.2, x=dot_x * (i + 1), y=dot_y)
            dot.filled = True
            dot.color = 'white'
            dot.fill_color = 'rosybrown'
            self.window.add(dot)
            pause(250)
        pause(500)
        self.window.clear()

    def level_2(self):
        """
        Level 2 is to make the paddle shorter, and change the label to Level 2
        """
        self.window.remove(self.__paddle)
        self.__paddle = GRect(self.__paddle_width * 2 // 3, self.__paddle_height,
                            x=(self.__window_width - self.__paddle_width) // 2,
                            y=self.__window_height - self.__paddle_offset - self.__paddle_height)
        self.__paddle.filled = True
        self.__paddle.color = 'cadetblue'
        self.__paddle.fill_color = 'cadetblue'
        self.window.add(self.__paddle)
        self.level_2_label.font = 'Helvetica-20-bold'
        self.level_2_label.color = 'cadetblue'
        self.window.add(self.level_2_label, x=(self.window.width - self.level_1.width) // 2, y=37)

    def bonus(self):
        """
        A bonus for player to attack Godzilla by the ball with extra score
        """
        self.window.remove(self.win_label)
        self.window.remove(self.level_2_label)
        self.attack.font = 'Helvetica-20-bold'
        self.attack.color = 'red'
        self.window.add(self.attack, x=(self.window.width - self.attack.width) // 2, y=37)
        warning_1 = GLabel('GODZILLA')
        warning_2 = GLabel('IS COMING')
        warning_1.font = 'Helvetica-60-bold'
        warning_1.color = 'red'
        warning_2.font = 'Helvetica-60-bold'
        warning_2.color = 'red'
        # Animation for warning the player
        for i in range(10):
            pause(100)
            self.window.add(warning_1, x=(self.__window_width - warning_1.width) // 2,
                            y=(self.__window_height - warning_1.height) // 2 - 50)
            self.window.add(warning_2, x=(self.__window_width - warning_2.width) // 2,
                            y=(self.__window_height - warning_2.height) // 2 + 50)
            pause(100)
            self.window.remove(warning_1)
            self.window.remove(warning_2)
        self.window.add(self.img, x=(self.__window_width - self.img.width) // 2, y=BRICK_OFFSET - 5)
        self.window.add(self.__ball, x=(self.__window_width - self.__ball.width) // 2, y=self.__paddle_offset - 50)

        self.set_ball()

    def paddle_or_godzilla(self):
        """
        Identify the ball hits the paddle or Godzilla or drop(***)
        if paddle, change the ball's dy to -dy
        if Godzilla, minus one attack, add on score, and change the ball's dy to -dy
        *** Not yet complete: if the drop hit the paddle, the player lose one life
        """
        if self.__ball.y > self.window.height // 2:  # If the ball is at the lower side
            self.__dy = -self.__dy
        if self.__ball.y < self.window.height // 2:  # If the ball is at the upper side
            if self.__count != 20:
                if self.img.x <= self.__ball.x <= self.img.x + self.img.width and self.img.y + self.img.height - 7 <= \
                        self.__ball.y <= self.img.y + self.img.height + 7 \
                        or self.img.y <= self.__ball.y <= self.img.y + self.img.height and \
                        self.img.x - 7 <= self.__ball.x <= self.img.x - 7 or \
                        self.img.y <= self.__ball.y <= self.img.y + self.img.height and \
                        self.img.x + self.img.width - 7 <= self.__ball.x <= self.img.x + self.img.width + 7:
                    self.__dy = -self.__dy
                    self.__dx = -self.__dx
                    global score
                    score += 10
                    self.random_drop()
                    self.__count += 1
                    self.score_label.text = 'SCORE: ' + str(score)  # Change score
                    self.attack.text = 'ATTACK' + str(20 - self.__count)

    def random_drop(self):
        """
        Godzilla will drop a rectangle to attack the user
        """
        self.drop = GRect(20, 50)
        self.drop.filled = True
        self.drop.fill_color = 'red'
        self.drop.color = 'white'
        drop_x = random.randint(0, self.__window_width)
        self.window.add(self.drop, x=drop_x, y=BRICK_OFFSET)
        self.attack_bricks.append(self.drop)

    def move_drop(self):
        """
        The method that can move the drop
        """
        for i in self.attack_bricks:
            i.move(self.__drop_vx, self.__drop_vy)
            if i.y >= self.window.height - PADDLE_OFFSET:
                self.window.remove(i)
                self.attack_bricks.pop(0)

    def bonus_end(self):
        """
        The break for the while loop
        :return: Boolean, True
        """
        if self.__count == 20 or NUM_LIVES == self.__times:
            return True
