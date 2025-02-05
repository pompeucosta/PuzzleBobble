import pygame
from os.path import join

from levels.level_loader import LevelLoader
from objects.arena.arena import Arena
from objects.score import Score
from objects.bubbleShooter import BubbleShooter
from objects.colors import bubble_sprites, BubbleColor
from utils.spritesheet import SpriteSheet
from maps.metal_map import MetalMap
import utils.settings as settings
from states.game.game_state import GameState
import states.game.game_over_menu_state as goms

class PlayState(GameState):
    def __init__(self, level: int) -> None:
        pygame.display.set_caption(settings.GAME_CAPTION)

        self._map = MetalMap()
        bg = pygame.sprite.Sprite()
        bg.image = self._map.bg_image
        bg.rect = bg.image.get_rect()

        self.WIDTH =  bg.rect.width
        self.HEIGHT = bg.rect.height
        self._display = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.GAME_EVENT = pygame.event.custom_type()

        self._running = True
        self._win = False

        self._lose_level = False
        self._next_level = False
        self._bubbles_during_animation = 0

        self.scoreFont = pygame.font.SysFont(settings.SCORE_TEXT_FONT_NAME, settings.SCORE_TEXT_FONT_SIZE)

        self._load_bubbles()

        self._bg_group = pygame.sprite.Group()
        self._bg_group.add(bg)

        self._score = Score()

        self._create_base_map(level)
        self._load_current_arena()

        self._keysdown = set()


    @property
    def running(self) -> bool:
        return self._running
    
    @property
    def win(self) -> bool:
        return self._win
    
    @property
    def level(self) -> int:
        current = self._level_loader.current_level_index
        max_level = len(self._level_loader.levels)
        return min(current + 1, max_level)


    def handle_input(self, events) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._keysdown.add(event.key)
                self._bubbleShooter.input_handler.input_start(event.key)
            elif event.type == pygame.KEYUP:
                #could had a on_stop event for when the player stops pressing the key
                if event.key in self._keysdown:
                    self._keysdown.remove(event.key)
            elif event.type == self.GAME_EVENT:
                print(event.txt)
        
        for key in self._keysdown:
            self._bubbleShooter.input_handler.input_triggered(key)

    def update(self, dt: float) -> None:
        self._bubbleShooter.update(dt=dt)
        if self.arena is not None:
            self.arena.update(dt=dt)

        if self._next_level and self._bubbles_during_animation == 0:
            self._level_loader.next_level()
            self._load_current_arena()
            self._next_level = False
        
        if self._lose_level and self._bubbles_during_animation == 0:
            self._win = False
            self._running = False

    def draw(self) -> None:
        self._display.fill(settings.BG_COLOR)

        self._bg_group.draw(self._display)

        if self.arena is not None:
            floor = self.arena.get_floor()
            self._display.blit(floor.image,floor.rect)

            ceiling = self.arena.get_ceiling()
            self._display.blit(ceiling.image,ceiling.rect)

        self._bubbleShooter.draw(self._display)

        if self.arena is not None:
            self.arena.get_grid().draw(self._display)
            self.arena.get_dynamic_bubbles().draw(self._display)

        score_surface = self.scoreFont.render(f"Score: {self._score.score}",False,settings.SCORE_TEXT_COLOR,settings.SCORE_TEXT_BG_COLOR)
        self._display.blit(score_surface,settings.SCORE_SCREEN_POSITION)

        pygame.display.flip()


    def _create_base_map(self, level: int) -> None:
        self._level_loader = LevelLoader(
            *self._map.grid_size, self._map.grid_topleft,
            initial_level_index=level - 1
        )
        self.arena = None
        self._bubbleShooter = BubbleShooter(self._map.shooter_position,join("sprites","shooter.png"),join("sprites","arrow.png"))


    def _register_handlers(self) -> None:
        if self.arena is not None:
            self.arena.register_win_handler(self.on_win)
            self.arena.register_lose_handler(self.on_lose)
            self.arena.register_bubble_start_animation_handler(self._handle_bubble_start_animation)
            self.arena.register_bubble_pop_handler(self.handle_bubble_pop)
            self.arena.register_bubble_pop_handler(self._score.handle_bubble_pop)
            self._bubbleShooter.register_on_shoot_event(self.arena.shooter_shoot_handler)
    
    def _unregister_important_handlers(self) -> None:
        if self.arena is not None:
            self._bubbleShooter.unregister_on_shoot_event(self.arena.shooter_shoot_handler)
            self.arena.unregister_win_handler(self.on_win)
            self.arena.unregister_lose_handler(self.on_lose)

    def _unregister_animation_handlers(self) -> None:
        if self.arena is not None:
            self.arena.unregister_bubble_start_animation_handler(self._handle_bubble_start_animation)
            self.arena.unregister_bubble_pop_handler(self.handle_bubble_pop)
            self.arena.unregister_bubble_pop_handler(self._score.handle_bubble_pop)
    

    def _load_current_arena(self) -> None:
        # unregister handlers from previous arena (if any)
        self._unregister_important_handlers()
        self._unregister_animation_handlers()

        # load current grid
        grid = self._level_loader.load_current_level()

        # in case of invalid level, stop the game
        if grid is None:
            self._win = True
            self._running = False
            return

        # create new arena
        self.arena = Arena(self._bubbleShooter.position.copy(), self._map,grid)
        self._register_handlers()

    def on_lose(self) -> None:
        self._lose_level = True

    def on_win(self) -> None:
        self._unregister_important_handlers()
        self._next_level = True

    def _handle_bubble_start_animation(self,_) -> None:
        self._bubbles_during_animation += 1
    
    def handle_bubble_pop(self,_) -> None:
        self._bubbles_during_animation -= 1

    
    def _load_bubbles(self):
        bubbles = join("sprites","bubbles.png")
        sheet = SpriteSheet(bubbles)

        COLORS = [BubbleColor.BLUE,BubbleColor.RED,BubbleColor.PURPLE,BubbleColor.BLACK,
                  BubbleColor.YELLOW,BubbleColor.GREEN,BubbleColor.ORANGE,BubbleColor.GRAY]
        CELL_SIZE = 32
        for row,color in enumerate(COLORS):
            # 7 sprites per color (the first is the bubble itself, the others are the pop animation)
            rects = [(col * CELL_SIZE,row * CELL_SIZE,CELL_SIZE,CELL_SIZE) for col in range(0,7)]
            sprites = sheet.images_at(rects,-1)
            bubble_sprites[color] = sprites

    def next_state(self) -> GameState:
        return self if self._running else goms.GameOverMenuState(self._score.score, self.level, self._win)
