import math
import random

# Verifica se o pygame está instalado
try:
    import pygame
except ImportError:
    print("O módulo pygame não está instalado. Instale-o com 'pip install pygame'.")
    exit()

# Inicializa o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Basquete")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Configurações do jogo
ball_radius = 15
basket_x = WIDTH - 100
basket_y = HEIGHT - 200
basket_width = 50
basket_height = 10

def draw_basket(x, y):
    pygame.draw.rect(screen, RED, (x, y, basket_width, basket_height))

def is_collision(ball_x, ball_y, basket_x, basket_y, basket_width, basket_height):
    return (
        basket_x <= ball_x <= basket_x + basket_width and
        basket_y <= ball_y <= basket_y + basket_height
    )

def main():
    running = True

    ball_x = 100
    ball_y = HEIGHT - 50
    velocity_x = 0
    velocity_y = 0
    is_thrown = False

    angle = 45  # Ângulo inicial
    power = 50  # Potência inicial

    font = pygame.font.SysFont(None, 36)

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if not is_thrown:
            if keys[pygame.K_UP]:
                angle = min(angle + 1, 90)  # Limita o ângulo máximo a 90 graus
            if keys[pygame.K_DOWN]:
                angle = max(angle - 1, 0)  # Limita o ângulo mínimo a 0 graus
            if keys[pygame.K_RIGHT]:
                power = min(power + 1, 100)  # Limita a potência máxima a 100
            if keys[pygame.K_LEFT]:
                power = max(power - 1, 10)  # Limita a potência mínima a 10
            if keys[pygame.K_SPACE]:
                # Calcula as velocidades com base no ângulo e na potência
                velocity_x = math.cos(math.radians(angle)) * power / 2
                velocity_y = -math.sin(math.radians(angle)) * power / 2
                is_thrown = True

        if is_thrown:
            ball_x += velocity_x
            ball_y += velocity_y
            velocity_y += 0.5  # Gravidade

            # Verifica se a bola saiu da tela
            if ball_y > HEIGHT - ball_radius or ball_x > WIDTH or ball_x < 0:
                ball_x = 100
                ball_y = HEIGHT - 50
                velocity_x = 0
                velocity_y = 0
                is_thrown = False

        # Verifica se a bola acertou a cesta
        if is_collision(ball_x, ball_y, basket_x, basket_y, basket_width, basket_height):
            message = font.render("Acertou!", True, BLACK)
            screen.blit(message, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
            pygame.display.update()
            pygame.time.wait(2000)

            # Reinicia o jogo
            ball_x = 100
            ball_y = HEIGHT - 50
            velocity_x = 0
            velocity_y = 0
            is_thrown = False

        # Desenha a bola e a cesta
        pygame.draw.circle(screen, ORANGE, (int(ball_x), int(ball_y)), ball_radius)
        draw_basket(basket_x, basket_y)

        # Exibe o ângulo e a potência
        angle_text = font.render(f"Ângulo: {angle}°", True, BLACK)
        power_text = font.render(f"Potência: {power}", True, BLACK)
        screen.blit(angle_text, (10, 10))
        screen.blit(power_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
