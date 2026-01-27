from enum import Enum
import math
from typing import Optional, Union

class DrawingShape(Enum):
    SQUARE = 1
    CIRCLE = 2

class BodyState(Enum):
    CYNEMATIC = 1
    KINEMATIC = 2

class Vector2:
    def __init__(self, x: Union[float, "Vector3"] = 0.0, y=None):
        # Vector2(x, y)
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.x: float = float(x)
            self.y: float = float(y)

        # Vector2(Vector3)
        elif y is None and type(x) == Vector3:
            self.x: float = float(x.x)
            self.y: float = float(x.y)

        else:
            Debug.LogError("Vector2 expects (x:float, y:float) or (vector:Vector3)", isFatal=True)

    # ---------- Représentation ----------
    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    # ---------- Opérateurs ----------
    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, value: float) -> "Vector2":
        return Vector2(self.x * value, self.y * value)

    def __rmul__(self, value: float) -> "Vector2":
        return self.__mul__(value)

    def __truediv__(self, value: float) -> "Vector2":
        return Vector2(self.x / value, self.y / value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vector2) and self.x == other.x and self.y == other.y

    # ---------- Maths ----------
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def sqr_magnitude(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalized(self) -> "Vector2":
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)

    def dot(self, other: "Vector2") -> float:
        return self.x * other.x + self.y * other.y

    # ---------- Constantes (Unity-like) ----------
    @staticmethod
    def zero() -> "Vector2":
        return Vector2(0, 0)

    @staticmethod
    def up() -> "Vector2":
        return Vector2(0, -1)

    @staticmethod
    def down() -> "Vector2":
        return Vector2(0, 1)

    @staticmethod
    def left() -> "Vector2":
        return Vector2(-1, 0)

    @staticmethod
    def right() -> "Vector2":
        return Vector2(1, 0)

class Vector3:
    def __init__(self, x:float, y:float, z:float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __str__(self) -> str:
        return str((self.x, self.y, self.z))
    
    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vector3) and (self.x == other.x and self.y == other.y and self.z == other.z)

class Color:
    def __init__(self, r:float, g:float, b:float):
        self.r = r
        self.g = g
        self.b = b

        self

    def __str__(self) -> str:
        return str((self.r, self.g, self.b))
    
    def __iter__(self) -> iter:
        return iter((self.r, self.g, self.b))
    
class Debug:
    def Log(log: str) -> None:
        print(f"\033[0m[LOG]\033[0m {log}")

    def LogSuccess(success: str) -> None:
        print(f"\033[92m[SUCCESS]\033[0m {success}")

    def LogWarning(warning: str) -> None:
        print(f"\033[93m[WARNING]\033[0m {warning}")
    
    def LogRegistry(log: str) -> None:
        print(f"\033[94m[Registry]\033[0m {log}")

    def LogError(error: str, isFatal: bool = False) -> None:
        import sys
        print(f"\033[91m[ERROR]\033[0m {error}")
        if isFatal:
            sys.exit(0)