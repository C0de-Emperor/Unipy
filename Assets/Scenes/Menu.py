from UnipyEngine import *
from UnipyEngine.ModuleManagement import Scene


def load():
    from Assets import S

    GameObject(
        name = "Ball 1",
        tags = [
            "Ball b"
        ],
        components= [
            Transform(Vector3(400, 100, 0), Vector3(0, 0, 0), Vector2(60, 60)),
            SpriteRenderer(DrawingShape.CIRCLE, color=Color(0, 0, 0)), #image=r"Assets\creative_casing.png"
            Rigidbody2D(Vector2(0, 0), BodyState.CYNEMATIC, mass=1),
            CircleCollider2D(30),
            S()
        ],
        auto_add = True,
        static=False
    )

    GameObject(
        name = "Camera",
        tags = [],
        components= [
            Transform(Vector3(400, 100, 0), Vector3(0, 0, 0), Vector2(60, 60)),
            Camera(zoom=1.0, bakgroundColor = Color(54, 215, 247))
        ],
        auto_add = True,
        static=True
    )



file_Type = Scene("Menu", load)