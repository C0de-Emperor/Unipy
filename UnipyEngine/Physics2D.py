import math
import pygame
from typing import Optional

from UnipyEngine.Core import Component, Transform, GameObject
from UnipyEngine.Utils import Vector2, BodyState, Vector3


class RaycastHit2D:
    def __init__(self, collider: "Collider2D", distance: float, normal: Vector2, point: Vector2) -> None:
        self.collider: Collider2D = collider
        self.distance: float = distance
        self.normal: Vector2 = normal
        self.point: Vector2 = point

class Collider2D(Component):
    def __init__(self, local_position: Vector3 = Vector3(0,0,0), gameObject: Optional[GameObject] = None) -> None:
        super().__init__(gameObject=gameObject, requiredComponents=[Transform, Rigidbody2D])
        self.local_position: Vector3 = local_position

    def Intersects(self, other) -> bool:
        """Test de collision avec un autre collider (à spécialiser)."""
        raise NotImplementedError("Chaque collider doit définir Intersects()")

    def IntersectsRay(self, origin: Vector2, direction: Vector2, distance: float) -> Optional[RaycastHit2D]:
        """Test d'intersection avec un rayon (à spécialiser)."""
        raise NotImplementedError("Chaque collider doit définir IntersectsRay()")

class BoxCollider2D(Collider2D):
    def __init__(self, size: Vector2, local_position: Vector3 = Vector3(0,0,0), gameObject: Optional[GameObject] = None) -> None:
        super().__init__(gameObject=gameObject, local_position=local_position)
        self.size: Vector2 = size

    def GetRect(self):
        transform = self.gameObject.GetComponent(Transform)
        if transform:
            world_x = (transform.position.x + self.local_position.x) - self.size.x / 2
            world_y = (transform.position.y + self.local_position.y) - self.size.y / 2
            return pygame.Rect(
                int(world_x),
                int(world_y),
                int(self.size.x),
                int(self.size.y)
            )
        return None

    def Intersects(self, other) -> bool:
        if isinstance(other, BoxCollider2D):
            rect1 = self.GetRect()
            rect2 = other.GetRect()
            return rect1.colliderect(rect2)

        elif isinstance(other, CircleCollider2D):
            return other.Intersects(self)  # délègue au cercle

        return False

    def IntersectsRay(self, origin: Vector2, direction: Vector2, distance: float) -> Optional[RaycastHit2D]:
        rect = self.GetRect()
        if not rect:
            return None

        # Ray vs Axis-Aligned Bounding Box intersection
        min_x = rect.left
        max_x = rect.right
        min_y = rect.top
        max_y = rect.bottom

        # Avoid division by zero
        if direction.x != 0:
            t1 = (min_x - origin.x) / direction.x
            t2 = (max_x - origin.x) / direction.x
        else:
            t1 = float('-inf') if min_x <= origin.x <= max_x else float('inf')
            t2 = t1

        if direction.y != 0:
            t3 = (min_y - origin.y) / direction.y
            t4 = (max_y - origin.y) / direction.y
        else:
            t3 = float('-inf') if min_y <= origin.y <= max_y else float('inf')
            t4 = t3

        t_min = max(min(t1, t2), min(t3, t4))
        t_max = min(max(t1, t2), max(t3, t4))

        if t_max < 0 or t_min > t_max or t_min > distance:
            return None

        t = t_min if t_min >= 0 else t_max
        if t < 0 or t > distance:
            return None

        point = origin + direction * t

        # Determine normal
        epsilon = 1e-6
        if abs(point.x - min_x) < epsilon:
            normal = Vector2(-1, 0)
        elif abs(point.x - max_x) < epsilon:
            normal = Vector2(1, 0)
        elif abs(point.y - min_y) < epsilon:
            normal = Vector2(0, -1)
        elif abs(point.y - max_y) < epsilon:
            normal = Vector2(0, 1)
        else:
            normal = Vector2(0, 0)  # Fallback, shouldn't happen

        return RaycastHit2D(self, t, normal, point)

    def RenderCollider(self, used_screen):
            rect = self.GetRect()
            if not rect:
                return
            # draw in screen space using camera if available
            try:
                from UnipyEngine.Rendering import Camera, Engine
            except Exception:
                Camera = None
                Engine = None

            if used_screen == Engine.static_world_surface:
                # Rendre directement en monde sur la surface statique
                pygame.draw.rect(used_screen, (200, 0, 0), rect, 2)
            elif Camera and Camera.active_camera:
                # world top-left -> screen
                screen_pos = Camera.WorldToScreen(Vector3(rect.x, rect.y, 0))
                sw = int(self.size.x * Camera.active_camera.zoom)
                sh = int(self.size.y * Camera.active_camera.zoom)
                draw_rect = pygame.Rect(int(screen_pos.x), int(screen_pos.y), sw, sh)
                pygame.draw.rect(used_screen, (200, 0, 0), draw_rect, 2)
            else:
                pygame.draw.rect(used_screen, (200, 0, 0), rect, 2)

class CircleCollider2D(Collider2D):
    def __init__(self, radius: float, local_position: Vector3 = Vector3(0,0,0), gameObject: Optional[GameObject] = None) -> None:
        super().__init__(gameObject=gameObject, local_position=local_position)
        self.radius: float = radius

    def GetCircle(self):
        transform = self.gameObject.GetComponent(Transform)
        if transform:
            return (transform.position.x + self.local_position.x, transform.position.y + self.local_position.y, self.radius)
        return None

    def Intersects(self, other) -> bool:
        if isinstance(other, CircleCollider2D):
            # Cercle vs Cercle
            x1, y1, r1 = self.GetCircle()
            x2, y2, r2 = other.GetCircle()
            dist_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
            return dist_sq <= (r1 + r2) ** 2

        elif isinstance(other, BoxCollider2D):
            # Cercle vs Rectangle
            cx, cy, r = self.GetCircle()
            rect = other.GetRect()

            # On trouve le point le plus proche du centre du cercle dans le rectangle
            closest_x = max(rect.left, min(cx, rect.right))
            closest_y = max(rect.top, min(cy, rect.bottom))

            # Distance entre ce point et le centre du cercle
            dist_sq = (cx - closest_x) ** 2 + (cy - closest_y) ** 2
            #print(dist_sq <= r ** 2)
            return dist_sq <= r ** 2

        return False

    def IntersectsRay(self, origin: Vector2, direction: Vector2, distance: float) -> Optional[RaycastHit2D]:
        circle = self.GetCircle()
        if not circle:
            return None

        cx, cy, r = circle
        center = Vector2(cx, cy)

        # Ray vs Circle intersection
        oc = origin - center
        a = direction.dot(direction)  # Should be 1 if normalized
        b = 2 * oc.dot(direction)
        c = oc.dot(oc) - r * r

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None

        sqrt_d = math.sqrt(discriminant)
        t1 = (-b - sqrt_d) / (2 * a)
        t2 = (-b + sqrt_d) / (2 * a)

        # Choose the smallest positive t
        t = min(t1, t2) if t1 >= 0 else t2
        if t < 0 or t > distance:
            return None

        point = origin + direction * t
        normal = (point - center).normalized()

        return RaycastHit2D(self, t, normal, point)

    def RenderCollider(self, used_screen):
        circle = self.GetCircle()
        if circle:
            cx, cy, r = circle
            try:
                from UnipyEngine.Rendering import Camera, Engine
            except Exception:
                Camera = None
                Engine = None

            if used_screen == Engine.static_world_surface:
                # Rendre directement en monde
                pygame.draw.circle(used_screen, (200, 0, 0), (int(cx), int(cy)), int(r), 2)
            elif Camera and Camera.active_camera:
                screen_center = Camera.WorldToScreen(Vector3(cx, cy, 0))
                rr = int(r * Camera.active_camera.zoom)
                pygame.draw.circle(used_screen, (200, 0, 0), (int(screen_center.x), int(screen_center.y)), rr, 2)
            else:
                pygame.draw.circle(used_screen, (200, 0, 0), (int(cx), int(cy)), int(r), 2)

class TilemapCollider2D(Collider2D):
    def __init__(self, solid_tiles: list[str], gameObject: Optional[GameObject] = None) -> None:
        super().__init__(gameObject=gameObject)
        #self.tilemap = self.gameObject.GetComponent(Tile)
        self.solid_tiles: set = set(solid_tiles)  # plus rapide en set
        self.colliders: list = []  # liste de colliders internes

    def Start(self):
        """Génère les colliders au lancement."""
        self.GenerateColliders()

    def GenerateColliders(self):
        from UnipyEngine.Rendering import TilemapRenderer

        self.colliders.clear()
        tilemap = self.gameObject.GetComponent(TilemapRenderer)
        t = tilemap.tile_size
        for y in range(tilemap.height):
            for x in range(tilemap.width):
                tile_id = tilemap.grid[y][x]
                if tile_id in self.solid_tiles:
                    pos = Vector3(
                        x * t.x + t.x / 2,
                        y * t.y + t.y / 2,
                        0
                    )
                    collider = BoxCollider2D(Vector2(t.x, t.y), local_position=pos, gameObject=self.gameObject)
                    self.colliders.append(collider)

    def Intersects(self, other: "Collider2D") -> bool:
        for col in self.colliders:
            if col.Intersects(other):
                return True
        return False

    def GetColliders(self):
        return self.colliders

    def RenderCollider(self, used_screen):
        for col in self.colliders:
            if hasattr(col, "RenderCollider") and callable(col.RenderCollider):
                col.RenderCollider(used_screen)

    def IntersectsRay(self, origin: Vector2, direction: Vector2, distance: float) -> Optional[RaycastHit2D]:
        closest_hit = None
        closest_dist = distance
        for tile in self.colliders:
            hit = tile.IntersectsRay(origin, direction, distance)
            if hit and hit.distance < closest_dist:
                closest_dist = hit.distance
                closest_hit = hit
        return closest_hit

class Rigidbody2D(Component):

    GRAVITY = Vector2(0, 9.8)
    collisions_handled_this_frame = set()  # static -> partagé par tous les Rigidbody2D

    def __init__(self, initialVelocity: Vector2, bodyType: BodyState, mass: float = 1.0, gravityScale: float = 5.0, bounciness: float = 0.5, gameObject: Optional[GameObject] = None) -> None:

        super().__init__(gameObject=gameObject, requiredComponents=[Transform])

        self.velocity: Vector2 = initialVelocity
        self.mass: float = float(mass)
        self.gravityScale: float = float(gravityScale)
        self.bounciness: float = float(bounciness)
        self.forces: Vector2 = Vector2.zero()

        self.bodyType: BodyState = bodyType

        self.current_collisions: set = set()  # collisions de cette frame
        self.previous_collisions: set = set() # collisions de la frame précédente

    def AddForce(self, force: Vector2):
        self.forces.x += force.x
        self.forces.y += force.y

    def Update(self, dt):
        transform = self.gameObject.GetComponent(Transform)
        collider = self.gameObject.GetComponent(Collider2D)

        if(self.bodyType == BodyState.CYNEMATIC):
            # 1. appliquer gravité + forces
            gravity_force = Vector2(
                Rigidbody2D.GRAVITY.x * self.mass * self.gravityScale,
                Rigidbody2D.GRAVITY.y * self.mass * self.gravityScale
            )
            self.AddForce(gravity_force)

        ax = self.forces.x / self.mass
        ay = self.forces.y / self.mass

        self.velocity.x += ax * dt
        self.velocity.y += ay * dt

        transform.position.x += self.velocity.x * dt
        transform.position.y += self.velocity.y * dt

        # --- Gestion collisions ---
        self.current_collisions.clear()
        if collider:
            for other in GameObject.instances:
                if other is self.gameObject:
                    continue
                other_collider = other.GetComponent(Collider2D)
                if not other_collider:
                    continue

                # clé unique pour la paire
                pair = tuple(sorted([id(self.gameObject), id(other)]))
                if pair in Rigidbody2D.collisions_handled_this_frame:
                    continue  # déjà traité cette frame

                if isinstance(other_collider, TilemapCollider2D):
                    for tile_col in other_collider.GetColliders():
                        if collider.Intersects(tile_col):
                            self.ResolveCollision(collider, tile_col)
                            self.current_collisions.add(other)
                            Rigidbody2D.collisions_handled_this_frame.add(pair)
                else:
                    if collider.Intersects(other_collider):
                        self.ResolveCollision(collider, other_collider)
                        self.current_collisions.add(other)
                        Rigidbody2D.collisions_handled_this_frame.add(pair)

        # 3. Callbacks OnCollisionEnter
        for other in self.current_collisions - self.previous_collisions:
            for comp in self.gameObject.components:
                if hasattr(comp, "OnCollisionEnter"):
                    comp.OnCollisionEnter(other.GetComponent(Collider2D))
            for comp in other.components:
                if hasattr(comp, "OnCollisionEnter"):
                    comp.OnCollisionEnter(self.gameObject.GetComponent(Collider2D))

        # 4. Callbacks OnCollisionExit
        for other in self.previous_collisions - self.current_collisions:
            for comp in self.gameObject.components:
                if hasattr(comp, "OnCollisionExit"):
                    comp.OnCollisionExit(other.GetComponent(Collider2D))
            for comp in other.components:
                if hasattr(comp, "OnCollisionExit"):
                    comp.OnCollisionExit(self.gameObject.GetComponent(Collider2D))

        # 5. Reset forces et swap collisions
        self.forces = Vector2(0, 0)
        self.previous_collisions = set(self.current_collisions)
        
    def ResolveCollision(self, col1, col2):
        transform = self.gameObject.GetComponent(Transform)

        # Si le corps est kinematic, on ne bouge pas ni ne change la vitesse
        if self.bodyType == BodyState.KINEMATIC:  
            return

        # ------------------------
        # 1. Box vs Box
        # ------------------------
        if isinstance(col1, BoxCollider2D) and isinstance(col2, BoxCollider2D):
            rect1 = col1.GetRect()
            rect2 = col2.GetRect()
            if rect1 and rect2 and rect1.colliderect(rect2):
                dx = min(rect1.right - rect2.left, rect2.right - rect1.left)
                dy = min(rect1.bottom - rect2.top, rect2.bottom - rect1.top)

                if dx < dy:
                    if rect1.centerx < rect2.centerx:
                        transform.position.x -= dx
                    else:
                        transform.position.x += dx
                    self.velocity.x *= -self.bounciness
                else:
                    if rect1.centery < rect2.centery:
                        transform.position.y -= dy
                    else:
                        transform.position.y += dy
                    self.velocity.y *= -self.bounciness

        # ------------------------
        # 2. Circle vs Circle
        # ------------------------
        elif isinstance(col1, CircleCollider2D) and isinstance(col2, CircleCollider2D):
            x1, y1, r1 = col1.GetCircle()
            x2, y2, r2 = col2.GetCircle()

            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < r1 + r2 and dist > 0:  # collision
                overlap = (r1 + r2) - dist
                nx = dx / dist
                ny = dy / dist

                # repousser le premier cercle
                transform.position.x -= nx * overlap
                transform.position.y -= ny * overlap

                # inverser la vitesse le long de la normale
                vn = self.velocity.x * nx + self.velocity.y * ny
                self.velocity.x -= 2 * vn * nx * self.bounciness
                self.velocity.y -= 2 * vn * ny * self.bounciness

        # ------------------------
        # 3. Circle vs Box
        # ------------------------
        elif isinstance(col1, CircleCollider2D) and isinstance(col2, BoxCollider2D):
            cx, cy, r = col1.GetCircle()
            rect = col2.GetRect()

            # point le plus proche du centre du cercle
            closest_x = max(rect.left, min(cx, rect.right))
            closest_y = max(rect.top, min(cy, rect.bottom))

            dx = cx - closest_x
            dy = cy - closest_y
            dist_sq = dx*dx + dy*dy

            if dist_sq < r*r:  # collision
                dist = math.sqrt(dist_sq)
                if dist == 0:
                    # centre exactement sur le coin : choisir la direction selon la vitesse
                    vx, vy = self.velocity.x, self.velocity.y
                    if abs(vx) > abs(vy):
                        nx, ny = 1 if vx < 0 else -1, 0
                    else:
                        nx, ny = 0, 1 if vy < 0 else -1
                    overlap = r
                else:
                    nx = dx / dist
                    ny = dy / dist
                    overlap = r - dist

                # Correction position
                transform.position.x += nx * overlap
                transform.position.y += ny * overlap

                # Rebond uniquement si on va vers la surface
                vn = self.velocity.x * nx + self.velocity.y * ny
                if vn < 0:
                    self.velocity.x -= (1 + self.bounciness) * vn * nx
                    self.velocity.y -= (1 + self.bounciness) * vn * ny

        # (symétrique : Box vs Circle → on délègue au code Circle vs Box)
        elif isinstance(col1, BoxCollider2D) and isinstance(col2, CircleCollider2D):
            self.ResolveCollision(col2, col1)

    @staticmethod
    def ClearFrameCollisions():
        """À appeler au début de chaque frame (avant tous les Updates)."""
        Rigidbody2D.collisions_handled_this_frame.clear()

class Raycast:
    def __init__(self, origin: Vector2, direction: Vector2, distance: float) -> Optional[RaycastHit2D]:
        self.origin: Vector2 = Vector2(origin)
        self.direction: Vector2 = direction.normalized()
        self.distance: float = distance
        self.hit: Optional[RaycastHit2D] = self._perform_raycast()

    def _perform_raycast(self) -> Optional[RaycastHit2D]:
        closest_hit = None
        closest_dist = self.distance

        for obj in GameObject.instances:
            collider = obj.GetComponent(Collider2D)
            if not collider:
                continue

            hit = collider.IntersectsRay(self.origin, self.direction, self.distance)
            if hit and hit.distance < closest_dist:
                closest_dist = hit.distance
                closest_hit = hit

        return closest_hit
