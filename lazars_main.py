# import the pygame module, so you can use it
import pygame
import sys
import os
from debug_me import debug
import maps


'''
set up constants
'''
# initialize the pygame module
pygame.init()

# set max FPS
FPS = 60
FramesPerSecond = pygame.time.Clock()

# load and set the logo
logo = pygame.image.load(os.path.join("assets", "laser.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Lazars")
font = pygame.font.SysFont("Arial", 20)

# set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# initialize assets
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BORDER_WIDTH = 12


'''
create classes
'''


class Wall(pygame.sprite.Sprite):
    def __init__(self, center=None):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "wall.png"))
        self.rect = self.image.get_rect()
        if center:
            self.rect.centerx = center[0]
            self.rect.centery = center[1]

    def blit_sprite(self, surface):
        surface.blit(
            source=self.image,
            dest=(self.rect.centerx-self.image.get_size()[0]//2,
                  self.rect.centery-self.image.get_size()[1]//2)
        )


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.direction = 180  # facing in degrees

    def blit_sprite(self, surface):
        surface.blit(
            source=self.image,
            dest=(self.rect.centerx-self.image.get_size()[0]//2,
                  self.rect.centery-self.image.get_size()[1]//2)
        )

    def laser(self):
        pass


def print_background(screen):
    screen.fill(BLACK)
    pygame.draw.lines(
        screen,
        WHITE,
        True,
        [
            (0, 0),
            (0, SCREEN_HEIGHT),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (SCREEN_WIDTH, 0)
        ],
        48
    )


'''
initialize game environment
'''
# create a surface on screen and initialize entities
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
borders = [
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH-1, 0), (0, 0)),
    pygame.draw.line(screen, WHITE, (0, 0), (0, SCREEN_HEIGHT-1)),
    pygame.draw.line(
        screen,
        WHITE,
        (0, SCREEN_HEIGHT-1),
        (SCREEN_WIDTH-1, SCREEN_HEIGHT-1)
    ),
    pygame.draw.line(
        screen,
        WHITE,
        (SCREEN_WIDTH-1, SCREEN_HEIGHT-1),
        (SCREEN_WIDTH-1, 0)
    ),
]
walls = pygame.sprite.Group()
for place in maps.testmap():
    wall = Wall(place)
    walls.add(wall)

player = Player()
player.rect.center = (50, 50)


# define a main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        print_background(screen)
        debug(pygame.mouse.get_pos(), screen,
              SCREEN_WIDTH, borders + walls.sprites())
        player.blit_sprite(screen)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
        FramesPerSecond.tick(FPS)
        pygame.display.update()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
