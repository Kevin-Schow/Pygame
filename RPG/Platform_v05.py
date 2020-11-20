import pygame, sys
from pygame.locals import *
pygame.init()
 
WINDOW_SIZE = (1000, 600)
display = pygame.Surface((1000, 600))
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)



pygame.display.set_caption('Platformer_v01') # Window Name

 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

tile_rects = []

global player_movement
max_fall_speed = 8
fall_speed = 0.5
 
 
clock = pygame.time.Clock()
 
background = pygame.image.load("C:/code/Pygame/RPG/Images/sky.jpg")
 
character = pygame.image.load('C:/code/Pygame/RPG/Images/blue.png')
# character.set_colorkey((255, 255, 255))

grass_tile = pygame.image.load('C:/code/Pygame/RPG/Images/grass_tile.png')
dirt_tile = pygame.image.load('C:/code/Pygame/RPG/Images/dirt_tile.png')
TILE_SIZE = grass_tile.get_width()


game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

def collision_test(rect, tiles):
    # returns a list of tiles touching
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
        return hit_list


def move(rect, player_x_momentum, player_y_momentum, tiles):
    collision_types = {'top': False,'bottom': False, 'right': False, 'left': False}
    rect.x += player_x_momentum
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if player_x_momentum > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif player_x_momentum < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += player_y_momentum
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if player_y_momentum > 0:
            rect.bottom = tile.top
            collision_types['botttom'] = True
        elif player_y_momentum < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types




# Moving Left / Right
moving_right = False
moving_left = False

# Momentum X / Y
player_x_momentum = 0
player_y_momentum = 0

# Location X / Y
# player_x_location = 50
# player_y_location = 50

player_max_speed = 5

jump_movement_disabled = False

player_movement = [0, 0] # Velocity of Player ( Not position of player)


player_rect = pygame.Rect(50, 50, character.get_width(),character.get_height())
test_rect = pygame.Rect(100,100,100,50)


in_game = True
font = pygame.font.Font(None, 36)
display.blit(background, (0, 0))
pygame.display.flip()

while in_game: # Game Loop
    tile_rects = []

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


    # Player Movement / Velocity
    player_movement = [0, 0] # Velocity of Player ( Not position of player)
    if moving_right:
        player_movement[0] += player_max_speed
    if moving_left:
        player_movement[0] -= player_max_speed
    player_movement[1] += player_y_momentum
    player_y_momentum += fall_speed
    if player_y_momentum > max_fall_speed:
        player_y_momentum = max_fall_speed

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    display.blit(character, player_rect.x, player_rect.y)






    # Old Movement
    # if moving_right == True:
        # player_x_location += player_max_speed
    # if moving_left == True:
        # player_x_location -= player_max_speed
    # player_rect.x = player_x_location # update rect x
    # player_rect.y = player_y_location # update rect y
    
    ##Update
    # player_x_location += 3
    # player_y_location += 3

    # Bounce
    # if player_y_location > WINDOW_SIZE[1]-character.get_height():
        # player_y_momentum = -player_y_momentum
    # else:
        # player_y_momentum += 0.2
    # player_y_location += player_y_momentum

    

    



    

    ##Draw
    text = font.render("Time : " + str(pygame.time.get_ticks()), 1, WHITE)
    display.blit(background, (0, 0))
    display.blit(text, (50, 50))
    display.blit(character, (player_movement[0], player_movement[1]))
    
        # Map Tiles
    # tile_rects = []
    map_row_y = 0
    for row in game_map:
        map_row_x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_tile, (map_row_x * TILE_SIZE, map_row_y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_tile, (map_row_x * TILE_SIZE, map_row_y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(map_row_x * TILE_SIZE, map_row_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            map_row_x += 1
        map_row_y += 1




    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update(0,0,1000,600)
    clock.tick(60)
 
 
pygame.quit()