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
JUMP_GRAVITY_START_SPEED = -22.5  # The speed at which the player jumps
swamp_sprite_fix = 300
players_gravity_speed = 0  # The current speed at which the player falls
current_score = 0
high_score = 0
lives = 3
object_speed = 5

# Pineapple variables
pineapple_active = False
pineapple_start = 0
pineapple_elapsed = pygame.time.get_ticks() - pineapple_start

# Guava variables
guava_active = False
guava_start = 0
guava_elapsed = pygame.time.get_ticks() - guava_start

# Durian variables

# Rainbow variables
rainbow_active = False
rainbow_start = 0
rainbow_elapsed = pygame.time.get_ticks() - rainbow_start

# Load sounds
bg_music = pygame.mixer.Sound("audio/music.mp3")
jump_sound = pygame.mixer.Sound("audio/jump.wav")
chomp_sound = pygame.mixer.Sound("audio/chomp1.wav")
ow_sound = pygame.mixer.Sound("audio/ow.mp3")
sparkle_sound = pygame.mixer.Sound("audio/powerup.wav")
rainbow_sound = pygame.mixer.Sound("audio/rainbow.mp3")

bg_music.set_volume(0.7)
bg_music.play(loops = -1)

# Load level assets
SKY_SURF1 = pygame.image.load("graphics/levels/sky1.png").convert()
GROUND_SURF1 = pygame.image.load("graphics/levels/ground1.png").convert()
SKY_SURF2 = pygame.image.load("graphics/levels/sky2.png").convert()
GROUND_SURF2 = pygame.image.load("graphics/levels/ground2.png").convert()
SKY_SURF3 = pygame.image.load("graphics/levels/sky3.png").convert()
GROUND_SURF3 = pygame.image.load("graphics/levels/ground3.png").convert()
game_font = pygame.font.Font("graphics/texticons/BaiJamjuree-Bold.ttf", 45)

SKY_SURF = SKY_SURF1
GROUND_SURF = GROUND_SURF1

# Load sprite assets
playersurf = pygame.image.load("graphics/player/croc1.png").convert_alpha()
playersurf2 = pygame.image.load("graphics/player/croc2.png").convert_alpha()
player_surf = pygame.transform.scale(playersurf,(125,41))
player_surf_2 = pygame.transform.scale(playersurf2,(125,41))
playerjump = pygame.image.load("graphics/player/croc3.png").convert_alpha()
player_jump = pygame.transform.scale(playersurf2,(125,41))
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
player_walk = [player_surf,player_surf_2]
player_index = 0
player = player_walk[player_index]

# Load obstacles
cactisurf = pygame.image.load("graphics/obstacles/cacti/cacti1.png").convert_alpha()
cactisurf2 = pygame.image.load("graphics/obstacles/cacti/cacti2.png").convert_alpha()
branchsurf = pygame.image.load("graphics/obstacles/branch/branch1.png").convert_alpha()
branchsurf2 = pygame.image.load("graphics/obstacles/branch/branch2.png").convert_alpha()
shrubsurf = pygame.image.load("graphics/obstacles/shrub/shrub1.png").convert_alpha()
shrubsurf2 = pygame.image.load("graphics/obstacles/shrub/shrub2.png").convert_alpha()

cacti_surf = pygame.transform.scale(cactisurf,(55,80))
cacti_surf_2 = pygame.transform.scale(cactisurf2,(55,80))
branch_surf = pygame.transform.scale(branchsurf,(80,80))
branch_surf_2 = pygame.transform.scale(branchsurf2,(80,80))
shrub_surf = pygame.transform.scale(shrubsurf,(60,46))
shrub_surf_2 = pygame.transform.scale(shrubsurf2,(60,46))

plant_surf = cacti_surf
plant_surf_2 = cacti_surf_2

plant_idle = [plant_surf,plant_surf_2]
plant_index = 0
plant = plant_idle[plant_index]

flysurf = pygame.image.load("graphics/obstacles/fly/fly1.png").convert_alpha()
flysurf2 = pygame.image.load("graphics/obstacles/fly/fly2.png").convert_alpha()
fly_surf = pygame.transform.scale(flysurf,(70,50))
fly_surf_2 = pygame.transform.scale(flysurf2,(70,50))
fly_idle = [fly_surf,fly_surf_2]
fly_index = 0
fly = fly_idle[fly_index]

#river_surf = pygame.image.load("graphics/river.png").convert_alpha()

obstacle_rect_list = []

# Load collectibles/powerups
dragonfruit_surf = pygame.image.load("graphics/collectibles/dragonfruit.png").convert_alpha()
dragonfruit = pygame.transform.scale(dragonfruit_surf,(100,100))
lychee_surf = pygame.image.load("graphics/collectibles/lychee.png").convert_alpha()
lychee = pygame.transform.scale(lychee_surf,(100,90))

guava_surf = pygame.image.load("graphics/collectibles/guava.png").convert_alpha()
guava = pygame.transform.scale(guava_surf,(100,100))
pineapple_surf = pygame.image.load("graphics/collectibles/pineapple.png").convert_alpha()
pineapple = pygame.transform.scale(pineapple_surf,(100,100))

rainbow_surf = pygame.image.load("graphics/collectibles/mango.png").convert_alpha()
rainbow = pygame.transform.scale(rainbow_surf,(100,100))

collectible_rect_list = []
powerup_rect_list = []
rainbow_rect_list = []

# Load menu screen assets
game_name = game_font.render("CROC RUN\nPlay (ENTER)\nHow to play (H)\nLevels (L)",False,"Black")
game_name_rect = game_name.get_rect(center=(400,200))

# Load levels screen assets
levels_text = game_font.render("Levels\nDESERT: Press 1\nSWAMP: Press 2\nJUNGLE: Press 3\nMENU: Press M",False,"Black")
levels_rect = levels_text.get_rect(center=(400,180))

# Load game over screen assets
game_over_text = game_font.render("Game Over...\nTry again (ENTER)\nBack to menu (M)",False,"White")
game_over_rect = game_over_text.get_rect(center=(550,200))
leaderboard_text = game_font.render(f"High score:\n{high_score}",False,"White")
leaderboard_rect = leaderboard_text.get_rect(center=(180,200))

# Load powerup text assets
pineapple_left = (5000 - (pygame.time.get_ticks() - pineapple_start)) // 1000
pineapple_text = game_font.render(f"High jump:\n{pineapple_left}s", False, "Black")
guava_text = game_font.render("+1 life", False, "Black")
rainbow_left = (5000 - (pygame.time.get_ticks() - rainbow_start)) // 1000
rainbow_text = game_font.render(f"Invincibility:\n{rainbow_left}s", False, "Black")

# Load icons
heart_surf = pygame.image.load("graphics/texticons/heart.png").convert_alpha()
heart = pygame.transform.scale(heart_surf,(50,50))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1600)

collectible_timer = pygame.USEREVENT + 2
pygame.time.set_timer(collectible_timer,2000)

powerup_timer = pygame.USEREVENT + 3
pygame.time.set_timer(powerup_timer,9000)

rainbow_timer = pygame.USEREVENT + 4
pygame.time.set_timer(rainbow_timer,20000)

speed_timer = pygame.USEREVENT + 5
pygame.time.set_timer(speed_timer,1)

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
    global plant, plant_index, fly, fly_index
    plant_idle = [plant_surf,plant_surf_2]

    plant_index += 0.1
    fly_index += 0.1
    if plant_index >= len(plant_idle):
        plant_index = 0
    if fly_index >= len(fly_idle):
        fly_index = 0
    plant = plant_idle[int(plant_index)]
    fly = fly_idle[int(fly_index)]

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacles_rect in obstacle_list:
            obstacles_rect.x -= object_speed
            
            if obstacles_rect.bottom == swamp_sprite_fix:
                screen.blit(plant,obstacles_rect) 
            else:
                screen.blit(fly,obstacles_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collectible_movement(collectible_list):
    if collectible_list:
        for collectibles_rect in collectible_list:
            collectibles_rect.x -= object_speed

            if collectibles_rect.bottom == 310:
                screen.blit(dragonfruit,collectibles_rect)
            else:
                screen.blit(lychee,collectibles_rect)
            
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

def powerup_movement(powerup_list):
    global powerups_rect
    if powerup_list:
        for powerups_rect in powerup_list:
            powerups_rect.x -= object_speed

            if powerups_rect.bottom == 310:
                screen.blit(pineapple,powerups_rect)
            else:
                screen.blit(guava,powerups_rect)
            
        powerup_list = [powerup for powerup in powerup_list if powerup.x > -100]
        return powerup_list
    else: return []

def get_powerup(player,powerups):
    if powerups:
        for powerup_rect in powerups:
            if player.colliderect(powerup_rect):
                powerups.remove(powerup_rect)
                return False
    return True

def rainbow_movement(rainbow_list):
    global rainbows_rect
    if rainbow_list:
        for rainbows_rect in rainbow_list:
            rainbows_rect.x -= object_speed

            screen.blit(rainbow,rainbows_rect)
            
        rainbow_list = [rainbow for rainbow in rainbow_list if rainbow.x > -100]
        return rainbow_list
    else: return []

def get_rainbow(player,rainbows):
    if rainbows:
        for rainbow_rect in rainbows:
            if player.colliderect(rainbow_rect):
                rainbows.remove(rainbow_rect)
                return False
    return True
 
def display_score():
    global object_speed
    current_time = pygame.time.get_ticks() - start_time
    current_time //= 1000
    global time_surf, time_rect, score_surf, score_rect, heart

    # Object speed
    for second in range(current_time):
        object_speed += 0.00005
    
    time_surf = game_font.render(f"Time: {current_time}", False, "Black")
    time_rect = time_surf.get_rect(center=(400,50))

    score_surf = game_font.render(f"Score: {current_score}", False, "Black")
    score_rect = score_surf.get_rect(center=(400,90))

    screen.blit(time_surf,time_rect)
    screen.blit(score_surf,score_rect)

def menu():
    screen.blit(SKY_SURF, (0, 0))
    screen.blit(GROUND_SURF, (0, GROUND_Y))
    screen.fill("white")
    screen.blit(game_name,game_name_rect)

def howtoplay():
    screen.blit(SKY_SURF, (0, 0))
    screen.blit(GROUND_SURF, (0, GROUND_Y))

def levels():
    screen.blit(SKY_SURF, (0, 0))
    screen.blit(GROUND_SURF, (0, GROUND_Y))
    screen.blit(levels_text,levels_rect)

def game():
    screen.fill("purple")  # Wipe the screen

    # Blit the level assets
    screen.blit(SKY_SURF, (0, 0))
    screen.blit(GROUND_SURF, (0, GROUND_Y))
    display_score()

def game_over():
    screen.fill("black")
    screen.blit(game_over_text, game_over_rect)
    leaderboard_text = game_font.render(f"High score:\n{high_score}",False,"White")
    screen.blit(leaderboard_text, leaderboard_rect)

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    SKY_SURF = SKY_SURF1
                    GROUND_SURF = GROUND_SURF1
                    plant_surf = cacti_surf
                    plant_surf_2 = cacti_surf_2
                    swamp_sprite_fix = 300
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    SKY_SURF = SKY_SURF2
                    GROUND_SURF = GROUND_SURF2
                    plant_surf = branch_surf
                    plant_surf_2 = branch_surf_2
                    swamp_sprite_fix = 320
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    SKY_SURF = SKY_SURF3
                    GROUND_SURF = GROUND_SURF3
                    plant_surf = shrub_surf
                    plant_surf_2 = shrub_surf_2
                    swamp_sprite_fix = 300

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
            # When player wants to play again by pressing ENTER
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                screen_type = 2
                menu_type = 1
                start_time = int(pygame.time.get_ticks())
                current_score = 0
                lives = 3
                JUMP_GRAVITY_START_SPEED = -22.5
                pineapple_active = False
                guava_active = False
                rainbow_active = False
                object_speed = 5
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                screen_type = 1
                start_time = int(pygame.time.get_ticks())
                current_score = 0
                lives = 3
                JUMP_GRAVITY_START_SPEED = -22.5
                pineapple_active = False
                guava_active = False
                rainbow_active = False
                object_speed = 5
        
        if event.type == obstacle_timer and screen_type == 2:
            if randint(0,2):
                obstacle_rect_list.append(plant.get_rect(bottomleft = (randint(800,900),swamp_sprite_fix)))
            else:
                obstacle_rect_list.append(fly.get_rect(bottomleft = (randint(800,900),280)))
        
        if event.type == collectible_timer and screen_type == 2:
            if randint(0,2):
                collectible_rect_list.append(dragonfruit.get_rect(bottomleft = (randint(800,900),310)))
            else:
                collectible_rect_list.append(lychee.get_rect(bottomleft = (randint(800,900),230)))
        
        if event.type == powerup_timer and screen_type == 2:
            if randint(0,2):
                powerup_rect_list.append(pineapple.get_rect(bottomleft = (randint(800,2000),310)))
            else:
                powerup_rect_list.append(guava.get_rect(bottomleft = (randint(800,2000),301)))

        if event.type == rainbow_timer and screen_type == 2:
            rainbow_rect_list.append(rainbow.get_rect(bottomleft = (randint(800,2000),310)))


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
        if rainbow_active == False:
            if collisions(player_rect, obstacle_rect_list) != True:
                lives -= 1
                player = player_jump
                ow_sound.play()
        
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
            collectible_rect_list = []
            powerup_rect_list = []
            if current_score > high_score:
                high_score = current_score

        # If player collects collectible, add to score
        if collections(player_rect, collectible_rect_list) != True:
            current_score += 1
            chomp_sound.play()

        # If player collides with powerup, add powerup condition
        if get_powerup(player_rect, powerup_rect_list) != True:
            sparkle_sound.play()
            if powerups_rect.bottom == 310:
                pineapple_active = True
                pineapple_start = pygame.time.get_ticks()
                pineapple_left = max(0, 5000 - (pygame.time.get_ticks() - pineapple_start)) // 1000
                JUMP_GRAVITY_START_SPEED = -25
            elif powerups_rect.bottom != 310 and lives < 3:
                lives += 1
                guava_active = True
                guava_start = pygame.time.get_ticks()
                
        # Make pineapple condition stop after 10 seconds
        if pineapple_active == True:
            pineapple_elapsed = pygame.time.get_ticks() - pineapple_start
            pineapple_left = max(0, 5000 - pineapple_elapsed) // 1000
        # Blit pineapple timer text
            pineapple_text = game_font.render(f"High jump:\n{pineapple_left}s", False, "Black")
            if rainbow_active == False:
                screen.blit(pineapple_text, (22, 20))
        
        # Check if expired
        if pineapple_elapsed > 5000:
            pineapple_active = False
            JUMP_GRAVITY_START_SPEED = -22.5

        # Make guava text blit
        if guava_active == True and rainbow_active == False:
            guava_elapsed = pygame.time.get_ticks() - guava_start
            screen.blit(guava_text, (22,20))

        # Stop it from blitting after 1 seconds
        if guava_elapsed > 1000:
            guava_active = False

        # If player collides with rainbow fruit, invincibility
        if get_rainbow(player_rect, rainbow_rect_list) != True:
            rainbow_sound.play()
            rainbow_active = True
            rainbow_start = pygame.time.get_ticks()
            rainbow_left = max(0, 5000 - (pygame.time.get_ticks() - rainbow_start)) // 1000

        # Make invincible condition stop after 10 seconds
        if rainbow_active == True:
            rainbow_elapsed = pygame.time.get_ticks() - rainbow_start
            rainbow_left = max(0, 5000 - rainbow_elapsed) // 1000
        # Blit rainbow timer text
            rainbow_text = game_font.render(f"Invincibility:\n{rainbow_left}s", False, "Black")
            screen.blit(rainbow_text, (22, 20))
        
        # Check if expired
        if rainbow_elapsed > 5000:
            rainbow_active = False
        
        #Obstacle & collectible movement
        collectible_rect_list = collectible_movement(collectible_rect_list)
        powerup_rect_list = powerup_movement(powerup_rect_list)
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        rainbow_rect_list = rainbow_movement(rainbow_rect_list)
        
    # Game over screen
    elif screen_type == 3:
        game_over()

    # Flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()