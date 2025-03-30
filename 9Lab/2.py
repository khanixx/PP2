import pygame
import random
import sys
import time

pygame.init()

#размер ячейки и сетки
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with Levels")

#цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


font = pygame.font.SysFont('Arial', 20)

#змейка и направление
snake = [(5, 5)]
direction = (1, 0)


#ключ цвет, очки, длина
FOOD_TYPES = {
    RED: (1, 1, 8),
    YELLOW: (2, 2, 6),
    BLUE: (3, 3, 4)
}

#генерация новой еды с таймером
def spawn_food():
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            color = random.choice(list(FOOD_TYPES.keys()))
            score_value, grow_length, ttl = FOOD_TYPES[color]
            return {
                'pos': pos,
                'color': color,
                'score': score_value,
                'grow': grow_length,
                'spawn_time': time.time(),
                'ttl': ttl
            }

#первая еда
food = spawn_food()

#счёт уровень скорость
score = 0
level = 1
speed = 10

#таймер
clock = pygame.time.Clock()

#цикл игры
while True:
    win.fill(BLACK)

    #событий выхода
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #нажатия клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)
    elif keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1)
    elif keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)

    #позиция головы
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    #столкновений
    if (
        new_head in snake or
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
    ):
        print("Game Over")
        pygame.quit()
        sys.exit()

    #добавление новой головы
    snake.insert(0, new_head)

    #поедание еды
    if new_head == food['pos']:
        score += food['score']
        for _ in range(food['grow'] - 1):
            snake.insert(0, snake[0])  #удлиняем змею дополнительно
        #повышение уровня каждые 4 очка
        if score % 4 == 0:
            level += 1
            speed += 2
        food = spawn_food()  #спавн новой еды
    else:
        snake.pop()  #убираем хвост если еду не съели

    #таймер еды
    if time.time() - food['spawn_time'] > food['ttl']:
        food = spawn_food()

    #еда
    pygame.draw.rect(win, food['color'], (
        food['pos'][0] * CELL_SIZE,
        food['pos'][1] * CELL_SIZE,
        CELL_SIZE, CELL_SIZE
    ))

    # Отрисовка змейки
    for idx, segment in enumerate(snake):
        color = GREEN if idx == 0 else DARK_GREEN
        pygame.draw.rect(win, color, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    #счёт
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    win.blit(score_text, (10, 10))

    #обновление экрана
    pygame.display.update()
    clock.tick(speed)
