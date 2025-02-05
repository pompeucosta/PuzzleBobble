from maps.map import Map
from utils.settings import GAME_SCALE,BUBBLE_RADIUS
import pygame
from os.path import join
from objects.wall import Wall 

class MetalMap(Map):
    def __init__(self):
        image = pygame.image.load(join("sprites","bg.png"))
        image = pygame.transform.scale_by(image,GAME_SCALE)
        super().__init__(image)

        floor_image = pygame.image.load(join("sprites","floor.png"))
        floor_image = pygame.transform.scale_by(floor_image,GAME_SCALE)
        floor_position = pygame.Vector2(96 * GAME_SCALE,181 * GAME_SCALE)
        self._floor = Wall(floor_position,image=floor_image)

        self._ceiling_image = pygame.image.load(join("sprites","ceiling.png"))
        self._ceiling_image = pygame.transform.scale_by(self._ceiling_image,GAME_SCALE)
        self._ceiling_position = pygame.Vector2(self.grid_topleft[0],self.arena_topleft[1])

        wall_thickness = 6 * GAME_SCALE 
        self._side_walls = [
            Wall(pygame.Vector2(self.arena_topleft[0] + wall_thickness,self.arena_topleft[1]),pygame.Vector2(1,self.arena_size[1])),
            Wall(pygame.Vector2(self.arena_topleft[0] + self.arena_size[0],self.arena_topleft[1]),pygame.Vector2(1,self.arena_size[1]))
        ]

    @property
    def bg_floor_height(self):
        return 8 * GAME_SCALE
    
    @property
    def arena_topleft(self):
        return (88 * GAME_SCALE,16 * GAME_SCALE)
    
    @property
    def arena_size(self):
        return (136 * GAME_SCALE,207 * GAME_SCALE)

    @property
    def arena_floor(self):
        return self._floor
    
    @property
    def arena_ceiling(self):
        return Wall(self._ceiling_position.copy(),image=self._ceiling_image)
    
    @property
    def arena_side_walls(self):
        return self._side_walls

    @property
    def arena_down_cd(self):
        return 30

    @property
    def arena_down_move_amount(self):
        return 20 * GAME_SCALE

    @property
    def arena_down_transition_duration(self):
        # the time it will take to move the arena down the above amount (in seconds)
        return 3

    @property
    def arena_wall_pixel_thickness(self):
        return 6 * GAME_SCALE

    @property
    def grid_topleft(self):
        return (96 * GAME_SCALE,24 * GAME_SCALE)

    @property
    def grid_size(self):
        return (127 * GAME_SCALE,199 * GAME_SCALE)
    
    @property
    def shooter_position(self):
        shooter_height_center = 20 * GAME_SCALE
        return pygame.Vector2(self.grid_topleft[0] + self.grid_size[0] / 2,self.bg_size[1] - self.bg_floor_height - shooter_height_center)
    
    @property
    def next_bubble_position(self):
        return pygame.Vector2(self.shooter_position.x - 30 * GAME_SCALE, self.bg_size[1] - self.bg_floor_height - BUBBLE_RADIUS)