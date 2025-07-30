# randomengine.math > transform

from randomengine.core.modifier import Modifier

from randomengine.math.vector import Vector3
from randomengine.math.quaternion import Quaternion
from randomengine.math.matrix import Matrix

class Transform(Modifier):
    """randomengine.math.transform"""
    def __init__(self, position = Vector3.ZERO, rotation = Quaternion.IDENTITY, scale = Vector3.ONE):
        super().__init__()
        self.__local_position = position
        self.__local_rotation = rotation
        self.__local_scale = scale
        self.matrix = Matrix.IDENTITY

    # Local Transforms

    @property # POSITION
    def local_position(self) -> Vector3:
        return self.__local_position

    @local_position.setter
    def local_position(self, v):
        self.__local_position = v
        self.DIRTY('matrix')
    
    @property # ROTATION
    def local_rotation(self) -> Quaternion:
        return self.__local_rotation
    
    @local_rotation.setter
    def local_rotation(self, v):
        self.__local_rotation = v
        self.DIRTY('matrix')
    
    @property # SCALE
    def local_scale(self) -> Vector3:
        return self.__local_scale
    
    @local_scale.setter
    def local_scale(self, v):
        self.__local_scale = v
        self.DIRTY('matrix')
    
    # Global Transforms

    @property
    def position(self) -> Vector3: # POSITION
        return self.__local_position
    
    @position.setter
    def position(self, v):
        self.local_position = v
    
    @property
    def rotation(self) -> Quaternion: # ROTATION
        return self.__local_rotation
    
    @rotation.setter
    def rotation(self, v):
        self.local_rotation = v

    @property
    def scale(self) -> Vector3: # SCALE
        return self.__local_scale
    
    @scale.setter
    def scale(self, v):
        self.local_scale = v

    # Local and World Space Conversions

    @property
    def parent(self) -> Transform | None:
        if self.owner is None or self.owner.parent is None:
            return None
        return self.owner.parent.get(Transform)

    def localize(self, v: Vector3 | Quaternion) -> Vector3 | Quaternion:
        if self.parent is None:
            return v

    def globalize(self, v: Vector3 | Quaternion) -> Vector3 | Quaternion:
        pass
    
    # Matrix Math
    
    @Modifier.DIRTY_UPDATE('matrix')
    def __update_matrix(self):
        t = Matrix.Translation(self.position)
        r = Matrix.Rotation(self.rotation)
        s = Matrix.Scale(self.scale)
        self.matrix = t * r * s

    def UPDATE(self):
        self.__update_matrix()