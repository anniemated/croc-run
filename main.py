"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: Annie!!
Hash: e7f59b4
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
menu_type = 1 # 1: menu, 2: how to play/controls, 3: level select
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
current_score = 0
lives = 3

# Load sounds
bg_music = pygame.mixer.Sound("audio/music.mp3")
jump_sound = pygame.mixer.Sound("audio/jump.wav")
chomp_sound = pygame.mixer.Sound("audio/chomp1.wav")

bg_music.set_volume(0.7)
bg_music.play(loops = -1)

# Load level assets
SKY_SURF = pygame.image.load("graphics/levels/sky1.png").convert()
GROUND_SURF = pygame.image.load("graphics/levels/ground1.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)

# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_surf_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
player_walk = [player_surf,player_surf_2]
player_index = 0
player = player_walk[player_index]

# Load obstacles
cacti_surf = pygame.image.load("graphics/obstacles/egg/egg_1.png").convert_alpha()
cacti_surf_2 = pygame.image.load("graphics/obstacles/egg/egg_2.png").convert_alpha()
cacti_idle = [cacti_surf,cacti_surf_2]
cacti_index = 0
cacti = cacti_idle[cacti_index]

fly_surf = pygame.image.load("graphics/obstacles/fly/fly_1.png").convert_alpha()
fly_surf_2 = pygame.image.load("graphics/obstacles/fly/fly_2.png").convert_alpha()
fly_idle = [fly_surf,fly_surf_2]
fly_index = 0
fly = fly_idle[fly_index]

#river_surf = pygame.image.load("graphics/river.png").convert_alpha()

obstacle_rect_list = []

# Load collectibles
orange_surf = pygame.image.load("graphics/collectibles/orange.png").convert_alpha()
orange = pygame.transform.scale(orange_surf,(50,50))
apple_surf = pygame.image.load("graphics/collectibles/apple.png").convert_alpha()
apple = pygame.transform.scale(apple_surf,(50,50))

collectible_rect_list = []

# Load menu screen assets
game_name = game_font.render("CROC RUN\nPlay (SPACE)\nHow to play (H)\nLevels (L)",False,"Black")
game_name_rect = game_name.get_rect(center=(400,200))

# Load game over screen assets
game_over_text = game_font.render("Game Over...\nTry again (SPACE)\nBack to menu (M)",False,"White")
game_over_rect = game_over_text.get_rect(center=(400,200))

# Load icons
heart_surf = pygame.image.load("graphics/icons/heart.png").convert_alpha()
heart = pygame.transform.scale(heart_surf,(50,50))


#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1600)

collectible_timer = pygame.USEREVENT + 2
pygame.time.set_timer(collectible_timer,2000)

def player_animation():
    # Animated while walking
    global player, player_index

    if player_rect.bottom < GROUND_Y:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]

def obstacle_animation():
    # Obstacles always idle
    global cacti, cacti_index, fly, fly_index
    cacti_index += 0.1
    fly_index += 0.1
    if cacti_index >= len(cacti_idle):
        cacti_index = 0
    if fly_index >= len(fly_idle):
        fly_index = 0
    cacti = cacti_idle[int(cacti_index)]
    fly = fly_idle[int(fly_index)]

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacles_rect in obstacle_list:
            obstacles_rect.x -= 5
            
            if obstacles_rect.bottom == GROUND_Y:
                screen.blit(cacti,obstacles_rect) 
            else:
                screen.blit(fly,obstacles_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collectible_movement(collectible_list):
    if collectible_list:
        for collectibles_rect in collectible_list:
            collectibles_rect.x -= 5

            if collectibles_rect.bottom == GROUND_Y:
                screen.blit(orange,collectibles_rect)
            else:
                screen.blit(apple,collectibles_rect)
            
        collectible_list = [collectible for collectible in collectible_list if collectible.x > -100]
        return collectible_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect):
                obstacles.remove(obstacles_rect)
                return False
    return True

def collections(player,collectibles):
    global current_score
    if collectibles:
        for collectibles_rect in collectibles:
            if player.colliderect(collectibles_rect):
                collectibles.remove(collectibles_rect)
                return False
    return True

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    current_time //= 1000
    global time_surf, time_rect, score_surf, score_rect, heart
    
    time_surf = game_font.render(f"Time: {current_time}", False, (64,64,64))
    time_rect = time_surf.get_rect(center=(400,50))

    score_surf = game_font.render(f"Score: {current_score}", False, (64,65,64))
    score_rect = score_surf.get_rect(center=(400,90))

    screen.blit(time_surf,time_rect)
    screen.blit(score_surf,score_rect)

def menu():
    screen.fill("white")
    screen.blit(game_name,game_name_rect)

def howtoplay():
    screen.fill("black")

def levels():
    screen.fill("Black")

def game():
    screen.fill("purple")  # Wipe the screen

    # Blit the level assets
    screen.blit(SKY_SURF, (0, 0))
    screen.blit(GROUND_SURF, (0, GROUND_Y))
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
        
        # Menu actions
        if screen_type == 1:
            if menu_type == 1:
                menu()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    menu_type = 2
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    menu_type = 3
            elif menu_type == 2:
                howtoplay()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_h or event.key == pygame.K_m):
                    menu_type = 1
            elif menu_type == 3:
                levels()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_l or event.key == pygame.K_m):
                    menu_type = 1

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
                current_score = 0
                lives = 3
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                screen_type = 1
                start_time = int(pygame.time.get_ticks())
                current_score = 0
                lives = 3
        
        if event.type == obstacle_timer and screen_type == 2:
            if randint(0,2):
                obstacle_rect_list.append(cacti.get_rect(bottomleft = (randint(800,900),GROUND_Y)))
            else:
                obstacle_rect_list.append(fly.get_rect(bottomleft = (randint(800,900),280)))
        
        if event.type == collectible_timer and screen_type == 2:
            if randint(0,2):
                collectible_rect_list.append(orange.get_rect(bottomleft = (randint(800,900),GROUND_Y)))
            else:
                collectible_rect_list.append(apple.get_rect(bottomleft = (randint(800,900),230)))

    if screen_type == 2:
        game()
        player_animation()
        obstacle_animation()

        # Adjust player's vertical location then blits it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player, player_rect)

        # If player collides with obstacle, remove 1 life
        if collisions(player_rect, obstacle_rect_list) != True:
            lives -= 1
        
        # Remove hearts on screen when lives are lost
        if lives == 3:
            screen.blit(heart,(600,20))
            screen.blit(heart,(660,20))
            screen.blit(heart,(720,20))
        elif lives == 2:
            screen.blit(heart,(660,20))
            screen.blit(heart,(720,20))
        elif lives == 1:
            screen.blit(heart,(720,20))
        elif lives == 0:
            screen_type = 3
            obstacle_rect_list = []

        # If player collects collectible, add to score
        if collections(player_rect, collectible_rect_list) != True:
            current_score += 1
            chomp_sound.play()
        
        #Obstacle & collectible movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        collectible_rect_list = collectible_movement(collectible_rect_list)
        
    # Game over screen
    elif screen_type == 3:
        game_over()

    # Flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()