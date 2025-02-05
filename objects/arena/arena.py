from typing import Any, List
import pygame
from objects.arena.hex_grid import HexGrid
from objects.wall import Wall
from objects.bubble import Bubble
from physics.staticPhysics import StaticPhysics
from physics.kinematicPhysics import KinematicPhysics
from maps.map import Map

import utils.settings as settings

import random


class Arena:
    def __init__(
            self,
            shooter_position: pygame.Vector2,
            map: Map,
            grid: HexGrid) -> None:

        self._map = map
        self._shooter_position = shooter_position.copy()
        self._next_bubble_position = self._map.next_bubble_position

        self._grid = grid
        self._grid.register_on_bubble_float_handler(self._handle_bubble_float)
        self._grid.register_on_bubble_pop_handler(self._handle_bubble_pop)
        self._grid.register_on_empty_handler(self._on_grid_empty)
        self._walls: list[Wall] = self._map.arena_side_walls

        self._floor = self._map.arena_floor

        self._ceiling = self._map.arena_ceiling

        self._dynamic_bubbles = pygame.sprite.Group()

        self._shooter_bubble = self.generate_random_bubble(self._shooter_position.copy(),self.get_random_color())
        self.spawn_bubble(self._shooter_bubble)

        self._next_bubble = self.generate_random_bubble(self._next_bubble_position,self.get_random_color())
        self.spawn_bubble(self._next_bubble)

        self._moving = False
        self._arena_down_current_time = self._map.arena_down_cd

        self._lose_handlers = list()
        self._win_handlers = list()
        self._bubble_start_animation_handlers = list()
        self._bubble_pop_handlers = list()

        self._grid_empty = False

    def spawn_bubble(self,bubble: Bubble):
        self._dynamic_bubbles.add(bubble)

    def generate_random_bubble(self,position,color):
        phys = StaticPhysics(position)
        return Bubble(phys,color=color)

    def get_random_color(self):
        colors = [color for color in self._grid.get_present_colors()]
        return random.choice(colors) if len(colors) > 0 else None


    def update(self, *args: Any, **kwargs: Any) -> None:
        self._dynamic_bubbles.update(*args,**kwargs)
        self._bubbles_collide_with_walls()
        self._bubbles_collide_with_grid()
        self._bubbles_collide_with_floor() 

        self._update_arena_down(dt=kwargs["dt"]) 
        self._grid.update(*args,**kwargs)      

    def get_floor(self):
        return self._floor
    
    def get_ceiling(self):
        return self._ceiling

    def get_dynamic_bubbles(self):
        return self._dynamic_bubbles
    
    def get_grid(self):
        return self._grid

    def _bubbles_collide_with_walls(self):
        for bubble in self._dynamic_bubbles:
            for wall in self._walls:
                if pygame.Vector2(bubble.position[0],0).distance_to(pygame.Vector2(wall.rect.x,0)) <= bubble.radius:
                    bubble.change_direction()
                elif pygame.Vector2(0,bubble.position[1]).distance_to(pygame.Vector2(0,self._ceiling.rect.y)) <= bubble.radius:
                    self._add_bubble_to_grid(bubble)

    def _bubbles_collide_with_grid(self):
        for bubble in self._dynamic_bubbles:
            for grid_bubble in self._grid:
                if bubble.shoted and pygame.sprite.collide_circle(bubble,grid_bubble):
                    self._add_bubble_to_grid(bubble)

    def _add_bubble_to_grid(self,bubble: Bubble):
        self._dynamic_bubbles.remove(bubble)
        bubble.stop()

        hex_position = self._grid.add_bubble(bubble)

        if hex_position == None:
            print("[ARENA] failed to add bubble")
            return None

        self._grid._pop_bubbles_from(hex_position)

    def _bubbles_collide_with_floor(self):
        for bubble in self._dynamic_bubbles:
            if bubble.floating and pygame.sprite.collide_rect(bubble,self._floor):
                    bubble.floor_hit()
        
        grid_collided = pygame.sprite.groupcollide(self._grid,pygame.sprite.Group(self._floor),False,False)
        if len(grid_collided) > 0:
            for handler in self._lose_handlers:
                handler()


    def _update_arena_down(self,dt):
        self._arena_down_current_time -= dt

        if self._arena_down_current_time <= 0:
            self._initial_pos = self._ceiling.rect.topleft[1]
            self._moving = True
            self._current_move_time = 0
            self._arena_down_current_time = self._map.arena_down_cd

        if self._moving:
            weight = self._current_move_time / self._map.arena_down_transition_duration
            self._current_move_time += dt
            pos = pygame.math.lerp(self._initial_pos,self._initial_pos + self._map.arena_down_move_amount,weight)
            amount = pos - self._ceiling.rect.topleft[1]
            self._ceiling.rect.topleft = (self._ceiling.rect.x,pos)
            self._grid.move_grid_down(amount)
            self._moving = self._current_move_time < self._map.arena_down_transition_duration
    
    def shooter_shoot_handler(self,shoot_direction: pygame.Vector2):
        if self._grid_empty:
            return None
        
        self._shooter_bubble.shot(shoot_direction)

        self._shooter_bubble = self._next_bubble
        self._shooter_bubble.position = (self._shooter_position[0],self._shooter_position[1])

        self._next_bubble = self.generate_random_bubble(self._next_bubble_position,self.get_random_color())
        self.spawn_bubble(self._next_bubble)

    def _handle_bubble_pop(self,bubble: Bubble):
        self.spawn_bubble(bubble)
        bubble.register_on_pop_animation_finished(self._handle_bubble_pop_finished)
        self._handle_bubble_start_animation(bubble)
        bubble.play_pop_animation()

    def _handle_bubble_float(self,bubble: Bubble):
        dir_x = random.randrange(settings.BUBBLE_FLOATING_DIRECTION_X_MINIMUM,settings.BUBBLE_FLOATING_DIRECTION_X_MAXIMUM) / 10
        bubble.physics = KinematicPhysics(pygame.Vector2(*bubble.position),
                                          pygame.Vector2(dir_x,1 - dir_x).normalize(),
                                          pygame.Vector2(settings.BUBBLE_FLOATING_ACCELERATION_X,settings.BUBBLE_FLOATING_ACCELERATION_Y))
        
        bubble.set_floating(random.randrange(settings.BUBBLE_FLOATING_DURATION_MINIMUM,settings.BUBBLE_FLOATING_DURATION_MAXIMUM))
        bubble.register_on_pop_animation_finished(self._handle_bubble_pop_finished)
        self._handle_bubble_start_animation(bubble)
        self.spawn_bubble(bubble)

    def _handle_bubble_start_animation(self,bubble: Bubble):
        for handler in self._bubble_start_animation_handlers:
            handler(bubble)

    def _handle_bubble_pop_finished(self,bubble: Bubble):
        for handler in self._bubble_pop_handlers:
            handler(bubble)

        bubble.unregister_on_pop_animation_finished(self._handle_bubble_pop_finished)
        self._dynamic_bubbles.remove(bubble)
        if self._grid_empty and len(self._dynamic_bubbles.sprites()) <= 2:
            for handler in self._win_handlers:
                handler()

    def _on_grid_empty(self):
        self._grid_empty = True

    def register_bubble_start_animation_handler(self,handler):
        self._bubble_start_animation_handlers.append(handler)

    def register_bubble_pop_handler(self,handler):
        self._bubble_pop_handlers.append(handler)
    
    def register_win_handler(self,handler):
        self._win_handlers.append(handler)

    def register_lose_handler(self,handler):
        self._lose_handlers.append(handler)


    def unregister_bubble_start_animation_handler(self,handler):
        self._bubble_start_animation_handlers = [h for h in self._bubble_start_animation_handlers if h != handler]

    def unregister_bubble_pop_handler(self,handler):
        self._bubble_pop_handlers = [h for h in self._bubble_pop_handlers if h != handler]
    
    def unregister_win_handler(self,handler):
        self._win_handlers = [h for h in self._win_handlers if h != handler]
    
    def unregister_lose_handler(self,handler):
        self._lose_handlers = [h for h in self._lose_handlers if h != handler]
