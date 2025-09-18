from UnipyEngine.Core import Component,Transform
from UnipyEngine.Utils import DrawingShape, Color
from UnipyEngine.Engine import Engine
from UnipyEngine.Utils import Debug, Vector2
import pygame
import json
import os

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
                        Engine.screen,
                        (self.color.r, self.color.g, self.color.b),
                        (int(transform.position.x), int(transform.position.y)),
                        int(min(transform.size.x, transform.size.y) / 2)
                    )

class TilemapRenderer(Component):
    def __init__(self, tile_size:Vector2, path:str, tileset=None, gameObject=None):
        super().__init__(gameObject=gameObject)
        self.tile_size = tile_size
        self.tileset = tileset or {}      # dict {tile_id: Color/Sprite}

        self.LoadTilemapFromJSON(path=path)

    def Update(self, dt):
        self.Render()

    def SetTile(self, x:int, y:int, tile_id:int):
        """Place une tuile (tile_id) à la position (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile_id

    def GetTile(self, x:int, y:int):
        return self.grid[y][x]

    def Render(self):
        from UnipyEngine.Engine import Engine
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.grid[y][x]
                if tile_id in self.tileset:
                    color = self.tileset[tile_id]
                    px = self.gameObject.GetComponent(Transform).position.x + x * self.tile_size.x
                    py = self.gameObject.GetComponent(Transform).position.y + y * self.tile_size.y
                    pygame.draw.rect(
                        Engine.screen,
                        (color.r, color.g, color.b),
                        pygame.Rect(px, py, self.tile_size.x, self.tile_size.y)
                    )

    def LoadTilemapFromJSON(self, path:str):
        if not os.path.exists(path):
            Debug.LogError(f"No file at '{path}'", isFatal=True)
            return

        with open(path, "r") as f:
            data = json.load(f)

        if data["fileType"] != "tilemap":
            Debug.LogError(f"The file at '{path}' is not a Tilemap", isFatal=True)
            return
        
        self.width, self.height = data["width"], data["height"]

        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]  # tile IDs
        for y in range(self.height):
            for x in range(self.width):
                tile_id = data["tiles"][y][x]
                self.grid[y][x] = tile_id
                self.SetTile(x, y, tile_id)
