import pygame
import random
import pgzrun
from random import random, randint, uniform

from pgzero.rect import Rect
from pygame import Color, Surface, Vector2, Rect

WIDTH = 1920
HEIGHT = 1080
X0 = WIDTH // 2
Y0 = HEIGHT // 2
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
stone_png = pygame.image.load('stone.png')
gravity = Vector2(0, 0.2)
num_stones = 5
dead = 0
#                               КЛАССЫ

class Rocket:
    def __init__(self):
        pass

    def draw(self):
        mouse_vec = Vector2(pygame.mouse.get_pos())
        screen.draw.filled_circle(pos=(mouse_vec.x, HEIGHT-20), color=(200, 200, 200), radius=15)


class Shot:
    def __init__(self, position: Vector2):
        self.position = position
        self.speed = Vector2(0, 3)

    def update(self):
        self.position -= self.speed

    def draw(self):
        screen.draw.filled_rect(
            Rect(self.position.x, self.position.y, 1, 24),
            Color(255, 0, 0)
        )


class Stone:
    def __init__(self, position, speed, hp):
        self.position = position
        self.speed = speed
        self.hp = hp
        self.image = pygame.transform.scale(pygame.image.load('stone.png'), (hp, hp))

    def update(self):
        self.position += self.speed
        if self.position.x <= 0 or self.position.x >= WIDTH:
            self.speed.x *= -1

    def draw(self):
        global debugging
        screen.draw.filled_circle(pos=self.position, color=(200, 200, 200), radius=self.hp)
        if debugging:
            screen.draw.text(f"HP = :{self.hp//1}, pos = :{self.position}", pos=self.position-Vector2(10, 10), color=(50, 50, 200))


class Part:
    def __init__(self, pos, vel, rad, clr, time):
        self.pos = pos
        self.vel = vel
        self.rad = rad
        self.clr = clr
        self.time = time

    def update(self):
        if not self.is_alive():
            return
        self.time -= 2
        self.pos += self.vel

    def draw(self):
        if self.is_alive():
            print(self.clr[0], self.time, self.clr[0]/(self.clr[0]/self.time))
            pygame.draw.circle(surface, center=self.pos, radius=self.rad, color=(self.time*(self.clr[0]/255), self.time*(self.clr[1]/255), self.time*(self.clr[2]/255)))

    def is_alive(self):
        return self.time > 0


class Genesis:
    def __init__(self, stone: Stone):
        self.rad = stone.hp
        self.mas = stone.hp * 5
        self.clr = (200, 200, 200)
        self.pos = stone.position
        #stones.remove(stone)
        self.parts = []

    def create_circle(self, rad):
        if self.rad > self.mas:
            return
        for _ in range(20):
            one_vec = Vector2(-1, 0)
            one_vec = one_vec.rotate(randint(0, 360))
            self.parts.append(Part(
                pos=self.pos + (one_vec * rad),
                vel=one_vec * random.uniform(-0.1, 1),
                rad=3,
                clr=self.clr,
                time=randint(100, 255)
            ))

    def update(self):
        self.rad += 1
        self.create_circle(self.rad)
        for p in self.parts:
            if p.is_alive():
                p.update()
            else:
                self.parts.remove(p)

    def draw(self):
        for p in self.parts:
            p.draw()


class Particle:
    def __init__(self, position: Vector2, speed, is_firework=False, mass=1):
        self.position = Vector2(position.x, position.y)
        self.speed = speed
        self.is_firework = is_firework
        self.mass = mass
        self.start_speed = speed
        self.life = 255
        self.a = Vector2(0, 0)

    def is_alive(self):
        return self.life > 0

    def apply_force(self, force):
        self.speed += force / self.mass

    def update(self):
        self.life -= 1
        if self.is_alive():
            self.speed += self.a
            if not self.is_firework:
                self.velocity = self.speed
                self.life -= 4
            self.position +=self.speed
            self.a = Vector2(0, 0)

    def draw(self, surface: Surface):
        global fireworks
        if self.is_alive():
            red = self.life * random()
            green = self.life * random()
            blue = self.life * random()
            if self.is_firework:
                color = (red, green, blue)
            else:
                color = (red, green, blue)
            pygame.draw.circle(surface, center=self.position, radius=2, color=color)
        else:
            return


class Firework:
    def __init__(self, pos: Vector2):
        self.firework = Particle(position=pos, speed=Vector2(0, randint(-21, -8)))
        self.is_exploaded = False
        self.particles = []

    def update(self):
        global gravity
        if not self.is_exploaded:
            self.firework.apply_force(gravity)
            self.firework.update()
            if self.firework.velocity.y > 0 and not self.is_exploaded:
                self.is_exploaded = True
                self.explode()
        for p in self.particles:
            p.apply_force(gravity)
            p.update()

    def draw(self, surface: Surface):
        if not self.is_exploaded:
            self.firework.draw(surface)
        for p in self.particles:
            p.draw(surface)

    def explode(self):
        for i in range(50):
            velocity: Vector2 = random_vector() * randint(2, 10)
            self.particles.append(Particle(
                position=Vector2(self.firework.position),
                speed=velocity,
                is_firework=False
                )
            )


#                               ФУНКЦИИ

def on_key_down(key):
    global pause, debugging
    mouse_vec = Vector2(pygame.mouse.get_pos())
    if key == pygame.K_SPACE:
        shots.append(Shot(
            position=Vector2(mouse_vec.x, HEIGHT-50)
        ))
    if key == pygame.K_ESCAPE:
        pause = not pause
    if key == pygame.K_q:
        debugging = not debugging


def random_vector():
    angle = randint(0, 360)
    return Vector2(1, 0).rotate(angle)


def keys():
    font = 35
    screen.draw.text("ESC-Pause", pos=(0, 40), fontsize=font, color=(255, 255, 255))
    screen.draw.text("SPACE-Fire", pos=(0, font * 2), fontsize=font, color=(255, 255, 255))

#                               МАССИВЫ


stones = [
    Stone(
        position=Vector2(random() * WIDTH, 10),
        hp=uniform(0.15, 0.99999)*70,
        speed=Vector2(random() * randint(-1, 1), random()*3)
    )for _ in range(num_stones)
]
shots = []
rocket = Rocket()
to_delete = []
pause = False
debugging = False
stars = [
    Vector2(random()*WIDTH, random()*HEIGHT)
    for _ in range(250)
]
fireworks = []
genesises = []
#                            UPDATE & DRAW


def update():
    global dead, pause
    if pause:
        return
    for i in stones:
        i.update()
        for j in shots:
            if (i.position - j.position).length() <= i.hp:
                to_delete.append(j)
                i.hp = 0
                genesises.append(Genesis(i))
                if i.hp <= 0:
                    dead += 1
                    shots.remove(j)
                    stones.remove(i)
                    genesises.append(Genesis(i))
                if j.position.y <= 0:
                    shots.remove(j)
    for i in shots:
        i.update()
    if dead >= num_stones:
        for firework in fireworks:
            firework.update()
        if randint(0, 100) > 75:
            fireworks.append(Firework(pos=Vector2(randint(0, WIDTH), HEIGHT - 10)))
    for g in genesises:
        if g.rad < g.mas * 10:
            g.update()
        else:
            genesises.remove(g)


def draw():
    global dead, pause
    screen.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface.fill((0, 0, 0, 255 / 5))
    if dead >= num_stones:
        screen.draw.text("WIN", pos=(X0-100, Y0 - 20), fontsize=150, color=(255, 255, 255))
        for firework in fireworks:
            firework.draw(surface)
        screen.blit(surface, pos=(0, 0))
    else:
        screen.blit(surface, pos=(0, 0))
    screen.draw.text(f"Kills:{dead}", pos=(10, 10), fontsize=30, color=(255, 255, 255))
    if pause:
        keys()
        screen.draw.text("PAUSE", pos=(X0-140, Y0 - 20), fontsize=150, color=(255, 255, 255))
    for g in genesises:
        g.draw()
    for i in stones:
        i.draw()
    rocket.draw()
    for i in shots:
        i.draw()
    for i in stars:
        screen.draw.filled_circle(pos=i, color=(200, 200, 200), radius=2)


pgzrun.go()