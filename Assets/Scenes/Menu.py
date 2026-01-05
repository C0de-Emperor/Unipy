from UnipyEngine import *
from UnipyEngine.ModuleManagement import Scene

scene = Scene("Menu")

def load():
        from Assets import S

        ball = GameObject(
        name = "Ball 1",
        tags = [
            "Ball b"
        ],
        components= [
            Transform(Vector3(400, 100, 0), Vector3(0, 0, 0), Vector2(60, 60)),
            SpriteRenderer(DrawingShape.CIRCLE, color=Color(0, 0, 0)), #image=r"Assets\creative_casing.png"
            Rigidbody2D(Vector2(0, 0), BodyState.CYNEMATIC, mass=1),
            CircleCollider2D(30),
            Camera(zoom=1.0),
            S()
        ],
        auto_add = True,
        static=False
    )