"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: Annie!!
"""

import pygame
from random import randint

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
start_time = 0

# Game state variables
screen_type = 1 # 1: menu, 2: game, 3: game over
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load sounds
bg_music = pygame.mixer.Sound("audio/music.mp3")
jump_sound = pygame.mixer.Sound("audio/jump.wav")
chomp_sound = pygame.mixer.Sound("audio/chomp1.wav")

bg_music.set_volume(0.7)
bg_music.play(loops = -1)

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))

# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

# Load obstacles
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))
fly_surf = pygame.image.load("graphics/fly_1.png").convert_alpha()

obstacle_rect_list = []

# Load collectibles
#fruit_surf =
#fruit_rect = 

# Load menu screen assets
game_name = game_font.render("CROC RUN",False,"Black")
game_name_rect = game_name.get_rect(center=(400,200))

# Load game over screen assets
game_over_text = game_font.render("Game Over...\nTry again?",False,"White")
game_over_rect = game_over_text.get_rect(center=(400,200))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1600)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacles_rect in obstacle_list:
            obstacles_rect.x -= 5
            
            if obstacles_rect.bottom == GROUND_Y:
                screen.blit(egg_surf,obstacles_rect)
            else:
                screen.blit(fly_surf,obstacles_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect):
                return False
    return True

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    current_time //= 1000
    global score_surf, score_rect
    score_surf = game_font.render(f"{current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)

def menu():
    screen.fill("white")
    screen.blit(game_name,game_name_rect)
    
def game():
    screen.fill("purple")  # Wipe the screen

    # Blit the level assets
    screen.blit(SKY_SURF, (0, 0))
    screen.blit(GROUND_SURF, (0, GROUND_Y))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
    screen.blit(score_surf, score_rect)
    display_score()

def game_over():
    screen.fill("black")
    screen.blit(game_over_text, game_over_rect)

while running:
# Player actions
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if screen_type == 2:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
                jump_sound.play()

        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen_type = 2
                start_time = int(pygame.time.get_ticks())
                obstacle_rect_list = []

        
        if event.type == obstacle_timer and screen_type == 2:
            if randint(0,2):
                obstacle_rect_list.append(egg_surf.get_rect(bottomleft = (randint(800,900),GROUND_Y)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomleft = (randint(800,900),270)))

# Different screens
    # Menu screen
    if screen_type == 1:
        menu()

    # Game screen
    elif screen_type == 2:
        game()
        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        # When player collides with enemy, game over screen
        if collisions(player_rect, obstacle_rect_list) != True:
            screen_type = 3  # Switch to game over screen
        
        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
    # Game over screen
    elif screen_type == 3:
        game_over()

    # Flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
