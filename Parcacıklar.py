import pygame
from random import choice
vektor = pygame.math.Vector2
import os
os.environ ['SDL_VIDEO_WINDOW_POS'] ="433,50"
klasor = os.path.dirname(__file__)
resimklasoru=os.path.join(klasor,"Tasarımlar")

WIDTH=600
HEIGHT=670
FPS=60
TITLE="JUMPER"

TOPLURESIM = "Tasarımlar/spritesheet_jumper.png"


adventurer1 = pygame.image.load(os.path.join(resimklasoru,"adventurer_stand.png"))
adventurer2 = pygame.image.load(os.path.join(resimklasoru,"adventurer_walk1.png"))
adventurer3 = pygame.image.load(os.path.join(resimklasoru,"adventurer_walk2.png"))
adventurer6 = pygame.image.load(os.path.join(resimklasoru,"adventurer_action1.png"))
adventurer7 = pygame.image.load(os.path.join(resimklasoru,"adventurer_action2.png"))
zombie1 = pygame.image.load(os.path.join(resimklasoru,"zombie_walk1.png"))
zombie2 = pygame.image.load(os.path.join(resimklasoru,"zombie_walk2.png"))
zombie3 = pygame.image.load(os.path.join(resimklasoru,"zombie_action2.png"))

class Basamak (pygame.sprite.Sprite):
    def __init__(self,oyun,x,y):
        super().__init__()
        self.oyun = oyun
        self.image =choice([self.oyun.spritesheet.get_image(0,96,380,94),self.oyun.spritesheet.get_image(382,408,200,100)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Oyuncu(pygame.sprite.Sprite):

    def __init__(self,oyun):
        super().__init__()
        self.oyun = oyun
        self.load_images()
        self.sonZaman =0
        self.sayac = 0
        self.yuruyor = False
        self.image = self.beklemeler[0]
        self.rect = self.image.get_rect()
        self.rect.center =(WIDTH/2,HEIGHT/2)
        self.hiz = vektor(0,0)
        self.ivme = vektor(0,0.5)

    def load_images(self):
        self.beklemeler = [adventurer1,adventurer6,adventurer7]
        self.sag_yurumeler =[adventurer2,adventurer3]
        self.sol_yurumeler= []
        for yurume in self.sag_yurumeler:
            self.sol_yurumeler.append(pygame.transform.flip(yurume,True,False))

    def zipla(self):
        self.rect.y += 1
        temasKontrol = pygame.sprite.spritecollide(self,self.oyun.basamaklar,False)
        if temasKontrol:
            self.oyun.ziplamaSesi.play()
            self.hiz.y -=15


    def update(self, *args):

        self.animasyon()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                if self.hiz.x < 7:
                    self.ivme.x = 0.5
                else:
                    self.ivme.x = 0

            if keys[pygame.K_LEFT]:
                if self.hiz.x > -7:
                    self.ivme.x = -0.5
                else:
                    self.ivme.x = 0

            self.hiz.x += self.ivme.x

        else:
            if self.hiz.x > 0:
                self.hiz.x -= 0.2
            if self.hiz.x < 0:
                self.hiz.x += 0.2

        self.hiz.y += self.ivme.y

        if abs(self.hiz.x) < 0.2:
            self.hiz.x = 0

        self.rect.x += self.hiz.x
        self.rect.y += self.hiz.y

        if self.rect.x > WIDTH:
            self.rect.x = 0 - self.rect.width

        if self.rect.right < 0:
            self.rect.right = WIDTH + self.rect.width

        self.mask = pygame.mask.from_surface(self.image)

    def animasyon(self):
        simdikizaman = pygame.time.get_ticks()
        if self.hiz.x != 0:
            self.yuruyor = True
        else:
            self.yuruyor = False

        if self.yuruyor:
            if simdikizaman - self.sonZaman > 150:
                self.sonZaman = simdikizaman
                if self.hiz.x > 0:
                   bottom = self.rect.midbottom
                   self.image = self.sag_yurumeler[self.sayac % 2]
                   self.rect = self.image.get_rect()
                   self.rect.midbottom = bottom
                   self.sayac += 1
                else:
                   bottom = self.rect.midbottom
                   self.image = self.sol_yurumeler[self.sayac % 2]
                   self.rect = self.image.get_rect()
                   self.rect.midbottom = bottom
                   self.sayac += 1

        if not self.yuruyor:

            if simdikizaman - self.sonZaman > 250:
                self.sonZaman = simdikizaman
                bottom= self.rect.midbottom
                self.image = self.beklemeler[self.sayac %3]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom
                self.sayac += 1



class Dusman(pygame.sprite.Sprite):
    def __init__(self,oyun,platform):
        super().__init__()
        self.oyun = oyun
        self.platform = platform
        self.upload_images()

        self.image = self.bekleme
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.platform.rect.midtop
        self.hareketSonZaman = 0
        self.sayac = 0

        self.vx = 3

    def upload_images(self):
        self.bekleme = zombie3

        self.sag_yurumeler = [zombie1,zombie2]
        self.sol_yurumeler = []

        for yurume in self.sag_yurumeler:
            self.sol_yurumeler.append(pygame.transform.flip(yurume,True,False))

    def update(self, *args):
        self.rect.bottom = self.platform.rect.top

        if not self.oyun.basamaklar.has(self.platform):
            self.kill()

        self.rect.x += self.vx

        if self.rect.right + 4 > self.platform.rect.right or self.rect.x - 4 < self.platform.rect.left:
            kayitvx = self.vx
            self.vx = 0

            bottom = self.rect.midbottom
            self.image = self.bekleme
            self.rect = self.image.get_rect()
            self.rect.midbottom = bottom

            self.vx = kayitvx * -1

        if self.vx > 0:
            simdi = pygame.time.get_ticks()
            if simdi - self.hareketSonZaman > 250:
                self.hareketSonZaman = simdi
                bottom = self.rect.midbottom
                self.image = self.sag_yurumeler[self.sayac % 2]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom
                self.sayac += 1
        else:
            simdi = pygame.time.get_ticks()
            if simdi - self.hareketSonZaman > 250:
                self.hareketSonZaman = simdi
                bottom = self.rect.midbottom
                self.image = self.sol_yurumeler[self.sayac % 2]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom
                self.sayac += 1
        self.mask = pygame.mask.from_surface(self.image)

class Topluresim:
    def __init__(self,resimler):
        self.spritesheet = pygame.image.load(resimler).convert()

    def get_image(self,x,y,width,height):
        image = pygame.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        image.set_colorkey((0, 0, 0))
        return image

