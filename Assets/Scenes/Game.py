from UnipyEngine import *
from UnipyEngine.ModuleManagement import Scene


def load():
    from Assets import S
    GameObject(
        name = "Ball 1",
        layer = LayerMask.NameToLayer("Player"),
        tags = [
            "Ball b"
        ],
        transform = Transform(Vector3(400, 100, 0), Vector3(0, 0, 0), Vector2(60, 60)),
        components= [
            SpriteRenderer(DrawingShape.CIRCLE, color=Color(0, 0, 0)), #image=r"Assets\creative_casing.png"
            Rigidbody2D(Vector2(0, 0), BodyState.CYNEMATIC, mass=1, bounciness=0.9),
            CircleCollider2D(30),
            Camera(zoom=1.0, bakgroundColor = Color(54, 215, 247)),
            S()
        ],
        auto_add = True,
        static=False
    )

    terrain_sheet = SpriteSheet(r"Assets\terrain_sprite_sheet.png", Vector2(16, 16))

    tileset = {
        #"0" : r"Assets\creative_casing.png",
        "1" : terrain_sheet.GetTile(6, 0),
        "2" : terrain_sheet.GetTile(7, 0),
        "3" : terrain_sheet.GetTile(8, 0),
        "4" : terrain_sheet.GetTile(6, 1),
        "5" : terrain_sheet.GetTile(8, 1),
        "6" : terrain_sheet.GetTile(7, 1)
    }

    GameObject(
        name = "Tilemap",
        layer = 0,
        tags = [],
        transform = Transform(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector2(0, 0)),
        components = [
            TilemapRenderer(Vector2(75, 75), r"Assets\Tilemap.json", tileset=tileset),
            TilemapCollider2D(["1", "2", "3"]),
            Rigidbody2D(Vector2(0, 0), BodyState.KINEMATIC)
        ],
        auto_add = True,
        static=True
    )


file_Type = Scene("Game", load)