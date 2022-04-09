from operator import truediv
import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT =950, 850 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Shooter")

#loading images 
RED_SPACE_player = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_player = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_player = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#player player
DUCK_SPACE_player = pygame.image.load(os.path.join("assets","pixel_ship_duck.png"))

#lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
DUCK_LASER = pygame.image.load(os.path.join("assets","pixel_laser_duck.png"))

#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")), (WIDTH, HEIGHT))

class player:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.player_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))

class Player(player):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.player_img = DUCK_SPACE_player
        self.laser_img = DUCK_LASER
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    player_val = 5

    player = Player(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_val > 0: #left
            player.x -= player_val
        if keys[pygame.K_d] and player.x + player_val + 50 < WIDTH: #right
            player.x += player_val
        
        
main()
