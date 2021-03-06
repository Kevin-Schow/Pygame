import pygame, sys, os, random
import data.engine as e
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1280,720)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((640,360)) # used as the surface for rendering, which is scaled

e.set_global_colorkey((203,217,217))

player_width = 32
player_height = 64

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0,0]

SPRITE_SIZE = 32
CHUNK_SIZE = 8

# def perfect_outline(img, loc):
#     mask = pygame.mask.from_surface(img)
#     mask_outline = mask.outline()
#     mask_surf = pygame.Surface(img.get_size())
#     for pixel in mask_outline:
#         mask_surf.set_at(pixel, (255, 255, 255))
#     mask_surf.set_colorkey((0, 0, 0))
#     display.blit(mask_surf, (loc[0]-1, loc[1]))
#     display.blit(mask_surf, (loc[0]+1, loc[1]))
#     display.blit(mask_surf, (loc[0], loc[1]-1))
#     display.blit(mask_surf, (loc[0], loc[1]+1))


def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            if target_y > 10:
                tile_type = 2 # dirt
            elif target_y == 10:
                tile_type = 1 # grass
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3 # plant
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data

class jumper_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(jumper_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 64, 16)

    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)


# e.load_animations('data/images/entities/')
e.load_animations('C:/code/Pygame/RPG/data/images/entities/')



game_map = {}

grass_img = pygame.image.load('data/images/grass_tile.png')
dirt_img = pygame.image.load('data/images/dirt_tile.png')
plant_img = pygame.image.load('data/images/plant_tile.png').convert()
plant_img.set_colorkey((203,217,217)) # colorkey

jumper_img = pygame.image.load('data/images/jumper.png').convert()
jumper_img.set_colorkey((203,217,217)) # colorkey


tile_index = {1:grass_img,
              2:dirt_img,
              3:plant_img
              }

jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
grass_sounds = [pygame.mixer.Sound('data/audio/grass_0.wav'),pygame.mixer.Sound('data/audio/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('data/audio/music.wav')
pygame.mixer.music.play(-1)

grass_sound_timer = 0

player = e.entity(600, 200, player_width, player_height,'player')

# player_img.get_width(),player_img.get_height()

enemies = []

for i in range (5):
    # enemies.append(0,e.entity(random.randint(0, 600) - 300, 80, 32, 32, 'enemy'))
    enemies.append([0,e.entity(random.randint(0,600)-300,80,32,32,'enemy')])




background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

jumper_objects = []

for i in range(5):
    jumper_objects.append(jumper_obj((random.randint(0, 600) - 500, 304)))

while True: # game loop -----------------------------------------
    display.fill((146,244,255)) # clear screen by filling it with blue


    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player.x-true_scroll[0]-250)/20
    true_scroll[1] += (player.y-true_scroll[1]-232)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(20,170,150),obj_rect)
        else:
            pygame.draw.rect(display,(15,76,73),obj_rect)

    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*SPRITE_SIZE)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*SPRITE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*SPRITE_SIZE-scroll[0],tile[0][1]*SPRITE_SIZE-scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*SPRITE_SIZE,tile[0][1]*SPRITE_SIZE,SPRITE_SIZE,SPRITE_SIZE))    

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(False)
        player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(True)
        player.set_action('run')

    collision_types = player.move(player_movement,tile_rects)

    if collision_types['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player.change_frame(1)
    player.display(display,scroll)

    # player.perfect_outline(player.get_current_img(),(player.x, player.y), display)



    for jumper in jumper_objects:
        jumper.render(display, scroll)
        if jumper.collision_test(player.obj.rect):
            vertical_momentum = -8
            # player_money += 1 (can turn jumper into other types)
            # player_health -= 1

    # Handles Off Screen Enemies
    display_r = pygame.Rect(scroll[0], scroll[1], 640, 360)

    for enemy in enemies:
        if display_r.colliderect(enemy[1].obj.rect):
            enemy[0] += 0.2
            if enemy[0] > 3:
                enemy[0] = 3

            enemy_movement = [0, enemy[0]]
            if player.x > enemy[1].x + 5:
                enemy_movement[0] = 1
            if player.x < enemy[1].x - 5:
                enemy_movement[0] = -1
            collision_types = enemy[1].move(enemy_movement, tile_rects)
            if collision_types['bottom'] == True:
                enemy[0] = 0

            enemy[1].display(display, scroll)

            if player.obj.rect.colliderect(enemy[1].obj.rect):
                vertical_momentum = -4

    for event in pygame.event.get(): # Buttons ----------------------
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
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
