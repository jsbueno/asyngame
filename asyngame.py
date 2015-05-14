import asyncio as tulip
import pygame
import random
from functools import partial

SIZE = 800, 600
CHAR_SIZE=  64, 64

BLUE = 0,0 ,255; RED = 255, 0,0; YELLOW = 255,255,0 ; GREEN=0 ,255,0; WHITE = 255,255,255; MAGENTA = 255,0,255; CYAN = 0,255,255; BLACK=0,0,0; GREY = 128,128,128

class GameOver(BaseException):
    pass

def init():
    global SCREEN, LOOP
    SCREEN = pygame.display.set_mode(SIZE)
    LOOP = tulip.get_event_loop()
    return SCREEN

class Object(pygame.sprite.Sprite):
    def __init__(self, *args, **kw):
        self.x, self.y = (kw.pop("pos", ((kw.pop("x", 0), kw.pop("y", 0)))))
        self.color = kw.pop("color", (255,0,0))
        self.speed = kw.pop("speed", 10)

        self.rect = pygame.Rect((self.x, self.y) + CHAR_SIZE)
        self.image = pygame.Surface(CHAR_SIZE) 
        self.move_function = kw.pop("move_function", lambda *args: None)
        super().__init__()

    def update(self):
        self.image.fill(self.color)
        self.move_function(self)

def move1(self):
    self.rect.x += self.speed
    if self.rect.right > SIZE[0]:
        self.kill()

def move2(self):
    self.rect.y += self.speed
    if self.rect.bottom > SIZE[1]:
        self.kill()
def move3(self):
    self.rect.x -= self.speed
    if self.rect.x < 0:
        self.kill()
def move4(self):
    self.rect.y -= self.speed
    if self.rect.y < 0:
        self.kill()

def clear_callback(surf, rect):
    color = 0, 0, 0
    surf.fill(color, rect)

def create_object():
    pos = random.randrange(0, SIZE[0], CHAR_SIZE[0]), random.randrange(0, SIZE[1], CHAR_SIZE[1])
    direction = random.choice((move1, move2, move3, move4))
    color = random.choice((BLUE, YELLOW, RED, GREEN, WHITE))
    return Object(pos=pos, move_function=direction, color=color)

@tulip.coroutine
def main_loop(main_group):
    while True:
        if random.random()<0.2:
            main_group.add(create_object())
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break
            raise GameOver
        main_group.clear(SCREEN, clear_callback)
        main_group.update()
        main_group.draw(SCREEN)
        pygame.display.flip()
        #pygame.time.delay(30)
        yield from tulip.sleep(0.03)

def main():
    main_group = pygame.sprite.OrderedUpdates()
    main_group.add(Object(pos=(0, 300), move_function=move1))

    task = tulip.Task(main_loop(main_group))

    LOOP.run_until_complete(task)


if __name__ == "__main__":
    init()
    try:
        main()
    finally:
        LOOP.stop()
        pygame.quit()