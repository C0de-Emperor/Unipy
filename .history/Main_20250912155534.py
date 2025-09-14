from UnipyEngine.Engine import run_game
#from Scripts.player_controller import PlayerController

from UnipyEngine.Core import GameObject, Transform
from UnipyEngine.Rendering import SpriteRenderer
from UnipyEngine.Physics import Rigidbody2D, CircleCollider2D
from UnipyEngine.utils import Vector2, Vector3, Color, DrawingShape, BodyState

# Création d'un objet avec un script custom
player = GameObject([
    Transform(Vector3(100, 100, 0), Vector3(0, 0, 0), Vector2(30, 30)),
    SpriteRenderer(DrawingShape.CIRCLE, Color(0, 255, 0)),
    Rigidbody2D(Vector2(0, 0), BodyState.CYNEMATIC, mass=1),
    CircleCollider2D(15),
    PlayerController()   # <-- script custom ajouté comme un Component
])

run_game()