from UnipyEngine.Core import Component,Transform
from UnipyEngine.Utils import DrawingShape, Color
from UnipyEngine.Engine import Engine
from UnipyEngine.Utils import Debug, Vector2
import pygame
import json
import os

class SpriteRenderer(Component):
    def __init__(self, shape:DrawingShape=None, color:Color=None, image=None, gameObject=None):
        """
        - shape + color -> rend une forme simple (cercle ou carré).
        - image (str ou pygame.Surface) -> rend une texture PNG.
        """
        super().__init__(gameObject=gameObject, requiredComponents=[Transform])

        self.drawShape = shape
        self.color = color
        self.sprite = None  # surface pygame si image chargée

        if image:
            if isinstance(image, str):
                if not os.path.exists(image):
                    Debug.LogError(f"Image not found: {image}", isFatal=True)
                else:
                    img = pygame.image.load(image).convert_alpha()
                    self.sprite = img
            elif isinstance(image, pygame.Surface):
                self.sprite = image
            else:
                Debug.LogError(f"Unsupported image type: {type(image)}", isFatal=True)

    def Render(self, used_screen):
        transform = self.gameObject.GetComponent(Transform)
        if not transform:
            return

        if self.sprite:
            # Redimensionner sprite selon transform.size
            scaled = pygame.transform.scale(
                self.sprite,
                (int(transform.size.x), int(transform.size.y))
            )
            # On blitte en centrant (comme circle/rect)
            pos = (transform.position.x - transform.size.x/2,
                   transform.position.y - transform.size.y/2)
            used_screen.blit(scaled, pos)

        elif self.drawShape and self.color:
            match self.drawShape:
                case DrawingShape.SQUARE:
                    pygame.draw.rect(
                        used_screen,
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
                        used_screen,
                        (self.color.r, self.color.g, self.color.b),
                        (int(transform.position.x), int(transform.position.y)),
                        int(min(transform.size.x, transform.size.y) / 2)
                    )


class TilemapRenderer(Component):
    default_tile_path = r"UnipyEngine\default_texture.png"

    def __init__(self, tile_size:Vector2, path:str, tileset:dict=None, gameObject=None):
        super().__init__(gameObject=gameObject)
        self.tile_size = tile_size
        self.tileset = tileset or {}      # dict {tile_id: Color/Sprite}

        if "0" in tileset.keys():
            Debug.LogError("The key 0 is only for empty tile in tileset", isFatal=True)

        for tile_id, value in tileset.items():
            if isinstance(value, str):  
                # Charger une image depuis un chemin
                if not os.path.exists(value):
                    Debug.LogError(f"No file at '{value}'", isFatal=True)
                    return

                try:
                    img = pygame.image.load(value).convert_alpha()
                    img = pygame.transform.scale(img, (int(tile_size.x), int(tile_size.y)))
                    self.tileset[tile_id] = img
                except:
                    Debug.LogError(f"Exception during import of the file : '{value}'", isFatal=True)
                    return
            elif isinstance(value, Color):  
                # Créer une Surface unie avec la couleur
                surf = pygame.Surface((int(tile_size.x), int(tile_size.y)), pygame.SRCALPHA)
                surf.fill((value.r, value.g, value.b))
                self.tileset[tile_id] = surf
            elif isinstance(value, pygame.Surface):
                # Déjà une surface → on s'assure qu'elle est à la bonne taille
                self.tileset[tile_id] = pygame.transform.scale(value, (int(tile_size.x), int(tile_size.y)))
            else:
                Debug.LogError(f"Unsupported tileset value for tile_id {tile_id}: {type(value)}", True)
                return


        img = pygame.image.load(TilemapRenderer.default_tile_path).convert_alpha()
        img = pygame.transform.scale(img, (int(tile_size.x), int(tile_size.y)))
        self.default_tile = img


        self.LoadTilemapFromJSON(path=path)

    def SetTile(self, x:int, y:int, tile_id:int):
        """Place une tuile (tile_id) à la position (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile_id

    def GetTile(self, x:int, y:int):
        return self.grid[y][x]

    def Render(self, used_screen):
        t = self.gameObject.GetComponent(Transform)
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.grid[y][x]

                if tile_id == "0":
                    continue

                px = t.position.x + x * self.tile_size.x
                py = t.position.y + y * self.tile_size.y

                surf = self.tileset.get(tile_id, self.default_tile)
                used_screen.blit(surf, (px, py))

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

class SpriteSheet:
    def __init__(self, path:str, tile_size:Vector2):
        if not os.path.exists(path):
            Debug.LogError(f"No file at '{path}'", isFatal=True)
            return

        self.sheet = pygame.image.load(path).convert_alpha()
        self.tile_size = tile_size
        self.cols = self.sheet.get_width() // int(tile_size.x)
        self.rows = self.sheet.get_height() // int(tile_size.y)

    def GetTile(self, col: int, row: int) -> pygame.Surface:
        """Récupère une tile par coordonnées (col, row)."""
        try :
            rect = pygame.Rect(
                col * self.tile_size.x,
                row * self.tile_size.y,
                self.tile_size.x,
                self.tile_size.y
            )
            return self.sheet.subsurface(rect).copy()
        except ValueError as e:
            Debug.LogError(e, True)

    def GetTileById(self, tile_id: int) -> pygame.Surface:
        """Récupère une tile par index linéaire (0,1,2... en parcourant ligne par ligne)."""
        col = tile_id % self.cols
        row = tile_id // self.cols
        return self.GetTile(col, row)

    def ToDict(self, mapping: dict) -> dict:
        """Construit un dict {tile_id: Surface} pour un Tilemap."""
        return {tile_id: self.GetTile(col, row) for tile_id, (col, row) in mapping.items()}
