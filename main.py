import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity, Player
from modules.utils import load_image, load_images, Animation
from modules.tilemap import Tilemap
def distance(A, B): return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5

class Game(modules.input.Input):
    def __init__(self):
        modules.input.Input.__init__(self)
        self.width = 1280
        self.height = 960

        pygame.init()
        pygame.display.set_caption("coffeboy e watergirl")

        self.screen = pygame.display.set_mode((self.width, self.height))
        #gera uma imagem. Pra aumentar o tamanho das coisas na tela,
        #renderizamos nela e depois escalamos pra screen 
        #é no display que gravaremos as coisas
        self.display = pygame.Surface((320, 240))

        self.player_x, self.player_y = self.width // 2, self.height // 2
        self.movement = [False, False]

        #loads the images as a list of assets containing every variant of that type
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player/idle/00.png'),
            'background': load_image("Background2.png"),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=4)
            }
        #print(self.assets)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, map_filename="data/maps/1.json", tile_size=16)
        self.back = pygame.image.load("data/images/clouds/cloud_1.png")
        #esse é o offset da camera
        self.scroll = [0,0]

        #preparar o background
        self.assets['background'] = pygame.transform.scale(self.assets['background'], self.display.get_size())


    def run(self):
        clock = pygame.time.Clock()

        while True:
            #self.display.fill((200,200,255))
            self.display.blit(self.assets['background'], (0,0))


            #dividir por 2 pra que fique no meio
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() // 2 - self.scroll[0]) // 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() // 2 - self.scroll[1]) // 10

            self.tilemap.render(self.display, offset=self.scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=self.scroll)

            #print(self.tilemap.physics_rects_around(self.player.pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                
                    

            pygame.draw.rect(self.display, (255,0,0), (self.player_x, self.player_y, 10, 16))

            # isto aqui é o que escala o display pra screen (A tela de vdd)
            # e escreve na tela as alteracoes que fizemos, a cada iter
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            clock.tick(60)












Game().run()