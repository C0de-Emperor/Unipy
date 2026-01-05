from enum import Enum


class DrawingShape(Enum):
    SQUARE = 1
    CIRCLE = 2

class BodyState(Enum):
    CYNEMATIC = 1
    KINEMATIC = 2

class Vector2:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return str((self.x, self.y))
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

class Vector3:
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return str((self.x, self.y, self.z))
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

class Color:
    def __init__(self, r:float, g:float, b:float):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self) -> str:
        return str((self.r, self.g, self.b))
    
    def __tuple__(self) -> tuple:
        return (self.r, self.g, self.b)

class Debug:
    def Log(log:str):
        print(f"\033[0m[LOG]\033[0m {log}")

    def LogSuccess(success:str):
        print(f"\033[92m[SUCCESS]\033[0m {success}")

    def LogWarnig(warning:str):
        print(f"\033[93m[WARNING]\033[0m {warning}")
    
    def LogRegistry(log:str):
        print(f"\033[94m[Registry]\033[0m {log}")

    def LogError(error:str, isFatal=False):
        import sys
        print(f"\033[91m[ERROR]\033[0m {error}")
        if isFatal:
            sys.exit(0)