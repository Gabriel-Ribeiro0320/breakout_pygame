import pygame

pygame.init()

# colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)

background_color = BLACK

# resolution

screen_width = 700
screen_height = 950
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.quit()