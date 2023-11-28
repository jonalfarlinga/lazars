import pygame
import sys
import os
import debug_me
import maps
from constants import *  # noqa:F403 flake8 ignore
from entities import Player


'''
set up constants
'''
# initialize the pygame module
pygame.init()

# load and set the logo
logo = pygame.image.load(os.path.join("assets", "laser.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Lazars")
font = pygame.font.SysFont("Arial", 20)


def print_background(screen):
    screen.fill(BLACK)
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


'''
initialize game environment
'''
# create a surface on screen and initialize entities
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
borders = maps.build_borders(screen)
walls = maps.build_walls(maps.testmap())

player = Player()
player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

FramesPerSecond = pygame.time.Clock()


# define a main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        print_background(screen)
        # blit the walls and make a list of all rects
        rects = []
        for block in borders + walls.sprites():
            if hasattr(block, "blit_sprite"):
                block.blit_sprite(screen)
            if hasattr(block, "rect"):
                rects.append(block.rect)
            else:
                rects.append(block)

        # debug_me.debug(pygame.mouse.get_pos(), screen, rects)
        player.move(rects)
        player.laser(screen, rects)
        player.blit_sprite(screen)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
        pygame.time.delay(0)
        FramesPerSecond.tick(FPS)
        debug_me.fps_counter(FramesPerSecond, screen, font)
        pygame.display.update()


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    main()
