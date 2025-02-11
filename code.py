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
levels = ["data/level1.txt", "data/level2.txt", "data/level3.txt"]


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


def load_obsticles(name, size=(120, 100)):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return pygame.transform.scale(image, size)


def create_obstacles(filename="level1.txt"):
    obstacles = pygame.sprite.Group()
    with open(filename, 'r') as f:
        line = f.readline().strip()
        x = WIDTH
        tree_img = load_obsticles("tree.png")
        bush_img = load_obsticles("bush.png")
        stone_img = load_obsticles("stone.png")
        for obstacle_type in line:
            if obstacle_type == '/':
                obstacles.add(Tree(x, 0, tree_img))
            elif obstacle_type == '#':
                obstacles.add(Bush(x, 0, bush_img))
            elif obstacle_type == '.':
                obstacles.add(Stone(x, 0, stone_img))
            x += 100
    return obstacles


class Checkbox:

    def __init__(self, x, y, text, value):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.text = text
        self.value = value
        self.checked = False

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(left=self.rect.right + 10, centery=self.rect.centery)
        screen.blit(text_surface, text_rect)
        if self.checked:
            pygame.draw.circle(screen, WHITE, self.rect.center, 8)


def handle_checkboxes(event, checkboxes):
    for box in checkboxes:
        if box.rect.collidepoint(event.pos):
            if not box.checked:
                for other_box in checkboxes:
                    other_box.checked = False
                box.checked = True


def start_screen():
    global user, button_start, click, images, index
    button1_color = (250, 250, 250)
    button1_new_color = (150, 150, 255)
    button2_color = (250, 250, 250)
    button2_new_color = (150, 150, 255)
    button3_color = (250, 250, 250)
    button3_new_color = (150, 150, 255)
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
    text1 = font.render("Цель - Преодалеть все препятствия и дойти до конца уровня, не столкнувшись с ними.", True,
                        WHITE)
    text_rect1 = text1.get_rect(center=(500, 105))
    screen.blit(text1, text_rect1)
    text2 = font.render("Чтобы персонаж перепрыгивал препядствие достаточно нажать любую кнопку или клавишу.", True,
                        WHITE)
    text_rect2 = text2.get_rect(center=(500, 155))
    screen.blit(text2, text_rect1)
    index = 0
    click = False
    while True:
        screen.fill(BLACK)
        screen.blit(fon, (0, 0))
        screen.blit(title_text, title_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_checkboxes(event, checkboxes)
                if button_start.collidepoint(event.pos):
                    click = True
                    return index
                elif button_left.collidepoint(event.pos):
                    index = (index - 1) % len(images)
                elif button_right.collidepoint(event.pos):
                    index = (index + 1) % len(images)
        mouse_pos = pygame.mouse.get_pos()
        button1_current_color = button1_new_color if button_start.collidepoint(mouse_pos) else button1_color
        button2_current_color = button2_new_color if button_left.collidepoint(mouse_pos) else button2_color
        button3_current_color = button3_new_color if button_right.collidepoint(mouse_pos) else button3_color
        if index == 0:
            user = "character1.png"
        if index == 1:
            user = "character2.png"
        if index == 2:
            user = "character3.png"
        for box in checkboxes:
            box.draw()
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(images[index], image_pos)
        pygame.draw.rect(screen, button2_current_color, button_left)
        pygame.draw.rect(screen, button3_current_color, button_right)
        pygame.draw.rect(screen, button1_current_color, button_start)
        screen.blit(left_text, button_left_text)
        screen.blit(right_text, button_right_text)
        screen.blit(start_text, button_start_text)
        pygame.display.flip()
        clock.tick(FPS)


def number_level():
    if click:
        for box in checkboxes:
            if box.checked:
                return box.value


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        if self.image:
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 500
            self.speed = 4
            self.mask = pygame.mask.from_surface(self.image)
            self.counted = False
        else:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load_image(user), (200, 200))
        self.rect = self.image.get_rect(center=(500, 500))
        self.mask = pygame.mask.from_surface(self.image)
        self.jumping = 0.5
        self.jump_power = -20
        self.flag = False

    def update(self):
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


class Tree(Obstacle):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Stone(Obstacle):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Bush(Obstacle):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


def final_screen(score):
    star_sprites = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image('startfon.jpg'), (WIDTH, HEIGHT))
    font = pygame.font.Font(None, 74)
    text = font.render(f"Overcome_Obstacles", True, WHITE)
    score_text = font.render(f"Score: {score} / 20", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 50))
    score_rect = score_text.get_rect(center=(WIDTH // 2, 200))
    good_text = font.render(f"Молодец! Ты прошёл уровень!", True, WHITE)
    good_text_rect = good_text.get_rect(center=(WIDTH // 2, 120))
    bad_text = font.render(f"Попробуй ещё раз! У тебя получится!", True, WHITE)
    bad_text_rect = good_text.get_rect(center=(WIDTH // 2 - 70, 120))
    while True:
        screen.fill(BLACK)
        screen.blit(fon, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(images[index], (400, 250))
        if score == 20:
            screen.blit(good_text, good_text_rect)
        else:
            screen.blit(bad_text, bad_text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()


font = pygame.font.Font(None, 36)
checkboxes = [
    Checkbox(800, 250, "level 1", 1),
    Checkbox(800, 300, "level 2", 2),
    Checkbox(800, 350, "level 3", 3)
]
checkboxes[0].checked = True
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
start_screen()
obstacles = create_obstacles(levels[number_level() - 1])
all_sprites.add(*obstacles)
player = Player(0, HEIGHT // 50)
all_sprites.add(player)
score = 0
background = pygame.transform.scale(load_image('main_fon.jpg'), (WIDTH, HEIGHT))
while True:
    font_play = pygame.font.Font(None, 74)
    text_play = font.render(f"Overcome_Obstacles", True, WHITE)
    text_play_rect = text_play.get_rect(center=(WIDTH // 2, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            player.jump()
    all_sprites.update()
    if any((pygame.sprite.collide_mask(player, i) for i in obstacles)) or score == 20:
        final_screen(score)
    for obstacle in obstacles:
        if obstacle.rect.right < player.rect.left and not obstacle.counted:
            score += 1
            obstacle.counted = True
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    screen.blit(text_play, text_play_rect)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
