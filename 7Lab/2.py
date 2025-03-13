import pygame
import os

pygame.init()
pygame.mixer.init()

foldermusic = "7Lab/music"
playlist = [f for f in os.listdir(foldermusic) if f.endswith(".mp3")]

screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Music Player")

track = 0

def play_music(track):
    pygame.mixer.music.load(os.path.join(foldermusic, playlist[track]))
    pygame.mixer.music.play()

next_button_img = pygame.image.load('7Lab/image/next.png')
prev_button_img = pygame.image.load('7Lab/image/prev.png')
pause_button_img = pygame.image.load('7Lab/image/pause.png')
play_button_img = pygame.image.load('7Lab/image/pause1.png')

next_button_img = pygame.transform.scale(next_button_img, (50, 50))
prev_button_img = pygame.transform.scale(prev_button_img, (50, 50))
pause_button_img = pygame.transform.scale(pause_button_img, (50, 50))
play_button_img = pygame.transform.scale(play_button_img, (50, 50))

next_button_rect = next_button_img.get_rect(center=(250, 150))
prev_button_rect = prev_button_img.get_rect(center=(50, 150))
pause_button_rect = pause_button_img.get_rect(center=(150, 150))

play_music(track)

runi = True
paused = False

while runi:
    screen.fill((0, 0, 0))

    if paused:
        screen.blit(play_button_img, pause_button_rect)
    else:
        screen.blit(pause_button_img, pause_button_rect)

    screen.blit(next_button_img, next_button_rect)
    screen.blit(prev_button_img, prev_button_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runi = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    paused = True
                else:
                    pygame.mixer.music.unpause()
                    paused = False

            elif event.key == pygame.K_RIGHT:
                track = (track + 1) % len(playlist)
                play_music(track)
            elif event.key == pygame.K_LEFT:
                track = (track - 1) % len(playlist)
                play_music(track)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_button_rect.collidepoint(event.pos):
                track = (track + 1) % len(playlist)
                play_music(track)
            elif prev_button_rect.collidepoint(event.pos):
                track = (track - 1) % len(playlist)
                play_music(track)
            elif pause_button_rect.collidepoint(event.pos):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    paused = True
                else:
                    pygame.mixer.music.unpause()
                    paused = False

    pygame.display.flip()

pygame.quit()