import pygame
import sys
import random

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Colors
BLUE_COLOR = (55, 255, 255)
bg_color = pygame.Color('grey12')
BLACK_COLOR = (0, 0, 0)

# Game Rectangles
ball = pygame.Rect(SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT / 2 - 15, 20, 20)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 70, 10, 140)
opponent = pygame.Rect(10, SCREEN_HEIGHT / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# text variable
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)
start_font = pygame.font.Font("freesansbold.ttf", 100)

# sound effect
pong_sound = pygame.mixer.Sound("music/pong.ogg")
score_sound = pygame.mixer.Sound("music/score.ogg")

# score timer
score_time = True

def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    countdown_pos = (SCREEN_WIDTH / 2 - 5, SCREEN_HEIGHT / 2 - 200)

    if current_time - score_time < 700:
        pygame.draw.circle(screen, BLUE_COLOR, countdown_pos, 50)
        num3_time = start_font.render('3', False, BLACK_COLOR)
        screen.blit(num3_time, num3_time.get_rect(center=countdown_pos))

    if 700 < current_time - score_time < 1400:
        pygame.draw.circle(screen, BLUE_COLOR, countdown_pos, 50)
        num2_time = start_font.render('2', False, BLACK_COLOR)
        screen.blit(num2_time, num2_time.get_rect(center=countdown_pos))


    if 1400 < current_time - score_time < 2100:
        pygame.draw.circle(screen, BLUE_COLOR, countdown_pos, 50)
        num1_time = start_font.render('1', False, BLACK_COLOR)
        screen.blit(num1_time, num1_time.get_rect(center=countdown_pos))


    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0 
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # player score 
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
    
    # ai score
    if ball.right >= SCREEN_WIDTH:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

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
    pygame.draw.rect(screen, BLUE_COLOR, player)
    pygame.draw.rect(screen, BLUE_COLOR, opponent)
    pygame.draw.ellipse(screen, BLUE_COLOR, ball)
    pygame.draw.aaline(screen, BLUE_COLOR, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    if score_time:
        ball_start()
        
    player_text = game_font.render(f"{player_score}", False, BLUE_COLOR)
    screen.blit(player_text,(420, 330))

    opponent_text = game_font.render(f"{opponent_score}", False, BLUE_COLOR)
    screen.blit(opponent_text,(360, 330))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
