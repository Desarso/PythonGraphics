import tkinter as tk
from dataclasses import dataclass
import numpy as np
import time


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
    def __init__(self):
        self.m = np.array([
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ])
    m: np.array([])

@dataclass 
class elapsedTime:
            time = 0
    

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
        self.fTheta = 0
        self.index = 0

        
    
    def draw_rectangle(self, x, y, width, height, color):
        return self.canvas.create_rectangle(x, y, x+width, y+height, fill=color)
    
    def draw_line(self, v1, v2, color, width=1):
        self.canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=color, width=width)
    
    def draw_circle(self, x, y, radius, color):
        return self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)

    def draw_triangle(self, v1, v2, v3, color, width=1):
        self.canvas.create_polygon(v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, fill=color)
        
        # self.draw_line(v1, v2, color, width=width)
        # self.draw_line(v2, v3, color, width=width)
        # self.draw_line(v3, v1, color, width=width)
    
    def multiplyMatrixVector(self, input, output, matrix):



        #for matrix conversion
        split3 = np.array_split(matrix.m, 3, 1)
        appendRight = np.concatenate((split3[0], split3[1]), axis=1)
        before = np.array_split(appendRight, 3, 0)
        RightSide = split3[2]
        beforeR3 = np.array_split(RightSide, 3, 0)
        Matrix3x3 = np.concatenate((before[0], before[1]), axis=0)

        #for w conversion
        right3 = np.concatenate((beforeR3[0], beforeR3[1]), axis=0)

        w = np.matmul(input.components, right3)[0] + RightSide[3][0]



        #get result
        bottom = np.array_split(matrix.m, 4, 0)[3][0]
        bottom3 = np.array(bottom[0:3])
        result = np.matmul(Matrix3x3, input.components)
        result = np.add(result, bottom3)


        if(w != 0):
            output.components = np.divide(result, w)
        else:
            output.components = result
          
        

        
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
            #BOTTOM
            triangle(vec3d(1, 0, 1), vec3d(0, 0, 1), vec3d(0, 0, 0)),
            triangle(vec3d(1, 0, 1), vec3d(0, 0, 0), vec3d(1, 0, 0))
        ]


        fNear = 0.1
        fFar = 1000.0
        FFov = 90.0
        fAspectRatio = self.height / self.width
        fFovRad = 1.0 / np.tan(FFov * 0.5 / 180.0 * 3.14159)
        self.matProj.m = np.array([
                            [fAspectRatio*fFovRad, 0.0, 0.0, 0.0], 
                            [0.0, fFar/(fFar - fNear), 0, 0.0], 
                            [0.0, 0.0, fFovRad, 1.0], 
                            [0.0, 0.0, (-fFar * fNear)/(fFar - fNear), 0.0]
                 ])
      
        
    
        
    def redrawBackground(self, canvas, width, height, fill="white"):
        canvas.delete("all")
        canvas.create_rectangle(0, 0, width, height, fill=fill)
        canvas.pack()

    def mainloop(self):
        testVar = vec3d(100, 100, 0)
        fElapsedTime = elapsedTime()
        print(fElapsedTime.time)
        while True:

            self.root.update_idletasks()
            self.root.update()
            time.sleep(0.0166666667)
            fElapsedTime.time +=0.0166666667
            self.redrawBackground(self.canvas, self.width, self.height, 'black')
            # self.draw_circle(testVar.x, testVar.y, 10, 'red')
            # testVar.x += 1
            self.OnUserUpdate(fElapsedTime)
        
        
    def OnUserUpdate(self, fElapsedTime):

        # matRotZ = np.array([
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0]
        # ])
        # matRotX = np.array([
        #     [np.cos(self.fTheta), np.sin(self.fTheta), 0, 0],
        #     [-np.sin(self.fTheta), 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0]
        # ])
        matRotZ = mat4x4()
        matRotX = mat4x4()


        self.fTheta = (fElapsedTime.time * 4)
        # if(self.fTheta > 12.5663706144):
        #     self.fTheta = 0
        #     fElapsedTime.time = 0
        

        print(fElapsedTime.time)
        # print(fElapsedTime.time)

        # print(self.fTheta)
        # print(np.cos(self.fTheta))

        # Rotation Z
        matRotZ.m[0][0] = np.cos(self.fTheta)
        matRotZ.m[0][1] = np.sin(self.fTheta)
        matRotZ.m[1][0] = -np.sin(self.fTheta)
        matRotZ.m[1][1] = np.cos(self.fTheta)
        matRotZ.m[2][2] = 1
        matRotZ.m[3][3] = 1

        # Rotation X
        matRotX.m[0][0] = 1
        matRotX.m[1][1] = np.cos(self.fTheta * 0.5)
        matRotX.m[1][2] = np.sin(self.fTheta * 0.5)
        matRotX.m[2][1] = -np.sin(self.fTheta * 0.5)
        matRotX.m[2][2] = np.cos(self.fTheta * 0.5)
        matRotX.m[3][3] = 1

        # for m in matRotZ.m:
        #     print(m)
        
        # print("")
        # for m in matRotX.m:
        #     print(m)






        for tri in self.meshCube.tris:
            triProjected = triangle(vec3d(0, 0, 0), vec3d(0, 0, 0), vec3d(0, 0, 0))
            triRotatedZ = triangle(vec3d(0, 0, 0), vec3d(0, 0, 0), vec3d(0, 0, 0))
            triRotatedZX = triangle(vec3d(0, 0, 0), vec3d(0, 0, 0), vec3d(0, 0, 0))

            self.multiplyMatrixVector(tri.p[0], triRotatedZ.p[0], matRotZ)
            self.multiplyMatrixVector(tri.p[1], triRotatedZ.p[1], matRotZ)
            self.multiplyMatrixVector(tri.p[2], triRotatedZ.p[2], matRotZ)

         
            # for p in triRotatedZ.p:
            #     print(self.index, "-->",p.x, p.y, p.z)
            #     self.index += 1
        
            # for p in tri.p:
            #     print(self.index, "-->",p.x, p.y, p.z)
            #     self.index += 1




            self.multiplyMatrixVector(triRotatedZ.p[0], triRotatedZX.p[0], matRotX)
            self.multiplyMatrixVector(triRotatedZ.p[1], triRotatedZX.p[1], matRotX)
            self.multiplyMatrixVector(triRotatedZ.p[2], triRotatedZX.p[2], matRotX)


            # for p in triRotatedZX.p:
            #     print(p.x, p.y, p.z)

        

            triTranslated = triRotatedZX
            triTranslated.p[0].z = triRotatedZX.p[0].z + 3.0
            triTranslated.p[1].z = triRotatedZX.p[1].z + 3.0
            triTranslated.p[2].z = triRotatedZX.p[2].z + 3.0

         
            # for p in triTranslated.p:
            #     print(p.x, p.y, p.z)
            


            self.multiplyMatrixVector(triTranslated.p[0], triProjected.p[0], self.matProj)
            self.multiplyMatrixVector(triTranslated.p[1], triProjected.p[1], self.matProj)
            self.multiplyMatrixVector(triTranslated.p[2], triProjected.p[2], self.matProj)

            # for p in triProjected.p:
            #     print(p.x, p.y, p.z)
            # for p in self.matProj.m:
            #     print(p)
            # for p in triTranslated.p:
            #     print(p.x, p.y, p.z)
               
        
            
            triProjected.p[0].x += 1.0; triProjected.p[0].y += 1.0
            triProjected.p[1].x += 1.0; triProjected.p[1].y += 1.0
            triProjected.p[2].x += 1.0; triProjected.p[2].y += 1.0
            triProjected.p[0].x *= 0.5 * self.width; triProjected.p[0].y *= 0.5 * self.height
            triProjected.p[1].x *= 0.5 * self.width; triProjected.p[1].y *= 0.5 * self.height
            triProjected.p[2].x *= 0.5 * self.width; triProjected.p[2].y *= 0.5 * self.height

            # for p in triProjected.p:
            #     print(p.x, p.y, p.z)

            self.draw_triangle(triProjected.p[0], triProjected.p[1], triProjected.p[2], 'white', 2)
    
 


        
        


def main():
    window = Drawingwindow(500, 500)
   
    print(np.tan(2))
    window.mainloop()
    # test = vec3d(1, 2, 3)
    # out = vec3d(0, 0, 0)
    # window.multiplyMatrixVector(test, out, window.matProj)
    # print(out.x, out.y, out.z)
    # print(np.tan(90 * 0.5 / 180.0 * 3.14159))


   





main()
      