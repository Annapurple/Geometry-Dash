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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    player_x, player_y = None, None
    for x in range(len(level)):
        if level[x] == '/':
            Tree('tree', x)
        elif level[x] == '.':
            Stone('stone', x)
        elif level[x] == '#':
            Stone('bush', x)
        elif level[x] == '*':
            Stone('box', x)
    new_player = Player(player_x, player_y)
    return new_player, x, y


def start_screen():
    global index, images, user
    user = ''
    image_paths = ["character1.png", "character2.png", "character3.png"]
    images = [pygame.transform.scale(load_image(path), (250, 250)) for path in image_paths]
    image_pos = (360, 180)
    font = pygame.font.Font(None, 30)
    button_left = pygame.Rect(200, 310, 100, 50)
    button_right = pygame.Rect(650, 310, 100, 50)
    button_start = pygame.Rect(380, 510, 200, 50)
    fon = pygame.transform.scale(load_image('startfon.jpg'), (WIDTH, HEIGHT))
    title_font = pygame.font.Font(None, 60)
    title_text = title_font.render("Overcome_Obstacles", True, WHITE)
    title_rect = title_text.get_rect(center=(500, 50))
    left_text = font.render("<-", True, BLACK)
    right_text = font.render("->", True, BLACK)
    start_text = font.render("START", True, BLACK)
    button_start_text = start_text.get_rect(center=button_start.center)
    button_left_text = left_text.get_rect(center=button_left.center)
    button_right_text = right_text.get_rect(center=button_right.center)
    text1 = font.render("Цель - Преодалеть все препятствия и дойти до конца уровня, не столкнувшись с ними.", True, WHITE)
    text_rect1 = text1.get_rect(center=(500, 105))
    screen.blit(text1, text_rect1)
    text2 = font.render("Чтобы персонаж перепрыгивал препядствие достаточно нажать любую кнопку или клавишу.", True, WHITE)
    text_rect2 = text2.get_rect(center=(500, 155))
    screen.blit(text2, text_rect1)
    index = 0
    while True:
        screen.fill(BLACK)
        screen.blit(fon, (0, 0))
        screen.blit(title_text, title_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    return index
                elif button_left.collidepoint(event.pos):
                    index = (index - 1) % len(images)
                elif button_right.collidepoint(event.pos):
                    index = (index + 1) % len(images)
        if index == 0:
            user = "character1.png"
        if index == 1:
            user = "character2.png"
        if index == 2:
            user = "character3.png"
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(images[index], image_pos)
        pygame.draw.rect(screen, WHITE, button_left)
        pygame.draw.rect(screen, WHITE, button_right)
        pygame.draw.rect(screen, WHITE, button_start)
        screen.blit(left_text, button_left_text)
        screen.blit(right_text, button_right_text)
        screen.blit(start_text, button_start_text)
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(score):
    fon = pygame.transform.scale(load_image('startfon.jpg'), (WIDTH, HEIGHT))
    font = pygame.font.Font(None, 74)
    text = font.render(f"Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    while True:
        screen.fill(BLACK)
        screen.blit(fon, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load_image(user), (200, 200))
        self.rect = self.image.get_rect(center=(100, 500))
        self.speed_x = 5
        self.jumping = 0.5
        self.jump_power = -12
        self.flag = False

    def update(self):
        self.rect.x += self.speed_x
        if self.flag:
            self.speed_y += self.jumping
            self.rect.y += self.speed_y
            if self.rect.y >= HEIGHT - self.rect.height:
                self.rect.y = HEIGHT - self.rect.height
                self.flag = False

    def jump(self):
        if not self.flag:
            self.flag = True
            self.speed_y = self.jump_power


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load_image("tree.png"), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))


class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load_image("stone.png"), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))


class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load_image("bush.png"), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load_image("bush.png"), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))


title_images = {'tree': load_image('tree.png'),
                'stone': load_image('stone.png'),
                'box': load_image('box.png'),
                'bush': load_image('bush.png')}
player_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
bush_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
start_screen()
player = Player(0, 100)
all_sprites.add(player)
background = pygame.transform.scale(load_image('main_fon.jpg'), (WIDTH, HEIGHT))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            player.jump()
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
