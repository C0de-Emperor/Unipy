from UnipyEngine.Core import Component,Transform
from UnipyEngine.Utils import DrawingShape, Color
from UnipyEngine.Engine import Engine
import pygame

class SpriteRenderer(Component):
    def __init__(self, shape:DrawingShape, color:Color, gameObject = None):
        assert isinstance(shape, DrawingShape)
        assert isinstance(color, Color)

        super().__init__(gameObject=gameObject, requiredComponents=[Transform])
        self.drawShape = shape
        self.color = color

    def Update(self, dt):
        # On récupère le Transform depuis le GameObject parent
        transform = self.gameObject.GetComponent(Transform)
        if transform:
            match self.drawShape:
                case DrawingShape.SQUARE:
                    pygame.draw.rect(
                        Engine.screen,
                        (self.color.r, self.color.g, self.color.b),
                        pygame.Rect(
                            transform.position.x - transform.size.x/2,
                            transform.position.y - transform.size.y/2,
                            transform.size.x,
                            transform.size.y
                        )
                    )
                case DrawingShape.CIRCLE:
                    pygame.draw.circle(
                        screen,
                        (self.color.r, self.color.g, self.color.b),
                        (int(transform.position.x), int(transform.position.y)),
                        int(min(transform.size.x, transform.size.y) / 2)
                    )
