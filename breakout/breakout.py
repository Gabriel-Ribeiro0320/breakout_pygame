import pygame
import random

pygame.init()

# colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)

# resolution

screen_width = 700
screen_height = 950
background_color = BLACK
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout - 1976")

# score

max_attempts = 3
score = 0

# scores and texts

font = pygame.font.Font('text_style/DSEG14Classic-Bold.ttf', 40)
text = font.render(str(f"{score:03}"), 1, WHITE)
screen.blit(text, (70, 50))
text = font.render(str(max_attempts), 1, WHITE)
screen.blit(text, (430, 1))
text = font.render('000', 1, WHITE)
screen.blit(text, (500, 50))
text = font.render("1", 1, WHITE)
screen.blit(text, (1, 1))

# sounds
brick_sound = pygame.mixer.Sound('sounds/brick.wav')
paddle_sound = pygame.mixer.Sound('sounds/paddle.wav')
wall_sound = pygame.mixer.Sound('sounds/wall.wav')

# ball

ball_color = WHITE
ball_width = 9
ball_height = 7
ball_x = random.randint(0, 700)
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
brick_width = 41.5
brick_height = 17
bricks = []
brick_colors = [RED, ORANGE, GREEN, YELLOW]

# line colors

def get_brick_color(row):
    if row < 2:
        return brick_colors[0]  # red
    elif row < 4:
        return brick_colors[1]  # orange
    elif row < 6:
        return brick_colors[2]  # green
    else:
        return brick_colors[3]  # yellow


# build bricks

for row in range(brick_lines):
    for col in range(brick_columns):
        brick_x = col * (brick_width + brick_spaces) + brick_spaces
        brick_y = row * (brick_height + brick_spaces) + 50
        brick_color = get_brick_color(row)
        brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append((brick_rect, brick_color))

# game loop

game_loop = True
game_clock = pygame.time.Clock()

# check events

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    # paddle movement

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
        paddle_pos[0] -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_pos[0] < screen_width - paddle_width:
        paddle_pos[0] += paddle_speed

    # ball movement

    ball_x += ball_dx
    ball_y += ball_dy

    # ball collisions with bricks

    for brick in bricks[:]:
        brick_rect, brick_color = brick
        if ball_rect.colliderect(brick_rect):
            brick_sound.play()
            bricks.remove(brick)
            ball_dy = -ball_dy

            # Colors points
            if brick_color == YELLOW:
                score += 1
            elif brick_color == GREEN:
                score += 3
            elif brick_color == ORANGE:
                score += 5
            elif brick_color == RED:
                score += 7
            break

pygame.quit()