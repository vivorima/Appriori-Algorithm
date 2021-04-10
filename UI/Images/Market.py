import pygame

# Initialisation
pygame.init()

# Screen
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('SuperMarket')
pygame.display.set_icon(pygame.image.load('food.png'))

# FPS
clock = pygame.time.Clock()

def gameLogic():

    # background image
    image = pygame.image.load('Supermarket.jpg',(0,0) )














#GAME LOOP: Sortir si on appuie sur X
running = True
while running:
    # events is a keyboard or mouse event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # background color
    screen.fill((150,40,20))
    gameLogic()
    # pour update the screen
    pygame.display.update()
    clock.tick(60) # 60FPS

# quitter le jeu
pygame.quit()
quit()


