from pygame import *

# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас-гравець
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 70:
            self.rect.y += self.speed

    def fire(self):
        # Куля вилітає з центру гравця і летить праворуч
        bullet = Bullet("bullet.png", self.rect.right, self.rect.centery, 10, 20, 10)
        bullets.add(bullet)

# клас-ворог
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# клас стіни
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, x, y, w, h):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас кулі
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed # летить праворуч
        if self.rect.x > win_width:
            self.kill()


#налаштування сцени
win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze online")
background = transform.scale(image.load("black and oranje fon.jpg"), (win_width, win_height))

# спрайти
player = Player('hero.png',5, win_height - 80, 4 ,65,65)
final = GameSprite('treasure.png', win_width - 100, win_height - 100,0,65,65)

game = True
finish = False
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                fire_sound.play()
                player.fire()




        # Відображення
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        final.reset()
        for w in walls:
            w.draw_wall()