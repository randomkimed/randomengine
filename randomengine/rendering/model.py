# randomengine.rendering > model

from randomengine.core.object import Modifier
from randomengine.rendering.mesh import Mesh
from randomengine.rendering.shader import Shader, Material
from randomengine.math.matrix import Matrix

class Model(Modifier):
    """randomengine.rendering.model"""

    def __init__(self):
        super().__init__()
        self.matrix: Matrix = None
        self.mesh: Mesh = None
        self.material: Material = None