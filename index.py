import tkinter as tk
from dataclasses import dataclass
import numpy as np


class vec3d:
    def __init__(self, x, y, z):
        self.components = np.array([x, y, z])

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return f"vec3d({self.x}, {self.y}, {self.z})"

    @property
    def x(self):
        return self.components[0]

    @property
    def y(self):
        return self.components[1]

    @property
    def z(self):
        return self.components[2]

    @x.setter
    def x(self, value):
        self.components[0] = value

    @y.setter
    def y(self, value):
        self.components[1] = value

    @z.setter
    def z(self, value):
        self.components[2] = value

    def magnitude(self):
        return np.linalg.norm(self.components)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            self.components /= mag

    def dot(self, other):
        return np.dot(self.components, other.components)

    def cross(self, other):
        return vec3d(*np.cross(self.components, other.components))

    def __add__(self, other):
        return vec3d(*np.add(self.components, other.components))

    def __sub__(self, other):
        return vec3d(*np.subtract(self.components, other.components))

    def __mul__(self, other):
        if isinstance(other, vec3d):
            return self.dot(other)
        else:
            return np.multiply(self.components, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return vec3d(*np.divide(self.components, other))   
    
class triangle:
    p: list[vec3d]
    def __init__(self, p1, p2, p3):
        self.p = [p1, p2, p3]
    
    
@dataclass
class mesh:
    tris: list[triangle]
    # def __init__(self, tris):
    #     self.tris = tris
    
class mat4x4:
    m: np.array([])
    

    
    

class Drawingwindow:

    def __init__(self, width, height):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.meshCube = mesh(tris = list[triangle])
        self.matProj = mat4x4()
        self.onUserCreate()

        
    
    def draw_rectangle(self, x, y, width, height, color):
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=color)
    
    def draw_line(self, v1, v2, color):
        self.canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=color)
    
    def draw_triangle(self, v1, v2, v3, color):
        self.canvas.create_polygon(v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, fill=color)
    
    def multiplyMatrixVector(self, input, output, matrix):
        thingy = np.array_split(matrix.m, 3, 1)
        first = np.concatenate((thingy[0], thingy[1]), axis=1)
        second = thingy[2]
       
        print(np.array([input.components]))
        new =np.reshape(np.array([input.components]), (3,1))
        print(new)
        print(first)
        print(np.matmul(first, new))
        # # output = np.reshape(np.matmul(first, new), (3,))
        # print(output)
        
        
    def onUserCreate(self):
        self.meshCube.tris = [
            #SOUTH
            triangle(vec3d(0, 0, 0), vec3d(0, 1, 0), vec3d(1, 1, 0)),
            triangle(vec3d(0, 0, 0), vec3d(1, 1, 0), vec3d(1, 0, 0)),
            #EAST
            triangle(vec3d(1, 0, 0), vec3d(1, 1, 0), vec3d(1, 1, 1)),
            triangle(vec3d(1, 0, 0), vec3d(1, 1, 1), vec3d(1, 0, 1)),
            #NORTH
            triangle(vec3d(1, 0, 1), vec3d(1, 1, 1), vec3d(0, 1, 1)),
            triangle(vec3d(1, 0, 1), vec3d(0, 1, 1), vec3d(0, 0, 1)),
            #WEST
            triangle(vec3d(0, 0, 1), vec3d(0, 1, 1), vec3d(0, 1, 0)),
            triangle(vec3d(0, 0, 1), vec3d(0, 1, 0), vec3d(0, 0, 0)),
            #TOP
            triangle(vec3d(0, 1, 0), vec3d(0, 1, 1), vec3d(1, 1, 1)),
            triangle(vec3d(0, 1, 0), vec3d(1, 1, 1), vec3d(1, 1, 0)),
        ]
        fNear = 0.1
        fFar = 1000.0
        FFov = 90.0
        fAspectRatio = self.height / self.width
        fFovRad = 1.0 / np.tan(FFov * 0.5 / 180.0 * np.pi)
        self.matProj.m = np.array([
                            [fAspectRatio*fFovRad, 0.0, 0.0, 0.0], 
                            [0.0, 0.0, fFar/(fFar - fNear), 1.0], 
                            [0.0, fFovRad, 0.0, 0.0], 
                            [0.0, 0.0, (-fFar * fNear)/(fFar - fNear), 0.0]
                 ])
        
        
        # print(self.meshCube.tris[0].p[2]*self.matProj.m)

        output = 0
        self.multiplyMatrixVector(self.meshCube.tris[0].p[0], output, self.matProj)
        
        
        
        
    def run(self):
        self.root.mainloop()
        
        


def main():
    window = Drawingwindow(500, 500)
    window.draw_rectangle(100, 100, 200, 200, 'black')
    # window.run()

main()
      