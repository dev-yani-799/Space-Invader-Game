import pygame
import random
import math
from pygame import mixer

pygame.init()


# Seting the screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('s.jpg')

pygame.display.set_caption("Space Loader")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Load player image
player_image = pygame.image.load('space-invaders.png')
player_rect = player_image.get_rect()
player_rect.x = 370
player_rect.y = 480
playerx_change = 0

# Adding multiple enemies on the screen
enemy_image = []
enemy_rect = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    # Load enemy image and create a Rect object based on its dimensions
    enemy_image.append(pygame.image.load('game.png'))
    rect = enemy_image[i].get_rect()
    # Set initial position of the enemy
    rect.x = random.randint(0, 736)
    rect.y = random.randint(50, 150)
    # Append the Rect object to the list
    enemy_rect.append(rect)
    # Set slower constant speed for enemy movement
    enemyX_change.append(1)
    # Set the amount to change the enemy's y position
    enemyY_change.append(30)

# Load bullet image
bullet_image = pygame.image.load('bullet.png')
bullet_rect = bullet_image.get_rect()
bullet_rect.x = 0
bullet_rect.y = 480
bulletY_change = 5
# Bullet state, ready means you can fire, fire means bullet is moving
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 12)

textX = 0
textY = 0

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 32)

def game_over_text(x, y):
    over = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over, (x, y))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

# Function to draw player
def player(x, y):
    screen.blit(player_image, (x, y))

# Function to draw enemy
def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

# Function to draw bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (x + 16, y + 10))

def isCollision(enemy_rect, bullet_rect):
    distance = math.sqrt((math.pow(enemy_rect.x - bullet_rect.x, 2)) + (math.pow(enemy_rect.y - bullet_rect.y, 2)))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handling player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -1
            if event.key == pygame.K_RIGHT:
                playerx_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Getting the current position of the spaceship
                    bullet_rect.x = player_rect.x
                    bullet_rect.y = player_rect.y
                    fire_bullet(bullet_rect.x, bullet_rect.y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    screen.fill((197, 236, 235))
    # Background image
    screen.blit(background, (0, 0))

    player_rect.x += playerx_change

    # Adding boundaries for player
    if player_rect.x <= 0:
        player_rect.x = 0
    elif player_rect.x >= 736:
        player_rect.x = 736

    for i in range(num_of_enemies):
        # Enemies movement
        enemy_rect[i].x += enemyX_change[i]

        # Bounce back when enemy reaches borders
        if enemy_rect[i].x <= 0 or enemy_rect[i].x >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemy_rect[i].y += enemyY_change[i]

        # Check for game over
        if enemy_rect[i].y > 440:  # Adjusted game over condition to a reasonable value
            for j in range(num_of_enemies):
                enemy_rect[j].y = 2000
            game_over_text(200, 250)
            # running = False
            break

        collision = isCollision(enemy_rect[i], bullet_rect)
        if collision:
            bullet_rect.y = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            # Resetting enemy position after collision
            enemy_rect[i].x = random.randint(0, 736)
            enemy_rect[i].y = random.randint(50, 150)

        enemy(enemy_rect[i].x, enemy_rect[i].y, i)

    # Bullet movements
    if bullet_rect.y <= 0:
        bullet_rect.y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_rect.x, bullet_rect.y)
        bullet_rect.y -= bulletY_change

    player(player_rect.x, player_rect.y)
    show_score(textX, textY)
    pygame.display.update()
    # clock.tick(60)
