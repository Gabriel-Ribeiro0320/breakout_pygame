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
screen_width = 500
screen_height = 750
background_color = BLACK
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout - 1976")

# Sons
brick_sound = pygame.mixer.Sound('sounds/brick.wav')
paddle_sound = pygame.mixer.Sound('sounds/paddle.wav')
wall_sound = pygame.mixer.Sound('sounds/wall.wav')

# Texto de Pontuação
font = pygame.font.Font('text_style/DSEG14Classic-Bold.ttf', 44)

# Variáveis globais
balls = 1

# Bola
ball_color = WHITE
ball_width = 7
ball_height = 7
ball_x = random.randint(0, 950)
ball_y = 475
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

# Construir os tijolos
for row in range(brick_lines):
    for col in range(brick_columns):
        brick_x = col * (brick_width + brick_spaces) + brick_spaces
        brick_y = row * (brick_height + brick_spaces) + 100  # Aumentei a posição dos tijolos para 100
        brick_color = get_brick_color(row)
        brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append((brick_rect, brick_color))

# Pontuação e tentativas
max_attempts = 3
score = 0

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
        ball_x, ball_y = screen_width // 2, screen_height // 2  # Reseta a bola
        max_attempts -= 1
        if max_attempts == 0:
            print("Game Over")
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
        ball_dy = -ball_dy
        paddle_sound.play()

    # Colisão da bola com os tijolos
    for brick in bricks[:]:
        brick_rect, brick_color = brick
        if ball_rect.colliderect(brick_rect):
            brick_sound.play()
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 1
            break

    # Desenhar tudo na tela
    screen.fill(background_color)

    # Desenhar a pontuação no topo da tela
    font = pygame.font.Font('text_style/DSEG14Classic-Bold.ttf', 40)
    text = font.render(str(f"{score:03}"), 1, WHITE)
    screen.blit(text, (80, 120))
    text = font.render(str(balls), 1, WHITE)
    screen.blit(text, (540, 40))
    text = font.render('000', 1, WHITE)
    screen.blit(text, (580, 120))
    text = font.render('1', 1, WHITE)
    screen.blit(text, (20, 40))

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

