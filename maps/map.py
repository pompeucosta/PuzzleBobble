from abc import ABC,abstractmethod

class Map(ABC):
    def __init__(self,bg_image):
        super().__init__()
        self._bg_image = bg_image

    @property
    def bg_image(self):
        return self._bg_image
    
    @property
    def bg_size(self):
        return (self._bg_image.get_width(),self._bg_image.get_height())

    @property
    @abstractmethod
    def bg_floor_height(self):
        pass

    @property
    @abstractmethod
    def arena_topleft(self):
        pass
    
    @property
    @abstractmethod
    def arena_size(self):
        pass

    @property
    @abstractmethod
    def arena_floor(self):
        pass

    @property
    @abstractmethod
    def arena_ceiling(self):
        pass

    @property
    @abstractmethod
    def arena_side_walls(self):
        pass

    @property
    @abstractmethod
    def arena_down_cd(self):
        pass

    @property
    @abstractmethod
    def arena_down_move_amount(self):
        pass

    @property
    @abstractmethod
    def arena_down_transition_duration(self):
        pass

    @property
    @abstractmethod
    def grid_topleft(self):
        pass

    @property
    @abstractmethod
    def grid_size(self):
        pass

    @property
    @abstractmethod
    def shooter_position(self):
        pass

    @property
    @abstractmethod
    def next_bubble_position(self):
        pass