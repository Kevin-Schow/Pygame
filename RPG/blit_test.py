import pygame
pygame.init()
 
size = (800, 600)
screen = pygame.display.set_mode(size)
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
 
clock = pygame.time.Clock()
 
background = pygame.image.load("C:/code/Pygame/RPG/Images/sky.jpg")
 
character = pygame.image.load('C:/code/Pygame/RPG/Images/blue.png')
x = 50
y = 50
in_game = True
font = pygame.font.Font(None, 36)
screen.blit(background, (0, 0))
pygame.display.flip()
while in_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_game = False
    
    ##Update
    x += 5
    y += 5
    ##Draw
    text = font.render("Time : " + str(pygame.time.get_ticks()), 1, WHITE)
    screen.blit(background, (0, 0))
    screen.blit(text, (50, 50))
    screen.blit(character, (x, y))
    pygame.display.update(0,0,400,400)
    clock.tick(60)
 
 
pygame.quit()