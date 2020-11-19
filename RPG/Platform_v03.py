import pygame, sys
from pygame.locals import *
pygame.init()
 
WINDOW_SIZE = (1000, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption('Platformer_v01') # Window Name

 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
 
clock = pygame.time.Clock()
 
background = pygame.image.load("C:/code/Pygame/RPG/Images/sky.jpg")
 
character = pygame.image.load('C:/code/Pygame/RPG/Images/blue.png')

# Moving Left / Right
moving_right = False
moving_left = False

# Momentum X / Y
player_x_momentum = 0
player_y_momentum = 0

# Location X / Y
player_x_location = 50
player_y_location = 50

player_max_speed = 5

jump_movement_disabled = False

player_rect = pygame.Rect(player_x_location,player_y_momentum,character.get_width(),character.get_height())
test_rect = pygame.Rect(100,100,100,50)


in_game = True
font = pygame.font.Font(None, 36)
screen.blit(background, (0, 0))
pygame.display.flip()
while in_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_game = False



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
        if event.type == KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False

    # Movement
    if moving_right == True:
        player_x_location += player_max_speed
    if moving_left == True:
        player_x_location -= player_max_speed
    
    ##Update
    # player_x_location += 3
    # player_y_location += 3

    # Bounce
    if player_y_location > WINDOW_SIZE[1]-character.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_y_location += player_y_momentum

    # Movement
    # if moving_right == True:
        # player_x_location += player_max_speed
    # if moving_left == True:
        # player_x_location -= player_max_speed

    


    player_rect.x = player_x_location # update rect x
    player_rect.y = player_y_location # update rect y

    # test rect for collisions
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen,(255,0,0),test_rect)
    else:
        pygame.draw.rect(screen,(0,0,0),test_rect)

    # test rect for collisions
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen,(255,0,0),test_rect)
    else:
        pygame.draw.rect(screen,(0,0,0),test_rect)
    

    ##Draw
    text = font.render("Time : " + str(pygame.time.get_ticks()), 1, WHITE)
    screen.blit(background, (0, 0))
    screen.blit(text, (50, 50))
    screen.blit(character, (player_x_location, player_y_location))
    pygame.display.update(0,0,1000,600)
    clock.tick(60)
 
 
pygame.quit()