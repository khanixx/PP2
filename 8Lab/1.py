import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")


car_image = pygame.image.load("8Lab/image/player.png")  
enemy_image = pygame.image.load("8Lab/image/enemy.png") 
coin_image = pygame.image.load("8Lab/image/coin.jpg")  


font = pygame.font.SysFont("Verdana", 20)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), -100)
        self.speed = 5

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), -100)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.reset_pos()

    def reset_pos(self):
        self.rect.center = (random.randint(30, WIDTH - 30), random.randint(-500, -50))
        self.speed = 5

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.reset_pos()


player = Player()
enemy = Enemy()
coins = [Coin() for _ in range(3)]

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins_group = pygame.sprite.Group()
for c in coins:
    coins_group.add(c)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(*coins)


coin_count = 0
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill(WHITE)

 
    player.move()
    enemy.move()
    for coin in coins:
        coin.move()

 
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.quit()
        sys.exit()


    for coin in coins:
        if pygame.sprite.collide_rect(player, coin):
            coin_count += 1
            coin.reset_pos()


    for entity in all_sprites:
        win.blit(entity.image, entity.rect)


    score_text = font.render(f"Coins: {coin_count}", True, YELLOW)
    win.blit(score_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(FPS)
