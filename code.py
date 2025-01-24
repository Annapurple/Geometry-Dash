import os
import pygame
import sys

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
SIZE = WIDTH, HEIGHT = (1000, 600)
FPS = 60
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Overcome_Obstacles")


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    intro_text = ['', '',
                  " Цель - Преодалеть все препядствия и дойти до конца уровня, не столкнувшись с ними.",
                  " Чтобы персонаж перепрыгивал препядствие достаточно нажать любую кнопку или клавишу."]
    fon = pygame.transform.scale(load_image('startfon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    title_font = pygame.font.Font(None, 60)
    title_text = title_font.render("Overcome_Obstacles", True, WHITE)
    title_rect = title_text.get_rect(center=(500, 50))
    screen.blit(title_text, title_rect)
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, WHITE)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    button_start = pygame.Rect(400, 500, 200, 50)
    pygame.draw.rect(screen, WHITE, button_start)
    button_text = font.render("START", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_start.center)
    screen.blit(button_text, button_text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and button_start.collidepoint(mouse_pos):
                    return
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
player = None
clock = pygame.time.Clock()
start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            player.move(event.key)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)