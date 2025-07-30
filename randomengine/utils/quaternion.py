# randomengine.utils > quaternion

from randomengine.utils.mathf import Mathf
from randomengine.utils.vector import Vector3

class Quaternion:
    """radomengine.utils.quaternion"""

    def __init__(self, x: float, y: float, z: float, w: float):
        self.x, self.y, self.z, self.w = x, y, z, w

    IDENTITY = ...
    ZERO = ...

    def __repr__(self):
        return f"Quaternion({self.x}, {self.y}, {self.z}, {self.w})"
    
    def __neg__(self):
        return self.inverse
    
    def __add__(self, o):
        o = toQuaternion(o)
        return Quaternion(self.x + o.x, self.y + o.y, self.z + o.z, self.w + o.w)

    def __sub__(self, o):
        o = toQuaternion(o)
        return Quaternion(self.x - o.x, self.y - o.y, self.z - o.z, self.w - o.w)

    def __mul__(self, o):
        q = self
        if isinstance(o, Quaternion):
            return Quaternion(
                q.w * o.x + q.x * o.w + q.y * o.z - q.z * o.y,
                q.w * o.y - q.x * o.z + q.y * o.w + q.z * o.x,
                q.w * o.z + q.x * o.y - q.y * o.x + q.z * o.w,
                q.w * o.w - q.x * o.x - q.y * o.y - q.z * o.z
            ) # <-- the matrix of pain, japanese bamboo torture, and agony™ (quaternion multiplication matrix)
        elif isinstance(o, (int, float)):
            return Quaternion(
                q.x * o,
                q.y * o,
                q.z * o,
                q.w * o
            )
        else:
            raise TypeError(f"Cannot multiply Quaternion by typeof '{type(o)}'")

    def __rmul__(self, o):
        return self * o

    def __truediv__(self, o):
        if isinstance(o, (int, float)):
            if o is 0: return Quaternion.identity
            return Quaternion(self.x / o, self.y / o, self.z / o, self.w / o)
        elif isinstance(o, Quaternion):
            return self * o.inverse
        else:
            raise TypeError(f"Cannot divide Quaternion by typeof '{type(o)}'")

    def __eq__(self, o):
        o = toQuaternion(o)
        return (
            self.x == o.x and
            self.y == o.y and
            self.z == o.z and
            self.w == o.w
        )

    @property
    def sqrMagnitude(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2

    @property
    def magnitude(self):
        return Mathf.sqrt(self.sqrMagnitude)

    @property
    def normalized(self):
        m = self.magnitude
        if m is 0: return Quaternion.identity
        return self / self.magnitude

    def normalize(self):
        return self.normalized
    
    @property
    def conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)
    
    @property
    def inverse(self):
        if self.sqrMagnitude is 0: return Quaternion.identity
        return self.conjugate / self.sqrMagnitude
    
    def invert(self):
        q = self.inverse
        self.x, self.y, self.z, self.w = q.x, q.y, q.z, q.w

    @property
    def eulers(self):
        pass

    @property
    def axis(self) -> Vector3:
        s = Mathf.sqrt(1 - self.w ** 2)
        if s < 0.001: return Vector3(1, 0, 0)
        return Vector3(self.x, self.y, self.z) / s
    
    @property
    def angle(self) -> float:
        return 2 * Mathf.acos(self.w)

    @property
    def axis_angle(self):
        return self.axis, self.angle

    @staticmethod
    def Euler(x, y, z):
        pass

    @staticmethod
    def AxisAngle(axis: Vector3, angle: float):
        axis = axis.normalized
        sin_half_angle = Mathf.sin(angle / 2)
        cos_half_angle = Mathf.cos(angle / 2)

        return Quaternion (
            axis.x * sin_half_angle,
            axis.y * sin_half_angle,
            axis.z * sin_half_angle,
            cos_half_angle
        )
    
Quaternion.IDENTITY = Quaternion(0, 0, 0, 1)
Quaternion.ZERO = Quaternion(0, 0, 0, 0)

def toQuaternion(x) -> Quaternion:
    if isinstance(x, Quaternion):
        return x
    raise TypeError(f"Cannot convert typeof '{type(x)}' to Quaternion")