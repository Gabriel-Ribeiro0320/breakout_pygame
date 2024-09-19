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

# Cores dos tijolos
brick_colors = [
    (255, 0, 0),   # Vermelho
    (255, 165, 0), # Laranja
    (0, 255, 0),   # Verde
    (255, 255, 0)  # Amarelo
]

# Função para determinar a cor da linha
def get_brick_color(row):
    if row < 2:
        return brick_colors[0]  # Vermelho
    elif row < 4:
        return brick_colors[1]  # Laranja
    elif row < 6:
        return brick_colors[2]  # Verde
    else:
        return brick_colors[3]  # Amarelo

# resolution

screen_width = 700
screen_height = 950
background_color = BLACK
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout - 1976")

# ball

ball_color = WHITE
ball_width = 9
ball_height = 7
ball_x = 350
ball_y = 475
ball_dx = 5
ball_dy = 5

# paddle

paddle_color = BLUE
paddle_width = 45
paddle_height = 15
paddle_pos = [screen_width // 2 - paddle_width // 2, screen_height - 50]
paddle_speed = 7

# bricks

brick_lines = 8
brick_columns = 14
brick_spaces = 8
brick_width = 41.5 # 130 pixel de espaço entre os blocos, e 570 de blocos, dando 41.71, mas achei esse a melhor possível
brick_height = 17
bricks = []
bricks_colors = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]

# score

max_attempts = 3
points = 0

# game loop

game_loop = True
game_clock = pygame.time.Clock()


pygame.quit()