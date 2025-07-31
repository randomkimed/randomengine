# randomengine.rendering > mesh

import os
from warnings import warn

from randomengine.core.asset import Asset, FORMAT
from randomengine.math.vector import Vector3, Vector2

class Mesh():
    def __init__(
        self,
        verticies: list[Vector3] = None,
        indices: list[tuple[int, int, int]] = None,
        normals: list[Vector3] = None,
        uvs: list[Vector2] = None
    ):
        # Mesh data
        self.vertices: list[Vector3] = []
        self.indices: list[tuple[int, int, int]] = []
        self.normals: list[Vector3] = []
        self.uvs: list[Vector2] = []

        self.bounding_box = None

    @staticmethod
    def triangulate_face(face: list[int]) -> list[tuple[int, int, int]]:
        if len(face) < 3:
            return []
        triangles = []
        for i in range(1, len(face) - 1):
            triangles.append((face[0], face[i], face[i + 1]))
        return triangles
    
    @staticmethod    
    def Cube(width: float = 1, height: float = None, depth: float = None):
        # Scalar input
        height = height if height is not None else width
        depth = depth if depth is not None else 1 if height is not None else width

        # Create a 1x1x1 cube * dimensions(width, height, depth)

        cube = Mesh()
        cube.loaded = True
        dimensions = Vector3(width, height, depth)

        cube.vertices = [
            Vector3(-0.5, -0.5, 0.5) * dimensions,
            Vector3(0.5, -0.5, 0.5) * dimensions,
            Vector3(0.5, -0.5, -0.5) * dimensions,
            Vector3(-0.5, -0.5, -0.5) * dimensions,
            Vector3(-0.5, 0.5, 0.5) * dimensions,
            Vector3(0.5, 0.5, 0.5) * dimensions,
            Vector3(0.5, 0.5, -0.5) * dimensions,
            Vector3(-0.5, 0.5, -0.5) * dimensions
        ]

        # Averag normalized corner normals
        cube.normals = [vertex.normalized for vertex in cube.vertices]
        
        # All (0, 0)
        cube.uvs = [Vector2.ZERO for _ in cube.vertices]

        cube.indices = [
            (1,2,5), (2,5,6), # front face
            (2,3,4), (3,6,7), # right face
            (5,6,8), (6,7,8), # top face
            (1,3,4), (1,2,3), # bottom face
            (1,4,5), (4,5,8), # left face
            (4,7,8), (3,4,7) # back face
        ]

        return cube

    CUBE = Cube()

class MeshAsset(Asset):
    """randomengine.rendering.mesh_asset"""

    def __init__(
        self,
        path: str = "",
        triangulate: bool = None,
    ):
        super().__init__(path)

        self.format = None
        self.triangulate = triangulate or True # always triangulate meshes by default

    def parse(self, format: str, raw: str): # raw: str is ok here right?
        if format in FORMAT.WAVEFRONT:
            self.format = "Wavefront (OBJ)"
            
            v: list[Vector3] = []
            t: list[Vector2] = []
            n: list[Vector3] = []

            mesh = Mesh()

            for line in raw.splitlines():
                line = line.strip()

                if not line or line.startswith('#'):
                    continue # skip comments (#) and empty lines

                token = line.split()
                prefix = token[0]

                if prefix == 'v': v.append(Vector3(*map(float, token[1:4])))

                elif prefix == 'vt': t.append(Vector2(*map(float, token[1:3])))

                elif prefix == 'vn': n.append(Vector3(*map(float, token[1:4])))

                elif prefix == 'f':
                    face = []

                    for vert in token[1:]:
                        # OBJ face can be v, v/vt, v//vn, or v/vt/vn

                        components = vert.split('/')
                        vi = int(components[0]) - 1 # vertex index

                        if len(components) >= 2 and components[1]:
                            ti = int[components[1]] - 1 # uv index
                            while len(mesh.uvs) <= vi:
                                mesh.uvs.append(Vector2())
                            mesh.uvs[vi] = t[ti]

                        if len(components) == 3 and components[2]:
                            ni = int(components[2]) - 1 # normal index
                            while len(mesh.normals) <= vi:
                                mesh.normals.append(Vector3())
                            mesh.normals[vi] = n[ni]

                        face.append(vi) # append vertex index to face indices

                    if len(face) == 3 or not self.trianglutate:
                        if len(face) > 3:
                            warn("Mesh contains non-triangular faces and/or N-gons")
                        mesh.indices.append(tuple(face))
                    else:
                        mesh.indices.extend(Mesh.triangulate_face(face))
            mesh.vertices = v

            return mesh
        else:
            raise ValueError(f"Unsupported mesh file format: {format}")

    def load(self):
        data = super().load()
        ext = os.path.splitext(self.path)[1].lower()

        if ext in FORMAT.WAVEFRONT:
            # Parse - Wavefront (OBJ)
            self.reference = self.parse("obj", data)
        else:
            raise ValueError(f"Unsupported mesh file format: {ext}")