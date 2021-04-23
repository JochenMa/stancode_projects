"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This is a breakout game with loading animation, two levels of games, and a score board
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120  # 120 frames per second


def main():
    graphics = BreakoutGraphics()
    # Add animation loop here!
    while True:
        graphics.collision()        # detect collision
        graphics.ball_move()        # move the ball
        pause(FRAME_RATE)
        graphics.win_or_lose()      # detect win or lose
        if graphics.end_game():     # when the game is ended, break the loop
            break
    if graphics.win:
        # For bonus game
        graphics.bonus()
        while True:
            graphics.collision()
            graphics.ball_move()
            graphics.move_drop()
            pause(FRAME_RATE)
            if graphics.bonus_end():
                break
    pause(FRAME_RATE*200)           # animation for showing final score board
    graphics.final_score_board()    # final score board


if __name__ == '__main__':
    main()
