# randomengine.math > matrix

import math
import copy

from randomengine.math.vector import Vector3
from randomengine.math.quaternion import Quaternion

class Matrix: # if you're wondering why its not called Matrix4x4 or Matrix4, it's because i'm only doing this once and SPECIFICALLY for transformation matrices.
    """randomengine.math.matrix"""

    IDENTITY = ...
    
    def __init__(self, rows = None):
        if not rows: rows = [ # default to indentity matrix
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        if len(rows) == 4: # [] [] [] []
            self.elements = [e for row in rows for e in row] # split data into a neat linear array (0-15)
        elif len(rows) == 1:
            self.elements = rows
        else: raise ValueError("Matrix requires a 4v4 nested list or a linear array of 16 members")

    def validate_index(self, key):
        if isinstance(key, tuple):
            if len(key) == 2:
                row, col = key
            else:
                if not(0 <= key < 16): raise IndexError(f"Matrix index out of range (0-15): given '{key}'")
                row, col = divmod(key, 4)
        else: raise TypeError("Matrix[key] requires a pair of 2D integer indices (tuple[int, int]) or a single array index (int)")

        if not (0 <= row < 4 and 0 <= col < 4):
            raise IndexError(f"Matrix indices out of range (0-4, 0-4): given '{row}, {col}'")
        
        return row, col

    def __getitem__(self, key):
        row, col = self.validate_index(key)
        return self.elements[row * 4 + col]
    
    def __setitem__(self, key, value: float):
        row, col = self.validate_index(key)
        self.elements[row * 4 + col] = value

    def __repr__(self):
        rows = [
            self.elements[i * 4:(i + 1) * 4]
            for i in range(4)
        ]
        row_strs = ["[" + ", ".join(f"{v: .3f}" for v in row) + "]" for row in rows]
        return "Matrix(\n  " + ",\n  ".join(row_strs) + "\n)"
    
    def __eq__(self, o):
        return isinstance(o, Matrix) and self.elements == o.elements

    @property
    def inverse(self):
        # returns inverse (wallahi this is going to suck balls to write)
        m = [list(self.elements[i:i+4]) for i in range(0, 16, 4)]
        id = [[float(i == j) for j in range(4)] for i in range(4)]

        for i in range(4):
            # find pivot
            pivot = m[i][i]
            if abs(pivot) < 1e-10:
                # try swapping with a lower row
                for j in range(i + 1, 4):
                    if abs(m[j][i]) > abs(pivot):
                        m[i], m[j] = m[j], m[i]
                        id[i], id[j] = id[j], id[i]
                        pivot = m[i][i]
                        break
                    else:
                        raise ValueError("Matrix is not invertible")
            
            # normalize row
            for j in range(4):
                m[i][j] /= pivot
                id[i][j] /= pivot

            # eliminate col
            for k in range(4):
                if k == i: continue
                fac = m[k][i]
                for j in range(4):
                    m[k][j] -= fac * m[i][j]
                    id[k][j] -= fac * id[i][j]

        # return as Matrix
        inverse = [x for row in id for x in row]
        return Matrix(inverse)
    
    def invert(self):
        # sets the current matrix to its inverse
        self.elements = copy.deepcopy(self.inverse.elements)

    def __inverse__(self):
        return self.inverse

    def __neg__(self):
        return Matrix([
            -e for e in self.elements
        ])

    def __add__(self, o):
        if not isinstance(o, Matrix): raise TypeError(f"Can not convert 4x4 Matrix to typeof '{type(o)}'")
        sum = [a + b for a, b in zip(self.elements, o.elements)]
        return Matrix(sum)
    
    def __sub__(self, o):
        if not isinstance(o, Matrix): raise TypeError(f"Can not convert 4x4 Matrix to typeof '{type(o)}'")
        dif = [a - b for a, b in zip(self.elements, o.elements)]
        return Matrix(dif)
    
    def __mul__(self, o):
        if not isinstance(o, Matrix):
            raise TypeError(f"Can not convert 4x4 Matrix to typeof '{type(o)}'")
        
        fac = [
            sum(self[row, k] * o[k, col] for k in range(4))
            for row in range(4)
            for col in range(4)
        ]
        return Matrix(fac)

    def transpose(self):
        return Matrix([
            self[0], self[4], self[8], self[12],
            self[1], self[5], self[9], self[13],
            self[2], self[6], self[10], self[14],
            self[3], self[7], self[11], self[15]
        ])
    
    @property
    def T(self): return self.transpose()

    @staticmethod
    def Translation(position: Vector3) -> "Matrix":
        m = Matrix.IDENTITY
        m[0, 3] = position.x
        m[1, 3] = position.y
        m[2, 3] = position.z
        return m
    
    @staticmethod
    def Scale(scale: Vector3) -> "Matrix":
        m = Matrix.IDENTITY
        m[0, 0] = scale.x
        m[1, 1] = scale.y
        m[2, 2] = scale.z
        return m
    
    @staticmethod
    def Rotation(rotation: Quaternion) -> "Matrix":
        x, y, z, w = rotation.x, rotation.y, rotation.z, rotation.w
        xx = x ** 2
        yy = y ** 2
        zz = z ** 2
        xy = x * y
        xz = x * z
        yz = y * z
        wx = w * x
        wy = w * y
        wz = w * z

        return Matrix([
            [1 - 2 * (yy + zz),       2 * (xy - wz),      2 * (xz + wy),          0],
            [    2 * (xy + wz),   1 - 2 * (xx + zz),      2 * (yz - wx),          0],
            [    2 * (xz - wy),       2 * (yz + wx),  1 - 2 * (xx + yy),          0],
            [                0,                   0,                  0,          1]
        ])
    
    def split(self) -> tuple[Vector3, Quaternion, Vector3]:
        T = Vector3(
            self[0, 3],
            self[1, 3],
            self[2, 3]
        )
        S = Vector3(
            Vector3(self[0, 0], self[1, 0], self[2, 0]).magnitude,
            Vector3(self[0, 1], self[1, 1], self[2, 1]).magnitude,
            Vector3(self[0, 2], self[1, 2], self[2, 2]).magnitude
        )
        
        R = Quaternion.Matrix(
            Matrix([
                [self[0, 0] / S.x, self[0, 1] / S.y, self[0, 2] / S.z, 0],
                [self[1, 0] / S.x, self[1, 1] / S.y, self[1, 2] / S.z, 0],
                [self[2, 0] / S.x, self[2, 1] / S.y, self[2, 2] / S.z, 0],
                [0, 0, 0, 1]
            ])
        )

        return T, R, S

Matrix.IDENTITY = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])