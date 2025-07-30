# randomengine.utils > mathf

import math

class Mathf:
    """randomengine.utils.mathf"""

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        t = Mathf.clamp01(t)
        return a + (b - a) * t
    
    @staticmethod
    def lerp_unclamped(a: float, b: float, t:float) -> float:
        return a + (b - a) * t
    
    @staticmethod
    def clamp(v: float, min_v: float, max_v: float) -> float:
        return max(min_v, min(v, max_v))
    
    @staticmethod
    def clamp01(v: float) -> float:
        return Mathf.clamp(v, 0.0, 1.0)
    
    @staticmethod
    def smoothstep(a: float, b: float, fac: float) -> float:
        t = Mathf.clamp01((fac - a) / (b - a))
        return t**2 * (3 - 2 * t)
    
    @staticmethod
    def pow(b: float, e: float) -> float:
        return math.pow(b, e)
    
    @staticmethod
    def round(v: float) -> int:
        return math.floor(v + 0.5) if v > 0 else math.ceil(v - 0.5)

    @staticmethod
    def sqrt(b: float) -> float:
        return math.sqrt(b)
    
    @staticmethod
    def sign(v: float) -> int:
        return (v > 0) - (v < 0)
    
    @staticmethod
    def floor(v: float) -> int:
        return math.floor(v)
    
    @staticmethod
    def ceil(v: float) -> int:
        return math.ceil(v)
    
    @staticmethod
    def sin(x: float) -> float:
        return math.sin(x)
    
    @staticmethod
    def cos(x: float) -> float:
        return math.cos(x)
    
    @staticmethod
    def acos(x: float) -> float:
        return math.acos(x)
    
    @staticmethod
    def tan(x: float) -> float:
        return math.tan(x)
    
    @staticmethod
    def rad(d: float) -> float:
        return math.radians(d)
    
    @staticmethod
    def deg(r: float) -> float:
        return math.degrees(r)
    
    PI = math.pi
    RADIANS = PI / 180
    DEGREES = 180 / PI