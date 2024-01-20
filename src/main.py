import pygame
from pygame.locals import *

pygame.init()

screen_Width = 800
screen_Height = 600

screen = pygame.display.set_mode((screen_Width, screen_Height))
pygame.display.set_caption("Quinn Questborne")

#load image

run = True
while run: 
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                        
        pygame.display.update()
pygame.quit()