# import the pygame module, so you can use it
import pygame
import sys

from pygame.sprite import _Group

# initialize the pygame module
pygame.init()

# load and set the logo
# logo = pygame.image.load("logo32x32.png")
# pygame.display.set_icon(logo)
pygame.display.set_caption("minimal program")

# set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# initialize assets
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
borders = pygame.draw.lines(
        screen,
        WHITE,
        closed=True,
        points=[
            (0, 0),
            (0, SCREEN_HEIGHT),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (SCREEN_WIDTH, 0)
        ]
    )
walls = [
    pygame.draw.rect(screen, WHITE, (100, 100, 50, 75))
]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


# define a main function
def main():
    pygame.display.flip()
    # main loop
    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
