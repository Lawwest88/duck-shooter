from operator import truediv
import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT =850, 850 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Shooter")

#loading images 
BLUE_JOEL_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_joel_small.png"))

#player 
DUCK_SPACE_player = pygame.image.load(os.path.join("assets","pixel_ship_duck.png"))

#lasers
JOEL_LASER = pygame.image.load(os.path.join("assets","pixel_laser_joel.png"))
DUCK_LASER = pygame.image.load(os.path.join("assets","pixel_laser_duck.png"))

#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.player_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = DUCK_SPACE_player
        self.laser_img = DUCK_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    def __init__(self, x, y, blue, health=100):
        super().__init__(x, y, health)
        self.ship_img = BLUE_JOEL_SPACE_SHIP
        self.laser_img = JOEL_LASER
        self.ship_img, self.laser_img 
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_lenght = 5
    enemy_val = 1

    player_val = 5

    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost Ducker!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))


        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["joel"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_val > 0: #left
            player.x -= player_val
        if keys[pygame.K_d] and player.x + player_val + 50 < WIDTH: #right
            player.x += player_val
        
        for enemy in enemies[:]:
            enemy.move(enemy_val)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()
        
main()
