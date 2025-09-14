



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