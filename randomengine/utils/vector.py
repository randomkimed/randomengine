# randomengine.core > vector

from randomengine.core.mathf import Mathf

class Vector2:
    """randomengine.math.vector2"""

    def __init__(self, x, y = None):
        self.x, self.y = x, y if y is not None else x

    ZERO = ...
    ONE = ...

    LEFT = ...
    RIGHT = ...

    UP = ...
    DOWN = ...

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def __add__(self, o):
        o = toVector2(o)
        return Vector2(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        o = toVector2(o)
        return Vector2(self.x - o.x, self.y - o.y)

    def __mul__(self, o):
        o = toVector2(o)
        return Vector2(self.x * o.x, self.y * o.y)

    def __rmul__(self, o):
        o = toVector2(o)
        self * o

    def __truediv__(self, o):
        o = toVector2(o)
        if o.magnitude is 0: return Vector2.ZERO
        else:
            return Vector2(self.x / o.x, self.y / o.y)

    def __eq__(self, o) -> bool:
        o = toVector2(o)
        return self.x == o.x and self.y == o.y
    
    @property
    def sqrMagnitude(self) -> float:
        return self.x ** 2 + self.y ** 2
    
    @property
    def magnitude(self) -> float:
        return Mathf.sqrt(self.sqrMagnitude)
    
    @property
    def normalized(self):
        return self / Vector2(self.magnitude)
    
    def normalize(self):
        return self.normalized
    
    @staticmethod
    def lerp(a, b, t: float, clamp = True):
        a = toVector2(a)
        b = toVector2(b)
        if clamp:
            return Vector2(
                Mathf.lerp(a.x, b.x, t),
                Mathf.lerp(a.y, b.y, t)
            )
        else:
            return Vector2(
                Mathf.lerp_unclamped(a.x, b.x, t),
                Mathf.lerp_unclamped(a.y, b.y, t)
            )

    def lerpTo(self, b, t: float, clamp = True):
        v = Vector2.lerp(self, b, t, clamp)
        self.x, self.y = v.x, v.y
        

def toVector2(x) -> Vector2:
    if isinstance(x, Vector2):
        return x
    elif isinstance(x, (int, float)):
        return Vector2(x)
    elif isinstance(x, (tuple, list)) and len(x) == 2:
        return Vector2(x[0], x[1])
    raise TypeError(f"Cannot convert typeof '{type(x)}' to Vector2")    

Vector2.ZERO = Vector2(0)
Vector2.ONE = Vector2(1)

Vector2.LEFT = Vector2(-1, 0)
Vector2.RIGHT = Vector2(1, 0)
Vector2.UP = Vector2(1, 0)
Vector2.DOWN = Vector2(-1, 0)

class Vector3:
    """randomengine.math.vector3"""

    def __init__(self, x, y = None, z = None):
        self.x = x
        self.y = y if y is not None else x
        self.z = z if z is not None else 0 if y is not None else x

    ZERO = ...
    ONE = ...
        
    FORWARD = ...
    BACK = ...
    
    LEFT = ...
    RIGHT = ...

    UP = ...
    DOWN = ...

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
    
    def __add__(self, o):
        o = toVector3(o)
        return Vector3(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o):
        o = toVector3(o)
        return Vector3(self.x - o.x, self.y - o.y, self.z - o.z)

    def __mul__(self, o):
        o = toVector3(o, True)
        return Vector3(self.x * o.x, self.y * o.y, self.z * o.z)

    def __rmul__(self, o):
        return self * o

    def __truediv__(self, o):
        o = toVector3(o)
        if o.magnitude is 0: return Vector3.ZERO
        else:
            return Vector3(self.x / o.x, self.y / o.y, self.z / o.z)

    def __eq__(self, o) -> bool:
        o = toVector3(o)
        return (
            self.x == o.x and
            self.y == o.y and
            self.z == o.z
        )
    
    @property
    def sqrMagnitude(self) -> float:
        return self.x ** 2 + self.y ** 2 + self.z ** 2
    
    @property
    def magnitude(self) -> float:
        return Mathf.sqrt(self.sqrMagnitude)
    
    @property
    def normalized(self):
        return self / Vector3(self.magnitude)
    
    def normalize(self):
        return self.normalized
    
    @staticmethod
    def lerp(a, b, t: float, clamp = True):
        a = toVector3(a)
        b = toVector3(b)
        if clamp:
            t = Mathf.clamp01(t)
        else:
            return Vector3(
                Mathf.lerp_unclamped(a.x, b.x, t),
                Mathf.lerp_unclamped(a.y, b.y, t),
                Mathf.lerp_unclamped(a.z, b.z, t)
            )

    def lerpTo(self, b, t: float, clamp = True):
        v = Vector3.lerp(self, b, t, clamp)
        self.x, self.y, self.z = v.x, v.y, v.z
        

def toVector3(x, ones = False) -> Vector3:
    if isinstance(x, Vector3):
        return x
    elif isinstance(x, Vector2):
        if ones: return Vector3(x.x, x.y, 1)
        return Vector3(x.x, x.y)
    elif isinstance(x, (int, float)):
        return Vector3(x)
    elif isinstance(x, (tuple, list)) and len(x) == 3:
        return Vector3(x[0], x[1], x[2])
    raise TypeError(f"Cannot convert typeof '{type(x)}' to Vector3")
    

Vector3.ZERO = Vector3(0)
Vector3.ONE = Vector3(1)

Vector3.FORWARD = Vector3(0, 0, 1)
Vector3.BACK = Vector3(0, 0, -1)

Vector3.LEFT = Vector3(-1, 0)
Vector3.RIGHT = Vector3(1, 0)

Vector3.UP = Vector3(1, 0)
Vector3.DOWN = Vector3(-1, 0)

class Vector4:
    """randomengine.utils.vector4"""

    def __init__(self, x, y = None, z = None, w = None):
        self.x = x
        self.y = y if y is not None else x
        self.z = z if z is not None else 0 if y is not None else x
        self.w = w if w is not None else 0 if y is not None else x

    ZERO = ...
    ONE = ...
        
    X = ...
    Y = ...
    Z = ...
    W = ...

    def __repr__(self):
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"
    
    def __add__(self, o):
        o = toVector4(o)
        return Vector4(self.x + o.x, self.y + o.y, self.z + o.z, self.w + o.w)

    def __sub__(self, o):
        o = toVector4(o)
        return Vector4(self.x - o.x, self.y - o.y, self.z - o.z, self.w - o.w)

    def __mul__(self, o):
        o = toVector4(o, True)
        return Vector4(self.x * o.x, self.y * o.y, self.z * o.z, self.w * o.w)

    def __rmul__(self, o):
        return self * o

    def __truediv__(self, o):
        o = toVector4(o)
        if o.magnitude is 0: return Vector4.ZERO
        else:
            return Vector4(self.x / o.x, self.y / o.y, self.z / o.z, self.w / o.w)

    def __eq__(self, o) -> bool:
        o = toVector4(o)
        return (
            self.x == o.x and
            self.y == o.y and
            self.z == o.z and
            self.w == o.w
        )
    
    @property
    def sqrMagnitude(self) -> float:
        return self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2
    
    @property
    def magnitude(self) -> float:
        return Mathf.sqrt(self.sqrMagnitude)
    
    @property
    def normalized(self):
        return self / Vector4(self.magnitude)
    
    def normalize(self):
        return self.normalized
    
    @staticmethod
    def lerp(a, b, t: float, clamp = True):
        a = toVector4(a)
        b = toVector4(b)
        if clamp:
            t = Mathf.clamp01(t)
        else:
            return Vector4(
                Mathf.lerp_unclamped(a.x, b.x, t),
                Mathf.lerp_unclamped(a.y, b.y, t),
                Mathf.lerp_unclamped(a.z, b.z, t),
                Mathf.lerp_unclamped(a.w, b.w, t)
            )

    def lerpTo(self, b, t: float, clamp = True):
        v = Vector4.lerp(self, b, t, clamp)
        self.x, self.y, self.z, self.w = v.x, v.y, v.z, v.w
        

def toVector4(x, ones = False) -> Vector4:
    if isinstance(x, Vector4):
        return x
    elif isinstance(x, Vector3):
        if ones : return Vector3(x.x, x.y, x.z, 1)
        return Vector4(x.x, x.y, x.z)
    elif isinstance(x, Vector2):
        if ones : return Vector2(x.x, x.y, 1, 1)
        return Vector4(x.x, x.y)
    elif isinstance(x, (int, float)):
        return Vector4(x)
    elif isinstance(x, (tuple, list)) and len(x) == 4:
        return Vector4(x[0], x[1], x[2], x[3])
    raise TypeError(f"Cannot convert typeof '{type(x)}' to Vector4")
    

Vector4.ZERO = Vector4(0)
Vector4.ONE = Vector4(1)

Vector4.X = Vector4(1, 0)
Vector4.Y = Vector4(0, 1)
Vector4.Z = Vector4(0, 0, 1)
Vector4.W = Vector4(0, 0, 0, 1)