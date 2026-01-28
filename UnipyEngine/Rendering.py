from UnipyEngine.Core import Component, Transform, GameObject
from UnipyEngine.Utils import DrawingShape, Color
from UnipyEngine.Engine import Engine
from UnipyEngine.Utils import Debug, Vector2, Vector3
from typing import Union, Optional, Dict
import pygame
import json
import os

class SpriteRenderer(Component):
    def __init__(self, shape: Optional[DrawingShape] = None, color: Optional[Color] = None, image: Optional[Union[str, pygame.Surface]] = None, gameObject: Optional[GameObject] = None) -> None:
        """
        - shape + color -> rend une forme simple (cercle ou carré).
        - image (str ou pygame.Surface) -> rend une texture PNG.
        """
        super().__init__(gameObject=gameObject, requiredComponents=[Transform])

        self.drawShape: Optional[DrawingShape] = shape
        self.color: Color = color if color else Color(0, 0, 0)

        if image:
            if isinstance(image, str):
                if not os.path.exists(image):
                    Debug.LogError(f"Image not found: {image}", isFatal=True)
                else:
                    img = pygame.image.load(image).convert_alpha()
                    self.sprite: pygame.Surface = img
            elif isinstance(image, pygame.Surface):
                self.sprite: pygame.Surface = image
            else:
                Debug.LogError(f"Unsupported image type: {type(image)}", isFatal=True)

    def Render(self, used_screen):
        transform = self.gameObject.transform
        if not transform:
            return
        # On prépare une surface temporaire et on utilise Camera.ApplyToSurface
        if hasattr(self, 'sprite') and self.sprite:
            surf = pygame.transform.scale(self.sprite, (int(transform.size.x), int(transform.size.y)))
            # world position : on passe le coin top-left (comme pour tiles)
            world_pos = Vector3(transform.position.x - transform.size.x/2,
                                transform.position.y - transform.size.y/2, 0)
            if used_screen == Engine.static_world_surface:
                # Rendre directement en monde sur la surface statique
                used_screen.blit(surf, (world_pos.x, world_pos.y))
            else:
                scaled, pos = Camera.ApplyToSurface(surf, world_pos, transform.size)
                used_screen.blit(scaled, pos)

        elif self.drawShape and self.color:
            # dessiner la forme sur une surface puis appliquer la caméra
            w = int(transform.size.x)
            h = int(transform.size.y)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            if self.drawShape == DrawingShape.SQUARE:
                pygame.draw.rect(surf, (self.color.r, self.color.g, self.color.b), pygame.Rect(0, 0, w, h))
            elif self.drawShape == DrawingShape.CIRCLE:
                pygame.draw.circle(surf, (self.color.r, self.color.g, self.color.b), (w//2, h//2), int(min(w, h)/2))

            world_pos = Vector3(transform.position.x - transform.size.x/2,
                                transform.position.y - transform.size.y/2, 0)
            if used_screen == Engine.static_world_surface:
                used_screen.blit(surf, (world_pos.x, world_pos.y))
            else:
                scaled, pos = Camera.ApplyToSurface(surf, world_pos, transform.size)
                used_screen.blit(scaled, pos)

class TilemapRenderer(Component):
    default_tile_path = r"UnipyEngine\default_texture.png"

    def __init__(self, tile_size: Vector2, path: str, tileset: Optional[Dict[str, pygame.Surface]] = None, gameObject: Optional[GameObject] = None) -> None:
        super().__init__(gameObject=gameObject, requiredComponents=[Transform])
        self.tile_size: Vector2 = tile_size
        self.tileset: Dict[str, pygame.Surface] = tileset or {}      # dict {tile_id: Color/Sprite}

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

    def SetTile(self, x: int, y: int, tile_id: int) -> None:
        """Place une tuile (tile_id) à la position (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile_id

    def GetTile(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def Render(self, used_screen):
        t = self.gameObject.transform
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.grid[y][x]

                if tile_id == "0":
                    continue

                px = t.position.x + x * self.tile_size.x
                py = t.position.y + y * self.tile_size.y

                surf = self.tileset.get(tile_id, self.default_tile)
                if surf == self.default_tile:
                    Debug.LogWarning(f"Unknown tile key [{tile_id}]")

                if used_screen == Engine.static_world_surface:
                    # Rendre directement en monde
                    used_screen.blit(surf, (px, py))
                else:
                    scaled, pos = Camera.ApplyToSurface(surf, Vector3(px, py, 0), self.tile_size)
                    used_screen.blit(scaled, pos)

    def LoadTilemapFromJSON(self, path: str) -> None:
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
    def __init__(self, path: str, tile_size: Vector2) -> None:
        if not os.path.exists(path):
            Debug.LogError(f"No file at '{path}'", isFatal=True)
            return

        self.sheet: pygame.Surface = pygame.image.load(path).convert_alpha()
        self.tile_size: Vector2 = tile_size
        self.cols: int = self.sheet.get_width() // int(tile_size.x)
        self.rows: int = self.sheet.get_height() // int(tile_size.y)

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

class Camera(Component):
    active_camera = None  # statique : une caméra active à la fois

    def __init__(self, zoom: float = 1.0, gameObject: Optional[GameObject] = None, bakgroundColor: Color = Color(0, 50, 150)) -> None:
        super().__init__(gameObject=gameObject, requiredComponents=[Transform])
        self.zoom: float = zoom
        self.target: GameObject = None
        self.offset: Vector2 = Vector2(0, 0)
        self.bakgroundColor: Color = bakgroundColor

        self.SetActive()


    def Follow(self, target_obj: GameObject, offset: Vector2 = None) -> None:
        """Fait suivre la caméra à une GameObject (centre la caméra dessus).
        `target_obj` doit être une instance de GameObject.
        `offset` est appliqué en pixels (monde) après centrage.
        """
        self.target = target_obj
        if offset is not None:
            self.offset = offset

    def Update(self, dt: float) -> None:
        # Si on suit une cible, positionner la transform de la caméra
        if not self.target:
            return

        cam_tr = self.gameObject.transform
        target_tr = self.target.transform
        if not cam_tr or not target_tr:
            return

        # Avec l'origine centrée, pour centrer la cible au centre de l'écran,
        # la caméra doit être à la position de la cible (plus offset)
        cam_tr.position.x = target_tr.position.x + self.offset.x
        cam_tr.position.y = target_tr.position.y + self.offset.y

    def SetActive(self) -> None:
        Camera.active_camera = self
        Engine.screen.fill(tuple(self.bakgroundColor))

    @staticmethod
    def WorldToScreen(pos: Vector3) -> Vector2:
        if not Camera.active_camera:
            return Vector2(pos.x, pos.y)

        cam_tr = Camera.active_camera.gameObject.transform
        if not cam_tr:
            return Vector2(pos.x, pos.y)

        # Récupérer taille écran pour centrer l'origine (0,0) monde au centre écran
        if Engine.screen is None:
            return Vector2(pos.x, pos.y)
        w, h = Engine.screen.get_size()

        # Variante "top-left" (origine écran = 0,0)
        screen_x = (pos.x - cam_tr.position.x) * Camera.active_camera.zoom + w / 2
        screen_y = (pos.y - cam_tr.position.y) * Camera.active_camera.zoom + h / 2
        return Vector2(screen_x, screen_y)

    @staticmethod
    def ApplyToSurface(surface: pygame.Surface, world_pos: Vector3, size: Vector2) -> tuple:
        """Applique la caméra lors du rendu d’une surface (sprite, tile, etc.)."""
        if not Camera.active_camera:
            Debug.LogError("No Active Camera", True)
            return

        # Calcul position écran
        screen_pos = Camera.WorldToScreen(world_pos)
        # Appliquer zoom
        scaled = pygame.transform.scale(surface, (int(size.x * Camera.active_camera.zoom),
                                                  int(size.y * Camera.active_camera.zoom)))
        # Centrer
        #draw_pos = (screen_pos.x - scaled.get_width() // 2, screen_pos.y - scaled.get_height() // 2)
        draw_pos = (screen_pos.x, screen_pos.y)

        return scaled, draw_pos