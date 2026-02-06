import pygame
import random
import math
import os

pygame.init()

# ================== CONFIG ==================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake NSI")

clock = pygame.time.Clock()
FPS = 60

GRID_SIZE = 40

# Couleurs (style Google Snake)
BG_COLOR = (170, 215, 81)
GRID_COLOR = (162, 209, 73)
WHITE = (245, 245, 245)
GREEN = (78, 124, 246)
DARK_GREEN = (60, 100, 220)

# Tailles
SNAKE_RADIUS_HEAD = 18
SNAKE_RADIUS_TAIL = 8
FOOD_RADIUS = 16
SNAKE_SPEED = 4

# Score
SCORE_FILE = "highscore.txt"

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 56)

# ================== OUTILS ==================

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def charger_highscore():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def sauvegarder_highscore(score):
    with open(SCORE_FILE, "w") as f:
        f.write(str(score))

def afficher_texte(texte, font, couleur, x, y):
    img = font.render(texte, True, couleur)
    screen.blit(img, (x, y))

def dessiner_grille():
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            color = BG_COLOR if (x // GRID_SIZE + y // GRID_SIZE) % 2 == 0 else GRID_COLOR
            pygame.draw.rect(screen, color, rect)

# ================== GRAPHISMES ==================

def dessiner_pomme_degrade(x, y):
    for r in range(FOOD_RADIUS, 0, -1):
        couleur = (
            220 + r,
            60 + r,
            60
        )
        pygame.draw.circle(screen, couleur, (x, y), r)

def dessiner_serpent(snake):
    total = len(snake)
    for i, (x, y) in enumerate(snake):
        t = i / total
        radius = int(SNAKE_RADIUS_HEAD * (1 - t) + SNAKE_RADIUS_TAIL * t)
        color = (
            int(GREEN[0] * (1 - t) + DARK_GREEN[0] * t),
            int(GREEN[1] * (1 - t) + DARK_GREEN[1] * t),
            int(GREEN[2] * (1 - t) + DARK_GREEN[2] * t)
        )
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)

# ================== MENU ==================

def menu():
    highscore = charger_highscore()

    while True:
        dessiner_grille()
        afficher_texte("SNAKE - PROJET NSI", big_font, WHITE, 200, 160)
        afficher_texte("ESPACE : Jouer", font, WHITE, 320, 260)
        afficher_texte("P : Pause", font, WHITE, 350, 300)
        afficher_texte(f"High Score : {highscore}", font, WHITE, 320, 360)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_loop()

        pygame.display.update()
        clock.tick(30)

# ================== JEU ==================

def game_loop():
    x, y = WIDTH // 2, HEIGHT // 2
    dir_x, dir_y = 1, 0

    snake = []
    snake_length = 14
    score = 0
    paused = False
    game_over = False

    food_x = random.randint(80, WIDTH - 80)
    food_y = random.randint(80, HEIGHT - 80)

    while True:
        clock.tick(FPS)
        dessiner_grille()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dir_x, dir_y = 0, -1
                elif event.key == pygame.K_DOWN:
                    dir_x, dir_y = 0, 1
                elif event.key == pygame.K_LEFT:
                    dir_x, dir_y = -1, 0
                elif event.key == pygame.K_RIGHT:
                    dir_x, dir_y = 1, 0
                elif event.key == pygame.K_p:
                    paused = not paused

        if not paused and not game_over:
            x += dir_x * SNAKE_SPEED
            y += dir_y * SNAKE_SPEED

            snake.insert(0, (x, y))
            if len(snake) > snake_length:
                snake.pop()

            # Murs
            if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
                game_over = True

            # Soi-même
            for seg in snake[10:]:
                if distance(x, y, seg[0], seg[1]) < 10:
                    game_over = True

            # Pomme
            if distance(x, y, food_x, food_y) < FOOD_RADIUS + 10:
                food_x = random.randint(80, WIDTH - 80)
                food_y = random.randint(80, HEIGHT - 80)
                snake_length += 6
                score += 10

        # Pomme dégradée
        dessiner_pomme_degrade(food_x, food_y)

        # Serpent arrondi progressif
        dessiner_serpent(snake)

        # Yeux
        eye_dx = dir_x * 8
        eye_dy = dir_y * 8
        pygame.draw.circle(screen, WHITE, (int(x + eye_dx - 5), int(y + eye_dy - 5)), 4)
        pygame.draw.circle(screen, WHITE, (int(x + eye_dx + 5), int(y + eye_dy + 5)), 4)

        afficher_texte(f"Score : {score}", font, WHITE, 10, 10)

        if paused:
            afficher_texte("PAUSE", big_font, WHITE, 340, 280)

        if game_over:
            highscore = charger_highscore()
            if score > highscore:
                sauvegarder_highscore(score)

            afficher_texte("PERDU", big_font, (220, 60, 60), 340, 250)
            afficher_texte("R : Rejouer | M : Menu", font, WHITE, 270, 320)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_loop()
            if keys[pygame.K_m]:
                menu()

        pygame.display.update()

# ================== LANCEMENT ==================
menu()
