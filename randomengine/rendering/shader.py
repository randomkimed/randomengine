# randomengine.rendering > shader

from randomengine.core.asset import Asset

class Shader(Asset):
    def __init__(self):
        pass

DEFAULT_LIT_SHADER = Shader()

class Material(Asset):
    def __init__(self, shader = DEFAULT_LIT_SHADER):
        self.shader: Shader = shader

DEFAULT_LIT = Material()