import pygame

SIRINA, VISINA = 900, 500
PROZOR = pygame.display.set_mode((SIRINA, VISINA))

def main():

    game_running = True
    while game_running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
    pygame.quit()