# import the pygame module, so you can use it
import pygame
import sys


# initialize the pygame module
pygame.init()

FPS = 60
FramesPerSecond = pygame.time.Clock()

# load and set the logo
# logo = pygame.image.load("logo32x32.png")
# pygame.display.set_icon(logo)
pygame.display.set_caption("Lazars")
font = pygame.font.SysFont("Arial", 20)

# set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# initialize assets
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
walls = [
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
    pygame.draw.rect(screen, WHITE, (100, 100, 50, 75)),
]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


# define a main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        screen.fill(BLACK)
        point = pygame.mouse.get_pos()
        track = font.render(str(point), True, WHITE)
        screen.blit(track, (SCREEN_WIDTH-100, 10))
        for rect in walls:
            if rect.collidepoint(point):
                print("COLLISION" + str(rect))
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
