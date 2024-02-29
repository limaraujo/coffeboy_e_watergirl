import pygame
NEIGHBOR_OFFSET = [(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(0,0),(-1,1),(0,1),(1,1),]
COLLIDABLE_TILE_TYPES = {"grass", "stone"}
from modules.utils import sum_vectors, k_vector


def pos_in_pixels(pos_normal, tile_size=16):
    return tuple(map(lambda x: x*tile_size, pos_normal))

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        #temos dois sistemas: um que é em uma grid (grade)
        self.tilemap = {}
        #e outro que pode nao estar alinhado à grade
        #esses offgrids sao decoracoes, background, basicamente
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap["10;" + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}            
    
    def neighbor_tiles(self, pos):
        """Retorna uma lista com no máximo todos os 9 blocos ao redor do personagem, se existirem"""
        # a posicao esta em pixel, passemos-na pra posicao em tiles
        tile_position = tuple(map (lambda axis:(int(axis // self.tile_size)), pos))
        tiles = []
        for offset in NEIGHBOR_OFFSET:
            possible_block = str(tile_position[0] + offset[0]) + ";" + str(tile_position[1] + offset[1])
            if possible_block in self.tilemap:
                tiles.append(self.tilemap[possible_block])
        return tiles

    def physics_rects_around(self, pos):
        """Retorna a lista dos retangulos colidiveis ao nosso redor"""
        rects = []
        for tile in self.neighbor_tiles(pos):
            if tile['type'] in COLLIDABLE_TILE_TYPES:
                rects.append(pygame.Rect(*pos_in_pixels(tile['pos']), self.tile_size, self.tile_size ))
        return rects
    
    def render(self, surface, offset=(0,0)):
        
        for tile in self.offgrid_tiles:
            #interpretaremos a posicao como PIXEL, nao como lugar na grid
            surface.blit(self.game.assets[tile['type']][tile['variant']],sum_vectors( k_vector(-1, offset), tile['pos']) )

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            #pega a lista de assets daquele tipo, acessa o indice (variant) dela e desenha
            surface.blit(self.game.assets[tile['type']][tile['variant']],
                         sum_vectors(k_vector(-1, offset), 
                         tuple(map(lambda x: x*self.tile_size, tile['pos'])))
        )