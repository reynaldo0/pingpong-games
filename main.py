import pygame
import sys

def ball_animation():
    global ball_speed_x, ball_speed_y
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT
# General setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT / 2 - 15, 30, 30)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # Game logic
    ball_animation()
    player_animation()
    opponent_ai()

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
