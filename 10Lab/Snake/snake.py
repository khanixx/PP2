import pygame
import random
import sys
from utils import create_user, get_user, get_last_score, save_score

username = input("Enter your username: ").strip()[:50]
create_user(username)

user_id = get_user(username)
last = get_last_score(username)

if last:
    print(f"Welcome back, {username}! Your last score: {last[0]}, level: {last[1]}")
    score, level = last
    speed = 10 + level * 2
else:
    print(f"Hello, {username}! Starting fresh.")
    score = 0
    level = 1
    speed = 10

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

walls_by_level = {
    1: [],
    2: [(10, y) for y in range(5, 15)],
    3: [(x, 10) for x in range(5, 25)],
    4: [(x, x % GRID_HEIGHT) for x in range(5, 25)],
    5: [(x, 5) for x in range(5, 25)] + [(x, 14) for x in range(5, 25)]
}

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with Levels")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 20)

snake = [(5, 5)]
direction = (1, 0)

def spawn_food():
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake and pos not in walls_by_level.get(level, []):
            return pos

food = spawn_food()
clock = pygame.time.Clock()


while True:
    win.fill(BLACK)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)
    elif keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1)
    elif keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)
    elif keys[pygame.K_p]:
        print("Game paused. Saving progress...")
        save_score(username, score, level)
        pygame.time.delay(1000)
        continue


    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    walls = walls_by_level.get(level, [])

    if (
        new_head in snake or
        new_head in walls or
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
    ):
        print("Game Over")
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = spawn_food()
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    pygame.draw.rect(win, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))


    for idx, segment in enumerate(snake):
        color = GREEN if idx == 0 else DARK_GREEN
        pygame.draw.rect(win, color, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))


    for wall in walls:
        pygame.draw.rect(win, WHITE, (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))


    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    win.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(speed)
