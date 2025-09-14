
from UnipyEngine.Core import Component, Transform, GameObject
from UnipyEngine.Utils import Vector2
import math
import pygame

class Collider2D(Component):
    def __init__(self, gameObject=None):
        super().__init__(gameObject=gameObject, requiredComponents=[Transform, Rigidbody2D])

    def Intersects(self, other) -> bool:
        """Test de collision avec un autre collider (à spécialiser)."""
        raise NotImplementedError("Chaque collider doit définir Intersects()")

class BoxCollider2D(Collider2D):
    def __init__(self, size:Vector2, gameObject=None):
        super().__init__(gameObject)
        self.size = size

    def GetRect(self):
        transform = self.gameObject.GetComponent(Transform)
        if transform:
            return pygame.Rect(
                int(transform.position.x - self.size.x / 2),
                int(transform.position.y - self.size.y / 2),
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

class CircleCollider2D(Collider2D):
    def __init__(self, radius:float, gameObject=None):
        super().__init__(gameObject)
        self.radius = radius

    def GetCircle(self):
        transform = self.gameObject.GetComponent(Transform)
        if transform:
            return (transform.position.x, transform.position.y, self.radius)
        return None

    def Intersects(self, other) -> bool:
        if isinstance(other, CircleCollider2D):
            print("e")
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
            return dist_sq <= r ** 2

        return False

class Rigidbody2D(Component):
    GRAVITY = Vector2(0, 9.8)

    def __init__(self, initialVelocity, bodyType, mass=1.0, gravityScale=5.0, bounciness=0.5, gameObject=None):
        assert isinstance(initialVelocity, Vector2)
        assert isinstance(mass, (int, float)) and mass > 0
        assert isinstance(gravityScale, (int, float))
        assert isinstance(bounciness, (int, float))
        assert isinstance(bodyType, BodyState)

        super().__init__(gameObject=gameObject, requiredComponents=[Transform])
        self.velocity = initialVelocity
        self.bodyType = bodyType
        self.mass = float(mass)
        self.gravityScale = gravityScale
        self.bounciness = bounciness
        self.forces = Vector2(0, 0)

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

        # 2. collisions (seulement si on a un collider)
        if collider:
            for other in GameObject.instances:
                if other is self.gameObject:
                    continue
                other_collider = other.GetComponent(Collider2D)
                if not other_collider:
                    continue

                if collider.Intersects(other_collider):
                    self.ResolveCollision(collider, other_collider)

        # reset forces
        self.forces = Vector2(0, 0)

    def ResolveCollision(self, col1, col2):
        transform = self.gameObject.GetComponent(Transform)

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
