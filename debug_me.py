import pygame
from constants import *


def debug(mouse_pos, screen, blocks):
    font = pygame.font.SysFont("Arial", 20)
    track = font.render(str(mouse_pos), True, (255, 255, 255))
    pygame.draw.line(screen, RED, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2,), mouse_pos)
    screen.blit(track, (SCREEN_WIDTH-100, 10))
    for block in blocks:
        if hasattr(block, "blit_sprite"):
            block.blit_sprite(screen)
            if block.rect.collidepoint(mouse_pos):
                print("COLLISION" + str(block))
        elif block.collidepoint(mouse_pos):
            print("COLLISION" + str(block))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())
