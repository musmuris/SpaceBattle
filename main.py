import pygame
import random

from pygame.sprite import AbstractGroup
import images as loader

# Setup
pygame.init()
windowSize=(800,600)#
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

images = loader.load_images()

BLACK = (0,0,0)

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, scale = 1):
        super().__init__()
        if scale != 1:
            rect = image.get_rect().scale_by(scale)
            self.image =  pygame.transform.scale(image, rect.size)
        else:
            self.image=image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def collide(self, other):
        offset = (other.rect.left - self.rect.left, other.rect.top - self.rect.top)
        return self.mask.overlap(other.mask, offset ) != None

# Sprites
class Player(Actor):
    def __init__(self):
        super().__init__(images.playerShip1_orange)
        r = screen.get_rect()
        self.rect.center = r.center
        self.rect.bottom = r.bottom

    def update(self, left, right, bounds):
        if left:
            self.rect.left=max(self.rect.left-10, bounds.left)
        if right:
            self.rect.right=min(self.rect.right+10, bounds.right)

class Projectile(Actor):
    def __init__(self, pos):
        super().__init__(images.laserRed04, scale=0.5)
        self.rect.center = pos

    def update(self, bounds):
        self.rect.centery -= 5
        if self.rect.bottom < bounds.top:
            self.kill()


class Baddie(Actor):
    def __init__(self, pos):
        super().__init__(images.enemyGreen1, scale=0.75)
        self.rect.center = pos
        self.speed = 5

    def update(self, bounds):
        #self.rect.centerx += self.speed
        if self.rect.left < bounds.left:
            self.speed = -self.speed
        if self.rect.right > bounds.right:
            self.speed = -self.speed

class Star:
    def __init__(self, speed):
        self.speed = speed
        r = screen.get_rect()
        self.x = random.randint(0, r.right)
        self.y = random.randint(0, r.bottom)

    def update(self):
        self.y += self.speed
        r = screen.get_rect()
        if self.y > r.bottom:
            self.x = random.randint(0,r.right)
            self.y -= r.bottom

    def pos(self):
        return (int(self.x), int(self.y))

class Game:
    def __init__(self):
        self.players=pygame.sprite.Group()
        self.projectiles=pygame.sprite.Group()
        self.baddies=pygame.sprite.Group()

        self.player = Player()
        self.players.add(self.player)

        r = screen.get_rect()
        r.centery = 50
        self.baddies.add(Baddie(r.center))


    def doFire(self, player):
        if self.tick < self.lastFire + 15:
            return
        self.lastFire = self.tick
        pos = (player.rect.centerx, player.rect.centery - 35)
        b = Projectile(pos)
        self.projectiles.add(b)

    def doCollide(self, baddie, projectiles):
        for p in projectiles:
            if baddie.collide(p):
                baddie.kill()
                p.kill()
                r = screen.get_rect()
                r.centerx = pygame.time.get_ticks() % 600 + 100
                r.centery = 50
                self.baddies.add(Baddie(r.center))


    def run(self):
        # Main game loop

        finished=False
        stars = [ Star(random.random() + x % 3) for x in range(40)]
        self.tick = 0
        self.lastFire = 0
        while not finished:
            clock.tick(60)
            self.tick += 1

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished=True

            keys = pygame.key.get_pressed()
            self.player.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], screen.get_rect())

            if keys[pygame.K_SPACE]:
                self.doFire(self.player)

            screen.fill(BLACK)
            for s in stars:
                i = int(s.speed * 50) + 70
                screen.set_at(s.pos(), (i,i,i))
                s.update()

            self.baddies.update(screen.get_rect())
            self.projectiles.update(screen.get_rect())

            collisions = pygame.sprite.groupcollide(self.baddies, self.projectiles, False, False)
            for k,v in collisions.items():
                if len(v) > 0:
                    self.doCollide(k, v)

            self.projectiles.draw(screen)
            self.baddies.draw(screen)
            self.players.draw(screen)
            pygame.display.flip()

g = Game()
g.run()
pygame.quit()

