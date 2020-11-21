import pygame, sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init() # initiates pygame

pygame.display.set_caption('Platformer')
WINDOW_SIZE = (1280,720)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((640,360)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
player_speed = 3
SPRITE_SIZE = 32
true_scroll = [0,0]

global animation_frames
animation_frames = {}
global animation_name
animation_name =''
global player_img
player_img = pygame.image.load('C:/code/Pygame/RPG/Images/32x64.png') # .convert()


def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


def load_animation(path,frame_durations): # [7, 7]
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animation/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((203,217,217))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

# # load_animation('C:/code/Pygame/RPG/Images/player_animation/idle', [7, 7, 40])

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


animation_database = {}

animation_database['run'] = load_animation('C:/code/Pygame/RPG/Images/player_animation/run', [11, 11])
animation_database['idle'] = load_animation('C:/code/Pygame/RPG/Images/player_animation/idle', [7, 7, 40])

player_action = 'idle'
player_frame = 0
player_flip = False

game_map = load_map('C:/code/Pygame/RPG/Maps/map_02.txt')

grass_img = pygame.image.load('C:/code/Pygame/RPG/Images/grass_tile.png')
dirt_img = pygame.image.load('C:/code/Pygame/RPG/Images/dirt_tile.png')

jump_sound = pygame.mixer.Sound('C:/code/Pygame/RPG/Images/sound/jump.wav')
grass_sounds = [pygame.mixer.Sound('C:/code/Pygame/RPG/Images/sound/grass_1.wav'), pygame.mixer.Sound('C:/code/Pygame/RPG/Images/sound/grass_2.wav')]

pygame.mixer.music.load('C:/code/Pygame/RPG/Images/sound/music.wav')
pygame.mixer.music.play(-1)

# player_img = pygame.image.load('C:/code/Pygame/RPG/Images/32x64.png') # .convert()

player_rect = pygame.Rect(100,100,player_img.get_width(),player_img.get_height())

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue

    true_scroll[0] += (player_rect.x-true_scroll[0]-250)/20 # Camera Control X
    true_scroll[1] += (player_rect.y-true_scroll[1]-200)/20 # Camera Control X
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # Paralax Effect
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,280,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img,(x*SPRITE_SIZE-scroll[0],y*SPRITE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*SPRITE_SIZE-scroll[0],y*SPRITE_SIZE-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*SPRITE_SIZE,y*SPRITE_SIZE,SPRITE_SIZE,SPRITE_SIZE))
            x += 1
        y += 1


    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += player_speed
    if moving_left == True:
        player_movement[0] -= player_speed
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_m:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                if air_timer < 6:
                    jump_sound.play()
                    vertical_momentum -= 5
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
