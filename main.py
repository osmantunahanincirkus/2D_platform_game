import pygame
import random
import sys
from  Parcacıklar import  *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock=pygame.time.Clock()
        self.spritesheet = Topluresim(TOPLURESIM)
        self.running = True
        self.platformsayac = 0
        self.eskor = 0
        self.skor = 0
        self.maximumSkor = 0
        self.ziplamaSesi = pygame.mixer.Sound("ziplama.wav")
        pygame.mixer.music.load("background_music.ogg")
        pygame.mixer.music.set_volume(0.2)



    def run(self):
        self.playing = True
        pygame.mixer.music.play()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()

        pygame.mixer.music.fadeout(1000)

    def draw(self):
        self.screen.fill((226,169,83))
        self.ekranaYazdirma("Skor: {}".format(self.skor))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image,self.player.rect)

    def new(self):
         self.all_sprites =pygame.sprite.Group()
         self.basamaklar = pygame.sprite.Group()
         self.dusmanlar = pygame.sprite.Group()


         b1 = Basamak(self,250,HEIGHT-30)
         b2 = Basamak(self,WIDTH/2-50,350)
         b3 = Basamak(self,400,300)
         b4 = Basamak(self,250,200)
         b5 = Basamak(self,100,200)
         b6 = Basamak(self,50,400)

         self.basamaklar.add(b1)
         self.basamaklar.add(b2)
         self.basamaklar.add(b3)
         self.basamaklar.add(b4)
         self.basamaklar.add(b5)
         self.basamaklar.add(b6)

         self.player = Oyuncu(self)
         self.all_sprites.add(self.player)
         self.all_sprites.add(b1)
         self.all_sprites.add(b2)
         self.all_sprites.add(b3)
         self.all_sprites.add(b4)
         self.all_sprites.add(b5)
         self.all_sprites.add(b6)
         self.run()

    def girisEkrani(self):
        resim = pygame.image.load("baslangic.png")
        self.screen.blit(resim,resim.get_rect())
        pygame.display.update()
        self.gekran()

    def bitisEkrani(self):
        resim = pygame.image.load("gameOver.png")
        self.screen.blit(resim, resim.get_rect())

        font = pygame.font.SysFont("Century Gothic", 25)
        text = font.render("Skor : {} ".format(self.eskor), True, (0, 0, 0))
        self.screen.blit(text, (250 - (text.get_size()[0] / 2), 350))
        font1 = pygame.font.SysFont("Century Gothic", 25)
        text1 = font1.render("En Yuksek Skor : {} ".format(self.maximumSkor), True, (0, 0, 0))
        self.screen.blit(text1, (250 - (text.get_size()[0] / 2), 400))
        pygame.display.update()
        self.gekran()

    def gekran(self):
        bekleme = True
        while bekleme:
            self.clock.tick(FPS)
            for event in pygame.event.get():
               if event.type ==pygame.QUIT:
                  bekleme =False
                  self.running = False
               if event.type == pygame.KEYDOWN:
                   bekleme = False


    def ekranaYazdirma(self,yazi):
        font = pygame.font.SysFont("Century Gothic",25)
        text = font.render(yazi,True,(255,255,255))
        self.screen.blit(text,(WIDTH/2-(text.get_size()[0]/2),0))

    def update(self):
        self.all_sprites.update()

        if self.player.hiz.y > 0:
            carpismalar = pygame.sprite.spritecollide(self.player,self.basamaklar,dokill=False)

            if carpismalar:
                durum = self.player.rect.midbottom[0] <= carpismalar[0].rect.left-8 or self.player.rect.midbottom[0] >= carpismalar[0].rect.right+8
                if carpismalar[0].rect.center[1] + 6 > self.player.rect.bottom and not durum:
                   self.player.hiz.y = 0
                   self.player.rect.bottom = carpismalar[0].rect.top

        if self.player.rect.top < HEIGHT/4:
            self.player.rect.y += max(abs(self.player.hiz.y),3)
            for bas in self.basamaklar:
                bas.rect.y += max(abs(self.player.hiz.y),3)
                if bas.rect.top >= HEIGHT:
                    bas.kill()
                    self.skor += 15
        dusmanTemasi = pygame.sprite.spritecollide(self.player,self.dusmanlar,False,pygame.sprite.collide_mask)
        if dusmanTemasi:
            self.playing = False
            with open ("skor.txt","r") as dosya:
                maxskor = int(dosya.read())
                if self.skor > maxskor:
                     with open("skor.txt","w") as dosya:
                        dosya.writelines(str(self.skor))
                     self.maximumSkor = self.skor
                else:
                    with open("skor.txt","r") as dosya:
                        skor = str(dosya.read())
                        self.maximumSkor = skor

            self.eskor= self.skor
            self.skor = 0

        if self.player.rect.top > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.hiz.y,15)
                if sprite.rect.bottom < 0:
                    sprite.kill()



        if len(self.basamaklar) == 0:
            with open ("skor.txt","r") as dosya:
                maxskor = int(dosya.read())
                if self.skor > maxskor:
                     with open("skor.txt","w") as dosya:
                        dosya.writelines(str(self.skor))
                     self.maximumSkor = self.skor
                else:
                    with open("skor.txt","r") as dosya:
                        skor = str(dosya.read())
                        self.maximumSkor = skor

            self.eskor= self.skor
            self.skor = 0
            self.playing = False

        while len(self.basamaklar) < 6:
            if self.platformsayac ==0:
                genislik = random.randrange(50, 100)
                b = Basamak(self, random.randrange(0, WIDTH - genislik), random.randrange(-2, 0))
            else:
                genislik = random.randrange(50,100)
                b = Basamak(self,random.randrange(0,WIDTH-genislik),random.randrange(-40,-2))
            self.platformsayac +=1
            if len(self.basamaklar)== 5:
                self.platformsayac = 0
            self.basamaklar.add(b)
            self.all_sprites.add(b)

            if b.rect.width > 100:
                if random.randint(1,5)==1:
                    dusman = Dusman(self,b)
                    self.dusmanlar.add(dusman)
                    self.all_sprites.add(dusman)

        pygame.display.update()




    def events(self):
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               sys.exit()

           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                   self.player.zipla()

game = Game()
game.girisEkrani()

while game.running:
    game.new()
    game.bitisEkrani()



