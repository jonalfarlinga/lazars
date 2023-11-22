# import the pygame module, so you can use it
import pygame
import sys
import os
from debug_me import debug
import maps
from constants import *
from vector_math import calculate_line


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



'''
create classes
'''


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.direction = 45  # facing in degrees

    def blit_sprite(self, surface):
        surface.blit(
            source=self.image,
            dest=(self.rect.centerx-self.image.get_size()[0]//2,
                  self.rect.centery-self.image.get_size()[1]//2)
        )

    def laser(self, screen, blocks):
        rects = []
        for block in blocks:
            if hasattr(block, "rect"):
                rects.append(block.rect)
            else:
                rects.append(block)
        line_segments = calculate_line(self.rect.center, self.direction, rects)
        for segment in line_segments:
            pygame.draw.line(
                screen,
                RED,
                segment,
            )


def print_background(screen):
    screen.fill(WHITE)
    pygame.draw.lines(
        screen,
        BLACK,
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
borders = [
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH-13, 12), (12, 12)),
    pygame.draw.line(screen, WHITE, (0, TOP_PAD), (0, SCREEN_HEIGHT+TOP_PAD-1)),
    pygame.draw.line(
        screen,
        WHITE,
        (12, SCREEN_HEIGHT+TOP_PAD-13),
        (SCREEN_WIDTH-13, SCREEN_HEIGHT+TOP_PAD-13)
    ),
    pygame.draw.line(
        screen,
        WHITE,
        (SCREEN_WIDTH-13, SCREEN_HEIGHT+TOP_PAD-13),
        (SCREEN_WIDTH-13, TOP_PAD+12)
    ),
]
walls = pygame.sprite.Group()
for wall in maps.testmap():
    walls.add(wall)

player = Player()
player.rect.center = (50, 100)

FramesPerSecond = pygame.time.Clock()

# define a main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        print_background(screen)
        debug(pygame.mouse.get_pos(), screen, borders + walls.sprites())
        player.blit_sprite(screen)
        player.laser(screen, borders + walls.sprites())
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
        pygame.time.delay(10)
        FramesPerSecond.tick(FPS)
        pygame.display.update()


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    main()
