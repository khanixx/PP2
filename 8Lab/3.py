import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255)]
current_color = BLACK
tool = 'brush'
radius = 5
drawing = False
start_pos = None

def draw_ui():
    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, 40))
    for i, col in enumerate(colors):
        pygame.draw.rect(win, col, (10 + i*50, 5, 40, 30))
    pygame.draw.rect(win, (200, 200, 200), (WIDTH - 200, 5, 60, 30))
    pygame.draw.rect(win, (200, 200, 200), (WIDTH - 130, 5, 60, 30))
    pygame.draw.rect(win, (200, 200, 200), (WIDTH - 60, 5, 50, 30))
    font = pygame.font.SysFont("Arial", 16)
    win.blit(font.render("Rect", True, BLACK), (WIDTH - 185, 10))
    win.blit(font.render("Circle", True, BLACK), (WIDTH - 115, 10))
    win.blit(font.render("Eraser", True, BLACK), (WIDTH - 50, 10))

canvas = pygame.Surface((WIDTH, HEIGHT - 40))
canvas.fill(WHITE)
clock = pygame.time.Clock()

while True:
    win.fill(WHITE)
    win.blit(canvas, (0, 40))
    draw_ui()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my < 40:
                if 5 <= mx <= 5 + 4 * 50:
                    current_color = colors[(mx - 10) // 50]
                    tool = 'brush'
                elif WIDTH - 200 <= mx <= WIDTH - 140:
                    tool = 'rect'
                elif WIDTH - 130 <= mx <= WIDTH - 70:
                    tool = 'circle'
                elif WIDTH - 60 <= mx <= WIDTH:
                    tool = 'eraser'
            else:
                drawing = True
                start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                if tool == 'rect':
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif tool == 'circle':
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
            drawing = False
        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == 'brush':
                pygame.draw.circle(canvas, current_color, event.pos, radius)
            elif tool == 'eraser':
                pygame.draw.circle(canvas, WHITE, event.pos, radius)

    pygame.display.update()
    clock.tick(120)
