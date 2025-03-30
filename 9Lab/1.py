import pygame
import random
import sys

pygame.init()


WIDTH = 400
HEIGHT = 600
FPS = 60

#цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

#окна
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

#изображений
car_image = pygame.image.load("8Lab/image/player.png")  
enemy_image = pygame.image.load("8Lab/image/enemy.png") 
coin_image = pygame.image.load("8Lab/image/coin.jpg")  


font = pygame.font.SysFont("Verdana", 20)

#класс игрока
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

#класс врага
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

#вес цены
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.reset_pos()

    def reset_pos(self):
        self.rect.center = (random.randint(30, WIDTH - 30), random.randint(-500, -50))
        self.speed = 5
        self.value = random.choice([1, 2, 5])  #могут стоить 1, 2 или 5

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.reset_pos()

#объекты
player = Player()
enemy = Enemy()
coins = [Coin() for _ in range(3)]

#спрайты
enemies = pygame.sprite.Group()
enemies.add(enemy)

coins_group = pygame.sprite.Group()
for c in coins:
    coins_group.add(c)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(*coins)

#переменные 
coin_count = 0
speed_increase_step = 10  #каждые 10 монет враг ускоряется
clock = pygame.time.Clock()

#цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill(WHITE)

    #движение объектов
    player.move()
    enemy.move()
    for coin in coins:
        coin.move()

    #столкновения с врагом 
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.quit()
        sys.exit()

    #обновление счета
    for coin in coins:
        if pygame.sprite.collide_rect(player, coin):
            coin_count += coin.value
            coin.reset_pos()

            # Увеличиваем скорость врага каждые speed_increase_step монет
            enemy.speed = 5 + (coin_count // speed_increase_step)

    # Отрисовка всех объектов
    for entity in all_sprites:
        win.blit(entity.image, entity.rect)

    # Отображение счета
    score_text = font.render(f"Coins: {coin_count}", True, YELLOW)
    win.blit(score_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(FPS)
