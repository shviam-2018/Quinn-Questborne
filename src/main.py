import pygame
from pygame.locals import *

pygame.init()

screen_Width = 1110
screen_Height = 600

screen = pygame.display.set_mode((screen_Width, screen_Height))
pygame.display.set_caption("Quinn Questborne")

#load image
sun_img = pygame.image.load("res/sun.png")
bg_img = pygame.image.load("res/sky.png")

tile_size = 160

class World():
        def __init__(self, data):
                self.tile_list = []
                
                #load image
                dirt_img = pygame.image.load("res/dirt.png")
                
                row_count = 0
                for row in data:
                        col_count = 0
                        for tile in row:
                                if tile == 1:
                                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)
                                col_count +=1
                        row_count += 1       

        def draw(self):
                for tile in self.tile_list:
                        screen.blit(tile[0], tile[1])

world_data = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

world = World(world_data)

run = True
while run: 
        
        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))
        
        world.draw()
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                        
        pygame.display.update()
pygame.quit()