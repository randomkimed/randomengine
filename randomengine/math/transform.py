# randomengine.math > transform

from randomengine.core.object import Modifier

from randomengine.math.vector import Vector3
from randomengine.math.quaternion import Quaternion
from randomengine.math.matrix import Matrix

class Transform(Modifier):
    """randomengine.math.transform"""
    def __init__(self, position = Vector3.ZERO, rotation = Quaternion.IDENTITY, scale = Vector3.ONE):
        super().__init__()
        self.__local: list[Vector3, Quaternion, Vector3] = [position, rotation, scale] # local position cache
        self.__global: list[Vector3, Quaternion, Vector3] = [None, None, None] # global position cache
        self.matrix = Matrix.IDENTITY

        self.DIRTY('matrix', 'global')

    # Local Transforms

    @property
    def local_position(self) -> Vector3: return self.__local[0]

    @local_position.setter
    def local_position(self, v):
        self.__local[0] = v
        self.DIRTY('matrix', 'global')
    
    @property
    def local_rotation(self) -> Quaternion: return self.__local[1]
    
    @local_rotation.setter
    def local_rotation(self, v):
        self.__local[1] = v
        self.DIRTY('matrix', 'global')
    
    @property
    def local_scale(self) -> Vector3: return self.__local[2]
    
    @local_scale.setter
    def local_scale(self, v):
        self.__local[2] = v
        self.DIRTY('matrix', 'global')
    
    # Global Transforms

    @property
    def position(self):
        self.__update_globals() # will only execute if DIRTY becaues of the @
        return self.__global[0]

    @position.setter
    def position(self, v):
        self.DIRTY('globals')
        self.local_position = v - self.parent.position if self.parent is not None else v

    @property
    def rotation(self):
        self.__update_globals()
        return self.__global[1]

    @rotation.setter
    def rotation(self, v):
        self.DIRTY('globals')
        self.local_rotation = v - self.parent.rotation if self.parent is not None else v

    @property
    def scale(self):
        self.__update_globals()
        return self.__global[2]

    @position.setter
    def scale(self, v):
        self.DIRTY('globals')
        self.local_scale = v - self.parent.scale if self.parent is not None else v

    # Hierarchy stuff

    @property
    def parent(self) -> "Transform" | None:
        if self.owner is None or self.owner.parent is None:
            return None
        return self.owner.parent.get(Transform)

    # Coordinate Space Conversions and Caching

    @Modifier.DIRTY_UPDATE('global')
    def __update_globals(self):
        if self.parent is None:
            self.__global = [
                self.local_position,
                self.local_rotation,
                self.local_scale
            ]
        else:
            self.__global = [
                self.parent.position + self.local_position,
                self.parent.rotation * self.local_rotation,
                self.parent.scale * self.local_scale
            ]
    
    # Matrix math
    
    @Modifier.DIRTY_UPDATE('matrix')
    def __update_matrix(self):
        T = Matrix.Translation(self.position)
        R = Matrix.Rotation(self.rotation)
        S = Matrix.Scale(self.scale)
        self.matrix = T * R * S

    def UPDATE(self):
        self.__update_matrix()