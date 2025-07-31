# randomengine.core > asset

import os
from enum import Enum
from abc import ABC, abstractmethod

class FORMAT(Enum):
    # GRAPHICS
    BITMAP = "bmp",
    PNG = "png",
    JPEG = "jpg", "jpeg",
    ADOBE_PSD = "psd",
    VECTOR = "svg"
    
    # TEXT & DATA
    PLAINTEXT = "txt",
    JSON = "json",
    DATA = "dat",

    # MESH
    WAVEFRONT = "obj",
    FILMBOX = "fbx",
    COLLADA = "dae",
    BLENDER = "blend",
    KHRONOS = "gltf",

    # AUDIO
    WAVEFORM = "wav",
    MPEG = "mpeg", "mpg", "m2v",
    MPEG_A3 = "mp3",

    # VIDEO
    MPEG_4 = "mp4",
    QUICKTIME = "mov",

    # SHADER
    SHADER = "shader",
    SHADERFILE = "hlsl",

    # ENGINE ASSETS
    SCENE = "scene",
    MATERIAL = "material",
    SCRIPT = "py"

class Asset(ABC):
    def __init__(self, path: str = ""):
        self.uuid = ...
        self.path = os.path.abspath(path)

        self.reference = None
        self.loaded = False

    def load(self):
        # Return the contents of the file
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Asset not found at '{self.path}'")
        with open(self.path, "rb") as file:
            data = file.read()

        self.loaded = True
        return data
    
    @abstractmethod
    def unload(self):
        raise NotImplementedError()
    
    def reload(self):
        self.unload()
        self.load()

    def is_loaded(self) -> bool: return self.loaded