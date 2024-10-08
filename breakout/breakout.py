import pygame
import random

pygame.init()

# colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 127, 230)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)

# resolution

screen_width = 700
screen_height = 950
background_color = BLACK
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout - 1976")

# interface

max_attempts = 1
score = 0

# some functions

can_break_brick = True
game_started = False
sound_enabled = False

# sounds

brick_sound = pygame.mixer.Sound('sounds/brick.wav')
paddle_sound = pygame.mixer.Sound('sounds/paddle.wav')
wall_sound = pygame.mixer.Sound('sounds/wall.wav')

# ball

ball_color = WHITE
ball_width = 10
ball_height = 5
ball_x = random.randint(100, 600)
ball_y = 350
ball_dx = 5
ball_dy = 5
ball_speed = 5

# paddle

paddle_color = BLUE
paddle_width = screen_width
paddle_height = 15
paddle_pos = [screen_width // 2 - paddle_width // 2, screen_height - 50]
paddle_speed = 5

# bricks

brick_lines = 8
brick_columns = 14
brick_spaces = 8
brick_width = 41.5
brick_height = 17
bricks = []
brick_colors = [RED, ORANGE, GREEN, YELLOW]

# border

border_width = 10
top_width = 20
border_color = WHITE
border_yellow = YELLOW
border_green = GREEN
border_orange = ORANGE
border_red = RED

# line colors

def get_brick_color(lines):
    if lines < 2:
        return brick_colors[0]  # red
    elif lines < 4:
        return brick_colors[1]  # orange
    elif lines < 6:
        return brick_colors[2]  # green
    else:
        return brick_colors[3]  # yellow


# draw initial phrase

def draw_start_text():
    font = pygame.font.Font('text_style/breakout.ttf', 20)
    text = font.render("PRESS  SPACE  BAR  TO  START", True, WHITE)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)


# build bricks

for row in range(brick_lines):
    for col in range(brick_columns):
        brick_y = row * (brick_height + brick_spaces) + 100
        brick_x = col * (brick_width + brick_spaces) + brick_spaces
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

    # if game starts

    keys = pygame.key.get_pressed()
    if not game_started:
        sound_enabled = False
        if keys[pygame.K_SPACE]:
            score = 0
            max_attempts = 1
            ball_x = random.randint(100, 600)
            ball_y = 300
            ball_dy = 5
            ball_dx = 5
            paddle_width = 45
            game_started = True
            paddle_pos = [screen_width // 2 - paddle_width // 2, screen_height - 50]
            bricks = []

            # rebuild the bricks

            for row in range(brick_lines):
                for col in range(brick_columns):
                    brick_y = row * (brick_height + brick_spaces) + 100
                    brick_x = col * (brick_width + brick_spaces) + brick_spaces
                    brick_color = get_brick_color(row)
                    brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                    bricks.append((brick_rect, brick_color))

    # paddle movement

    if game_started:
        sound_enabled = True
        pygame.draw.ellipse(screen, ball_color, ball_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
            paddle_pos[0] -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_pos[0] < screen_width - paddle_width:
            paddle_pos[0] += paddle_speed
    else:
        paddle_pos = [0, screen_height - 50]

    # paddle movement

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
        paddle_pos[0] -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_pos[0] < (screen_width - border_width) - paddle_width:
        paddle_pos[0] += paddle_speed

    # ball movement

    if game_started:
        ball_x += ball_dx / abs(ball_dx) * ball_speed
        ball_y += ball_dy / abs(ball_dy) * ball_speed

    # ball collisions with wall

    if ball_x <= border_width or ball_x + ball_width >= screen_width - border_width:
        ball_dx = -ball_dx
        if sound_enabled:
            wall_sound.play()

    if ball_y <= 0 + top_width:
        can_break_brick = True
        ball_dy = -ball_dy
        if sound_enabled:
            wall_sound.play()
            
    if ball_y + ball_height >= screen_height:
        max_attempts += 1
        ball_x = random.randint(100, 600)
        ball_y = 300
        ball_dx = 5
        ball_dy = 5

        if sound_enabled:
            wall_sound.play()

        if max_attempts == 4:
            paddle_width = screen_width
            can_break_brick = False
            game_started = False
            sound_enabled = False

    # ball collision with paddle

    paddle_rect = pygame.Rect(paddle_pos[0], paddle_pos[1], paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)

    if ball_rect.colliderect(paddle_rect):
        ball_dx = -ball_dx
        if sound_enabled:
            paddle_sound.play()
        if ball_y + ball_height - ball_dy <= paddle_pos[1]:
            ball_dy = -ball_dy
            if sound_enabled:
                paddle_sound.play()

    # ball collision angle

    if ball_rect.colliderect(paddle_rect):
        paddle_middle = paddle_pos[0] + paddle_width // 2
        ball_impact_pos = ball_x + ball_width // 2

        if ball_impact_pos < paddle_pos[0] + paddle_width // 4:
            ball_dx = -abs(ball_dx) + 4
        elif ball_impact_pos >= paddle_middle + paddle_width // 4:
            ball_dx = abs(ball_dx) - 4

        paddle_sound.play()
        can_break_brick = True

    # ball collision with bricks

    if game_started:
        for brick in bricks[:]:
            brick_rect, brick_color = brick
            if ball_rect.colliderect(brick_rect) and can_break_brick:
                bricks.remove(brick)
                ball_dy *= -1
                can_break_brick = False

                if sound_enabled:
                    brick_sound.play()

                # colors points

                if brick_color == YELLOW:
                    score += 1
                    ball_dx = 5
                    ball_dy = 5
                elif brick_color == GREEN:
                    score += 3
                    ball_speed = 5.5
                elif brick_color == ORANGE:
                    score += 5
                    ball_speed = 5
                elif brick_color == RED:
                    score += 7
                    ball_speed = 6.5
                break

    # ball collision with top

    if ball_y < 100 and paddle_width == 45:
        paddle_width = paddle_width // 2

    # draw bricks

    for brick_rect, brick_color in bricks:
        pygame.draw.rect(screen, brick_color, brick_rect)

    # scores and texts

    font = pygame.font.Font('text_style/breakout.ttf', 50)
    text = font.render(str(f"{score:03}"), 1, WHITE)  # score left
    screen.blit(text, (105, 50))
    text = font.render(str(max_attempts), 1, WHITE)  # 1 number left 360
    screen.blit(text, (430, 15))
    text = font.render('000', 1, WHITE)  # score right
    screen.blit(text, (500, 50))
    text = font.render("1", 1, WHITE)  # 1 number right 465
    screen.blit(text, (35, 15))

    # draw borders top - left - right

    pygame.draw.rect(screen, border_color, pygame.Rect(0, 0, screen_width, top_width))
    pygame.draw.rect(screen, border_color, pygame.Rect(0, 0, border_width, screen_height))
    pygame.draw.rect(screen, border_color, pygame.Rect(screen_width - border_width, 0, border_width, screen_height))

    # draw border (red, orange, green, yellow)

    pygame.draw.rect(screen, RED, pygame.Rect(0, 96, border_width, 54))
    pygame.draw.rect(screen, ORANGE, pygame.Rect(0, 150, border_width, 50))
    pygame.draw.rect(screen, GREEN, pygame.Rect(0, 200, border_width, 50))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(0, 245, border_width, 50))
    pygame.draw.rect(screen, RED, pygame.Rect(690, 96, border_width, 54))
    pygame.draw.rect(screen, ORANGE, pygame.Rect(690, 150, border_width, 50))
    pygame.draw.rect(screen, GREEN, pygame.Rect(690, 200, border_width, 50))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(690, 245, border_width, 50))

    # draw paddle border

    pygame.draw.rect(screen, BLUE, pygame.Rect(0, 893, border_width, 30))
    pygame.draw.rect(screen, BLUE, pygame.Rect(690, 893, border_width, 30))

    # draw paddle

    pygame.draw.rect(screen, paddle_color, paddle_rect)

    # refresh screen

    pygame.display.flip()

    # game tick

    game_clock.tick(60)

    # draw background

    screen.fill(background_color)

    # show the initial text

    if not game_started:
        draw_start_text()

pygame.quit()
