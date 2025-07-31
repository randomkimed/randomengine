# randomengine.core > object

from typing import TypeVar, Type, Optional
from functools import wraps

from randomengine.math.vector import Vector3
from randomengine.math.quaternion import Quaternion
from randomengine.math.transform import Transform

from randomengine.rendering.model import Model

class Modifier:
    """randomengine.core.modifier"""

    def __init__(self):
        self.owner: Object = None
        self.__dirty = set()

    def START(self):
        pass

    def AWAKE(self):
        pass

    def UPDATE(self):
        pass

    def LATE_UPDATE(self):
        pass

    def FIXED_UPDATE(self):
        pass

    def EXIT(self):
        pass

    def DIRTY(self, *fields: str):
        self.__dirty.update(fields)

    def IS_DIRTY(self, field: str):
        return field in self.__dirty

    @staticmethod
    def DIRTY_UPDATE(*fields: str, strict: bool = False):
        def decorator(method):
            @wraps(method)
            def wrapper(self, *args, **kwargs):
                check = [self.IS_DIRTY(field) for field in fields]
                dirty = all(check) if strict else any(check)

                if dirty:
                    result = self.func(*args, **kwargs)
                    self.__dirty.difference_update(fields)
                    return result
            return wrapper
        return decorator

M = TypeVar('M', bound=Modifier)

class Object:
    """randomengine.core.object"""
    
    def __init__(
            self,
            name: str = "New Object",
            parent: "Object" = None,
            modifiers: Optional[list[Modifier]] = None,
            position: Vector3 = Vector3.ZERO,
            rotation: Quaternion = Quaternion.IDENTITY,
            scale: Vector3 = Vector3.ONE
    ):
        self.name: str = name
        self.parent: "Object" = parent
        self.modifiers: list[Modifier] = modifiers if modifiers is not None else []

        t = next((mod for mod in self.modifiers if isinstance(m, Transform)), None)
        m = next((mod for mod in self.modifiers if isinstance(m, Model)), None)

        if t:
            t.local_position = position
            t.local_rotation = rotation
            t.local_scale = scale
        else:
            t = Transform(position, rotation, scale)
            self.modifiers.insert(0, t)

        self.transform: Transform = t # must have a instance
        self.model: Model = m # can be null, renderer will just skip over it

    def add(self, mod: Modifier):
        self.modifiers.append(mod)
        mod.owner = self

    def get(self, query: Type[M]) -> Optional[M]:
        return next((mod for mod in self.modifiers if isinstance(mod, query)), None)