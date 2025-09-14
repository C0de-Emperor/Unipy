from UnipyEngine.Engine import run_game
#from Scripts.player_controller import PlayerController

from UnipyEngine.Core import GameObject, Transform
from UnipyEngine.Rendering import SpriteRenderer
from UnipyEngine.Physics import Rigidbody2D, CircleCollider2D, BoxCollider2D
from UnipyEngine.Utils import Vector2, Vector3, Color, DrawingShape, BodyState

# Création d'un objet avec un script custom
player = GameObject([
    Transform(Vector3(100, 100, 0), Vector3(0, 0, 0), Vector2(30, 30)),
    SpriteRenderer(DrawingShape.CIRCLE, Color(0, 255, 0)),
    Rigidbody2D(Vector2(0, 0), BodyState.CYNEMATIC, mass=1),
    CircleCollider2D(15),
    #PlayerController()   # <-- script custom ajouté comme un Component
])

gm1 = GameObject([
        Transform(Vector3(110, 40, 0), Vector3(0, 0, 0), Vector2(30, 30)),
        SpriteRenderer(DrawingShape.CIRCLE, Color(20, 140, 30)),
        Rigidbody2D(Vector2(5, 0), BodyState.CYNEMATIC , mass=2),
        CircleCollider2D(15)
    ])

gm2 = GameObject([
        Transform(Vector3(110, 440, 0), Vector3(0, 0, 0), Vector2(100, 100)),
        SpriteRenderer(DrawingShape.SQUARE, Color(200, 200, 30)),
        Rigidbody2D(Vector2(0, -10), BodyState.KYNEMATIC , mass=2),
        BoxCollider2D(Vector2(100, 100))
    ])

run_game()