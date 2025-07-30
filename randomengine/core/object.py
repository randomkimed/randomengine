# randomengine.core > object

from typing import TypeVar, Type, Optional

from randomengine.core.modifier import Modifier

from randomengine.math.vector import Vector3
from randomengine.math.quaternion import Quaternion
from randomengine.math.transform import Transform

from randomengine.rendering.model import Model

M = TypeVar('M', bound=Modifier)

class Object:
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