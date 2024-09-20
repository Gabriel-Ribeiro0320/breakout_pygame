import pygame
import random

# Inicializar o Pygame
pygame.init()

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)

# Definir a cor dos tijolos por linha
def get_brick_color(row):
    if row < 2:
        return brick_colors[0]  # Red
    elif row < 4:
        return brick_colors[1]  # Orange
    elif row < 6:
        return brick_colors[2]  # Green
    else:
        return brick_colors[3]  # Yellow


# Resolução da tela

screen_width = 700
screen_height = 950
background_color = BLACK
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout - 1976")

# Sons
brick_sound = pygame.mixer.Sound('sounds/brick.wav')
paddle_sound = pygame.mixer.Sound('sounds/paddle.wav')
wall_sound = pygame.mixer.Sound('sounds/wall.wav')

# Bola
ball_color = WHITE
ball_width = 10
ball_height = 5
ball_x = random.randint(11, 689)
ball_y = 500
ball_dx = 5
ball_dy = 5

# Raquete

paddle_color = BLUE
paddle_width = 45
paddle_height = 15
paddle_pos = [screen_width // 2 - paddle_width // 2, screen_height - 50]
paddle_speed = 8

# Tijolos

brick_lines = 8
brick_columns = 14
brick_spaces = 8
brick_width = 41.5  # 130 pixels de espaço entre os blocos, e 570 de blocos
brick_height = 17
bricks = []
brick_colors = [RED, ORANGE, GREEN, YELLOW]

# Pontuação e tentativas

max_attempts = 1
score = 0

# Bordas

border_width = 10
top_width = 20
border_color = WHITE
border_yellow = YELLOW
border_green = GREEN
border_orange = ORANGE
border_red = RED

# Construir os tijolos

for row in range(brick_lines):
    for col in range(brick_columns):
        brick_y = row * (brick_height + brick_spaces) + 100
        brick_x = col * (brick_width + brick_spaces) + brick_spaces
        brick_color = get_brick_color(row)
        brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append((brick_rect, brick_color))

# Loop principal do jogo
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:
    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    # Movimento da raquete
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
        paddle_pos[0] -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_pos[0] < screen_width - paddle_width:
        paddle_pos[0] += paddle_speed

    # Movimento da bola
    ball_x += ball_dx
    ball_y += ball_dy

    # Colisões da bola com as bordas da tela

    if ball_x <= 0 or ball_x + ball_width >= screen_width:
        ball_dx = -ball_dx
        wall_sound.play()
    if ball_y <= 0:
        ball_dy = -ball_dy
        wall_sound.play()
    if ball_y + ball_height >= screen_height:
        wall_sound.play()
        ball_x = random.randint(1, 700)
        ball_y = 500
        max_attempts += 1
        if max_attempts == 4:
            text = font.render("GAME OVER", 1, WHITE)
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(2000)
            game_loop = False

    # Colisão da bola com a raquete

    paddle_rect = pygame.Rect(paddle_pos[0], paddle_pos[1], paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)

    if ball_rect.colliderect(paddle_rect):
        if ball_y + ball_height - ball_dy <= paddle_pos[1]:
            ball_dy = -ball_dy
            paddle_sound.play()
        else:
            ball_dx = -ball_dx
        paddle_sound.play()

    # Colisão da bola com os tijolos
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

    # Desenhar tudo na tela

    screen.fill(background_color)

    # Desenhar bordas

    pygame.draw.rect(screen, border_color, pygame.Rect(0, 0, screen_width, top_width))  # Borda superior
    pygame.draw.rect(screen, border_color, pygame.Rect(0, 0, border_width, screen_height))  # Borda esquerda
    pygame.draw.rect(screen, border_color, pygame.Rect(screen_width - border_width, 0, border_width, screen_height))  # Borda direita

    # Desenhar a pontuação no topo da tela

    font = pygame.font.Font('text_style/DSEG14Classic-Bold.ttf', 40)
    text = font.render(str(f"{score:03}"), 1, WHITE)  # score left
    screen.blit(text, (70, 50))
    text = font.render(str(max_attempts), 1, WHITE)  # 1 number left
    screen.blit(text, (430, 22))
    text = font.render('000', 1, WHITE)  # score right
    screen.blit(text, (500, 50))
    text = font.render("1", 1, WHITE)  # number right
    screen.blit(text, (1, 22))

    # Desenhar os tijolos

    for brick_rect, brick_color in bricks:
        pygame.draw.rect(screen, brick_color, brick_rect)

    # Desenhar a raquete

    pygame.draw.rect(screen, paddle_color, paddle_rect)

    # Desenhar a bola

    pygame.draw.ellipse(screen, ball_color, ball_rect)

    # Atualizar a tela

    pygame.display.flip()

    # Controlar a taxa de quadros por segundo

    game_clock.tick(60)

pygame.quit()

