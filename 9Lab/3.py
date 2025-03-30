import pygame
import sys
import math


pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

#цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255)]
current_color = BLACK
tool = 'brush'
radius = 5
drawing = False
start_pos = None

#панели
def draw_ui():
    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, 40))
    for i, col in enumerate(colors):
        pygame.draw.rect(win, col, (10 + i*50, 5, 40, 30))

    tools = ["Rect", "Circle", "Eraser", "Square", "R. Tri", "E. Tri", "Rhomb"]
    for i, name in enumerate(tools):
        pygame.draw.rect(win, (200, 200, 200), (WIDTH - (70 * (len(tools) - i)), 5, 60, 30))
        font = pygame.font.SysFont("Arial", 14)
        win.blit(font.render(name, True, BLACK), (WIDTH - (70 * (len(tools) - i)) + 5, 10))

#поверхность для рисования
canvas = pygame.Surface((WIDTH, HEIGHT - 40))
canvas.fill(WHITE)
clock = pygame.time.Clock()

#цикл
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
                else:
                    index = (WIDTH - mx) // 70
                    tools_map = ['rect', 'circle', 'eraser', 'square', 'rtriangle', 'etriangle', 'rhombus']
                    if 0 <= index < len(tools_map):
                        tool = tools_map[len(tools_map) - 1 - index]
            else:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos
                if tool == 'rect':
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif tool == 'circle':
                    radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                elif tool == 'square':
                    side = max(abs(x2 - x1), abs(y2 - y1))
                    rect = pygame.Rect(x1, y1, side if x2 > x1 else -side, side if y2 > y1 else -side)
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif tool == 'rtriangle':
                    pygame.draw.polygon(canvas, current_color, [start_pos, (x1, y2), (x2, y2)], 2)
                elif tool == 'etriangle':
                    height = abs(y2 - y1)
                    pygame.draw.polygon(canvas, current_color, [((x1+x2)//2, y1), (x1, y2), (x2, y2)], 2)
                elif tool == 'rhombus':
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    dx, dy = abs(x2 - x1) // 2, abs(y2 - y1) // 2
                    points = [(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy)]
                    pygame.draw.polygon(canvas, current_color, points, 2)
            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == 'brush':
                pygame.draw.circle(canvas, current_color, event.pos, radius)
            elif tool == 'eraser':
                pygame.draw.circle(canvas, WHITE, event.pos, radius)

    pygame.display.update()
    clock.tick(120)