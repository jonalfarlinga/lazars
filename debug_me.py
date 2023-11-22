import pygame


def debug(mouse_pos, screen, sc_width, sprites):
    font = pygame.font.SysFont("Arial", 20)
    track = font.render(str(mouse_pos), True, (0, 0, 0))
    screen.blit(track, (sc_width-100, 10))
    """ for rect in borders:
        if rect.collidepoint(mouse_pos):
            print("COLLISION" + str(rect)) """
    for sprite in sprites:
        if hasattr(sprite, "blit_sprite"):
            sprite.blit_sprite(screen)
            if sprite.rect.collidepoint(mouse_pos):
                print("COLLISION" + str(sprite))
        elif sprite.collidepoint(mouse_pos):
            print("COLLISION" + str(sprite))
