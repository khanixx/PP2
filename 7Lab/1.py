import pygame
import datetime
pygame.init()
w = 600
h = 400
angle1 = 0
angle2 = 0

sc = pygame.display.set_mode((w, h), pygame.RESIZABLE)
pygame.display.set_caption("simple clock")

white = (255, 255, 255)
sc.fill(white)

mickey_surf = pygame.image.load("7Lab/image/mickeyclock.jpg")
left_hand_surf = pygame.image.load("7Lab/image/left_hand.png").convert_alpha()
right_hand_surf = pygame.image.load("7Lab/image/right_hand.png").convert_alpha()

mickey_surf = pygame.transform.scale(mickey_surf, (mickey_surf.get_width() // 2.7, mickey_surf.get_height() // 2.7))
clock = pygame.time.Clock()
x = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    t = datetime.datetime.now()
    angle1 = -t.second * 6
    angle2 = -t.minute * 6

    left_hand_surf1 = pygame.transform.rotate(left_hand_surf, x)
    right_hand_surf1 = pygame.transform.rotate(right_hand_surf, angle2)

    right_hand_surf1 = pygame.transform.scale(right_hand_surf1, (right_hand_surf1.get_width() // 1.2, right_hand_surf1.get_height() // 1.5))
    left_hand_surf1 = pygame.transform.scale(left_hand_surf1, (left_hand_surf1.get_width() // 1.2, left_hand_surf1.get_height() // 1.5))

    sc.fill(white)
    mickeyrect = mickey_surf.get_rect(center=(w // 2, h // 2))
    left_hand_rect = left_hand_surf1.get_rect(center=(w // 2, h // 2))
    right_hand_rect = right_hand_surf1.get_rect(center=(w // 2, h // 2))

    sc.blit(mickey_surf, mickeyrect)
    sc.blit(left_hand_surf1, left_hand_rect)
    sc.blit(right_hand_surf1, right_hand_rect)

    x -= 1
    pygame.display.update()
    clock.tick(60)