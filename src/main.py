import pygame
from pygame.locals import *
from pygame.sprite import Group
import pickle
import os

#initizing pygame
pygame.init()

#added fps cap to controlle the cpu uesage
clock = pygame.time.Clock()
fps = 90

#screen dimintion
screen_Width = 1000
screen_Height = 1000

screen = pygame.display.set_mode((screen_Width, screen_Height))
pygame.display.set_caption("Quinn Questborne")

font_score = pygame.font.SysFont(None , 50)

#load image
sun_img = pygame.image.load("res/sun.png")
bg_img = pygame.image.load("res/sky.png")
restart_img = pygame.image.load("res/restart_btn.png")
start_img = pygame.image.load("res/start_btn.png")
exit_img = pygame.image.load("res/exit_btn.png")

def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

#def game var

#game object size
tile_size = 50

#game over var
game_over = 0

#start meanu var
main_menu = True

#max level
max_level = 2

#score
score = 0

#color
white = (255, 255, 255)

#fuction to reset level
def reset_level(current_level):
        Player.reset( 100, screen_Height - 130)
        blob_group.empty()
        lava_group.empty()
        exit_group.empty()
        if os.path.exists(f"level{current_level}_data"):
                pickle_in = open(f"level{current_level}_data", "rb")
                world_data = pickle.load(pickle_in)
        world = World(world_data)
        return world

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

#player class responsible for player movment and colliction
class player():
        def __init__(self, x, y):
                self.reset(x, y)
                
        def update (self, game_over):
                dx = 0
                dy = 0
                walk_cooldown = 2
                
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
                                        
                        #check for colliction with objects
                        if pygame.sprite.spritecollide(self, blob_group, False):
                                game_over = "Death by slime"
                                print(game_over)
                                
                        #check for colliction with lava
                        if pygame.sprite.spritecollide(self, lava_group, False):
                                game_over = "bured in lava"
                                print(game_over)
                        
                        #check for colliction with exit
                        if pygame.sprite.spritecollide(self, exit_group, False):
                                game_over = "you win"
                                print(game_over)
                                
                        #update player locatio
                        self.rect.x += dx
                        self.rect.y += dy
                        
                elif game_over == "Death by slime" or game_over == "bured in lava":
                        self.image = self.dead_image
                        if self.rect.y > 200:
                                self.rect.y -= 5
                        
                #display player
                screen.blit(self.image, self.rect)
                pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

                return game_over
        
        #the reset method is used to reset the player location and image
        def reset(self, x, y):
                self.images_right = []
                self.images_left = []
                self.index = 0
                self.counter = 0
                
#this creats the aniumation for the player movment by loading the 5 images of the player in order and quick so 
#it looks like the player is moving
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
                                if tile == 7:
                                        coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                                        coin_group.add(coin)
                                if tile == 8:
                                        exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                                        exit_group.add(exit)
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
                
#point class
class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                img = pygame.image.load("res/coin.png")
                self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
                self.rect = self.image.get_rect()
                self.rect.center = (x, y)
#exit class
class Exit(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                img = pygame.image.load("res/exit.png")
                self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

Player = player(100, screen_Height - 130)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#load in level data
current_level = 1
if os.path.exists(f"level{current_level}_data"):
        pickle_in = open(f"level{current_level}_data", "rb")
        world_data = pickle.load(pickle_in)
world = World(world_data)

#buttom for start and exit
restart_button = Buttom(screen_Width // 2 - 50, screen_Height // 2 + 100, restart_img)
start_button = Buttom(screen_Width // 2 - 350, screen_Height // 2, start_img)
exit_button = Buttom(screen_Width // 2 + 150, screen_Height // 2, exit_img)

#the game loop this component is responsible for the game to load, run and loop
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
                
                if game_over == "Death by slime" or game_over == "bured in lava":
                        blob_group.update()
                        #update score
                        #check if coin collected
                        if pygame.sprite.spritecollide(Player, coin_group, True):
                                score +=1
                        draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
                blob_group.draw(screen)
                lava_group.draw(screen)
                coin_group.draw(screen)
                exit_group.draw(screen)
                
                game_over = Player.update(game_over)
                
                #when player is dead
                if game_over == "Death by slime" or game_over == "bured in lava":
                        if restart_button.draw():
                                world_data = []
                                world = reset_level(current_level)
                                game_over = 0
                                score = 0

                #if player wins
                if game_over == "you win":
                        current_level +=1
                        if current_level <= max_level:
                                #reset game to next level
                                world_data = []
                                world = reset_level(current_level)
                                game_over = 0
                                score = 0
                        else:
                                if restart_button.draw():
                                        current_level = 1
                                        world_data = []
                                        world = reset_level(current_level)
                                        game_over = 0
                                        score = 0
                
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                        
        pygame.display.update()
pygame.quit()