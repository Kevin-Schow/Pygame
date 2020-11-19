import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

# Initiates Pygame
pygame.init() # Initiate Pygame

pygame.display.set_caption('Platformer_v01') # Window Name

WINDOW_SIZE = (400, 400) # Window Size
# Initiates the window
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

player_image = pygame.image.load('C:/code/Pygame/RPG/Images/blue.png')

moving_right = False
moving_left = False

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

# Game Loop
while True:
	screen.fill((146,244,255)) # clear screen by filling it with blue

	screen.blit(player_image, player_location)

	# Bounce
	if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
		player_y_momentum = -player_y_momentum
	else:
		player_y_momentum += 0.2
	player_location[1] += player_y_momentum

	# Movement
	if moving_right == True:
		player_location[0] += 1
	if moving_left == True:
		player_location[0] -= 1

	player_rect.x = player_location[0] # update rect x
	player_rect.y = player_location[1] # update rect y
 
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


	# Exit Program
	for event in pygame.event.get(): # event loop
		if event.type == QUIT: # check for window quit
			pygame.quit() # stop pygame
			sys.exit() # stop script
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True
			if event.key == K_LEFT:
				moving_left = True
			if event.type == KEYUP:
				if event.key == K_RIGHT:
					moving_right = False
				if event.key == K_LEFT:
					moving_left = False

		pygame.display.update() # Update Display
		clock.tick(60) # Maintain 60 fps

