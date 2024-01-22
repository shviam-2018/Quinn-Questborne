import pygame
from pygame.locals import *
from pygame.sprite import Group

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_Width = 1000
screen_Height = 1000

screen = pygame.display.set_mode((screen_Width, screen_Height))
pygame.display.set_caption("Quinn Questborne")

#load image
sun_img = pygame.image.load("res/sun.png")
bg_img = pygame.image.load("res/sky.png")
restart_img = pygame.image.load("res/restart_btn.png")
start_img = pygame.image.load("res/start_btn.png")
exit_img = pygame.image.load("res/exit_btn.png")

#def game var
tile_size = 50
game_over = 0
main_menu = True

class Buttom():
        def __init__(self, x,y, image):
                self.image = image
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.clickied = False
                
        def draw(self):
                action = False
                
                #get mouse postion
                pos = pygame.mouse.get_pos()
                
                #check mousecover and clickied condiction
                if self.rect.collidepoint(pos):
                        if pygame.mouse.get_pressed()[0] == 1 and self.clickied == False:
                                action = True
                                self.clickied = True
                if pygame.mouse.get_pressed()[0] == 0:
                        self.clickied = False
                
                #draw buttom
                screen.blit(self.image, self.rect)
                
                return action

class player():
        def __init__(self, x, y):
                self.reset(x, y)
                
        def update (self, game_over):
                dx = 0
                dy = 0
                walk_cooldown = 4
                
                if game_over == 0:
                #movment
                        key = pygame.key.get_pressed()
                        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                                self.vel_y = -15
                                self.jumped = True
                        if key[pygame.K_SPACE] == False:
                                self.jumped = False
                        if key[pygame.K_a]:
                                dx -= 5
                                self.counter += 1
                                self.direction = -1
                        if key[pygame.K_d]:
                                dx += 5
                                self.counter += 1
                                self.direction = 1
                        if key[pygame.K_a] == False and key[pygame.K_d] == False:
                                self.counter = 0
                                self.index = 0
                                if self.direction == 1:
                                        self.image = self.images_right[self.index]
                                if self.direction == -1:
                                        self.image = self.images_left[self.index]
                        
                        #animation handler
                        if self.counter > walk_cooldown:
                                self.counter = 0
                                self.index += 1
                                if self.index >= len(self.images_right):
                                        self.index = 0
                                if self.direction == 1:
                                        self.image = self.images_right[self.index]
                                if self.direction == -1:
                                        self.image = self.images_left[self.index]
                        
                        #gravity
                        self.vel_y += 1
                        if self.vel_y > 10:
                                self.vel_y = 10        
                        dy += self.vel_y
                                
                        #collision
                        self.in_air = True
                        for tile in world.tile_list:
                                #check for colliction in x direction
                                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                        dx = 0
                                
                                #checking for colliction in y
                                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        #check if below the ground i.e jumping
                                        if self.vel_y < 0:
                                                dy = tile[1].bottom - self.rect.top
                                                self.vel_y = 0
                                        #check if above the ground i.e falling
                                        elif self.vel_y >= 0:
                                                dy = tile[1].top - self.rect.bottom
                                                self.vel_y = 0
                                                self.in_air = False
                                        
                        #check for colliction with enemys
                        if pygame.sprite.spritecollide(self, blob_group, False):
                                game_over = -1
                                
                        #check for colliction with lava
                        if pygame.sprite.spritecollide(self, lava_group, False):
                                game_over = -1
                                print(game_over)
                        
                        #update player locatio
                        self.rect.x += dx
                        self.rect.y += dy
                        
                elif game_over == -1:
                        self.image = self.dead_image
                        if self.rect.y > 200:
                                self.rect.y -= 5
                        
                #display player
                screen.blit(self.image, self.rect)
                pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

                return game_over
        
        def reset(self, x, y):
                self.images_right = []
                self.images_left = []
                self.index = 0
                self.counter = 0
                for num in range(1, 5):
                        img_right = pygame.image.load(f"res/guy{num}.png")
                        img_right = pygame.transform.scale(img_right, (40, 80))
                        img_left = pygame.transform.flip(img_right, True, False)
                        self.images_right.append(img_right)
                        self.images_left.append(img_left)
                self.dead_image = pygame.image.load("res/ghost.png")
                self.image = self.images_right[self.index]        
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                self.vel_y = 0
                self.jumped = False
                self.direction = 0
                self.in_air = True

class World():
        def __init__(self, data):
                self.tile_list = []
                
                #load image
                dirt_img = pygame.image.load("res/dirt.png")
                grass_img = pygame.image.load("res/grass.png")
                
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
                                if tile == 2:
                                        img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)
                                if tile == 3:
                                        blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                                        blob_group.add(blob)
                                if tile == 6:
                                        lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                                        lava_group.add(lava)
                                col_count +=1
                        row_count += 1       

        def draw(self):
                for tile in self.tile_list:
                        screen.blit(tile[0], tile[1])
                        pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

#Enemy class
class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("res/blob.png")
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.move_direction = 1
                self.move_counter = 0
                
        def update(self):
                self.rect.x += self.move_direction
                self.move_counter += 1
                if abs(self.move_counter) > 50:
                        self.move_direction *= -1
                        self.move_counter *= -1
#Lava class
class Lava(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                img = pygame.image.load("res/lava.png")
                self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

Player = player(100, screen_Height - 130)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

world = World(world_data)

#buttom
restart_button = Buttom(screen_Width // 2 - 50, screen_Height // 2 + 100, restart_img)
start_button = Buttom(screen_Width // 2 - 350, screen_Height // 2, start_img)
exit_button = Buttom(screen_Width // 2 + 150, screen_Height // 2, exit_img)


run = True
while run: 
        
        clock.tick(fps)
        
        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))
        
        if main_menu == True:
                if exit_button.draw():
                        run = False
                if start_button.draw():
                        main_menu = False
        else:
                world.draw()
                
                if game_over == 0:
                        blob_group.update()
                        
                blob_group.draw(screen)
                lava_group.draw(screen)
                
                game_over = Player.update(game_over)
                
                #when player is dead
                if game_over == -1:
                        if restart_button.draw():
                                Player.reset(100, screen_Height - 130)
                                game_over = 0
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                        
        pygame.display.update()
pygame.quit()