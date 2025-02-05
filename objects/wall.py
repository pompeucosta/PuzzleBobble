import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self,pos: pygame.Vector2,scale: pygame.Vector2 = None,image = None) -> None:
        super().__init__()
        
        if image == None:
            self.image = pygame.Surface((scale.x,scale.y),pygame.SRCALPHA)
            
            pygame.draw.rect(self.image,(0,255,0),pygame.Rect(0,0,scale.x,scale.y))
        else:
            self.image = image

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos.x,pos.y)