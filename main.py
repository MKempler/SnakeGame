import pygame
import sys
import time
import random

snake_speed = 20

# Window size
window_size_x = 720
window_size_y = 480

pygame.init()

# game window
pygame.display.set_caption('Maxs Snake Game')
game_window = pygame.display.set_mode((window_size_x, window_size_y))

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS
fps_controller = pygame.time.Clock()

# Default snake position
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# food
food_pos = [random.randrange(1, (window_size_x // 10)) * 10, random.randrange(1, (window_size_y // 10)) * 10]
food_spawn = True

# defaults
direction = 'RIGHT'
change_to = direction
score = 0


# Game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_size_x / 2, window_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_size_x / 10, 15)
    else:
        score_rect.midtop = (window_size_x / 2, window_size_y / 1.25)
    game_window.blit(score_surface, score_rect)


# Main function
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key press
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Not letting the snake move in multiple directions at once
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing
    # If snake collides with food score increases by 10
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food
    if not food_spawn:
        food_pos = [random.randrange(1, (window_size_x // 10)) * 10, random.randrange(1, (window_size_y // 10)) * 10]
    food_spawn = True

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 15, 15))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 15, 15))

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > window_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > window_size_y - 10:
        game_over()
    # Snake touches snake
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, red, 'times', 20)

    # Refresh game screen
    pygame.display.update()
    fps_controller.tick(snake_speed)
