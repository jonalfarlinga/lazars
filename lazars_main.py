import pygame
import sys
import os
# import debug_me
import maps
from constants import *  # noqa:F403 flake8 ignore
from entities import Player


'''
set up constants
'''
# initialize the pygame module
pygame.init()

# initialize the game Clock
FramesPerSecond = pygame.time.Clock()

# load and set the logo
logo = pygame.image.load(os.path.join("assets", "laser.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Lazars")
font = pygame.font.SysFont("Arial", 20)


# run each loop to fill the background and blit walls.
def print_background(screen, walls):
    # black BG
    screen.fill(BLACK)

    # builds a list of walls and borders
    rects = []
    for block in borders + walls.sprites():
        # if the block is a wall, blit it to the screen.
        if hasattr(block, "blit_sprite"):
            rects.append(block.rect)
            block.blit_sprite(screen)
        else:
            rects.append(block)

    # draw the screen borders
    pygame.draw.lines(
        screen,
        RED,
        True,
        [
            (0, TOP_PAD),
            (0, SCREEN_HEIGHT),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (SCREEN_WIDTH, TOP_PAD)
        ],
        BORDER_WIDTH * 2
    )

    return rects


'''
initialize game environment
'''
# create a surface on screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# build walls and borders
borders = maps.build_borders(screen)
walls = maps.build_walls(maps.testmap2())

# build the player
player = Player()
player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# define the main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        # print the level and generate rectangles
        rects = print_background(screen, walls)

        # manage player

        player.move(rects)
        player.laser(screen, rects)
        player.blit_sprite(screen)

        # event handling, gets all events from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
        # wait to limit processor focus
        pygame.time.wait(30)

        # tick game clock
        FramesPerSecond.tick(FPS)

        # debuggers
        #       debug_me.debug(pygame.mouse.get_pos(), screen, rects)
        #       debug_me.fps_counter(FramesPerSecond, screen, font)
        #       debug_me.fps_counter(FramesPerSecond, screen, font)

        # update display
        pygame.display.update()


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    main()
