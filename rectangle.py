import numpy

class Point:
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
class Rectangle:
    
    def __init__(self,unpack):
        x,y,w,h=unpack
        
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        
        self.bottomLeft=Point(x,y)
        self.bottomRight=Point(x+w,y)
        self.topLeft=Point(x,y+h)
        self.topRight=Point(x+w,y+h)
    
    def pad(self,padding):
    
        self.bottomLeft.x-=padding
        self.bottomLeft.y-=padding
        
        self.bottomRight.x+=padding
        self.bottomRight.y-=padding
        
        self.topLeft.x-=padding
        self.topLeft.y+=padding
        
        self.topRight.x+=padding
        self.topRight.y+=padding
    
        self.x-=padding
        self.y-=padding
        self.w+=padding
        self.h+=padding
    
    def unpad(self,padding):
    
        self.bottomLeft.x+=padding
        self.bottomLeft.y+=padding
        
        self.bottomRight.x-=padding
        self.bottomRight.y+=padding
        
        self.topLeft.x+=padding
        self.topLeft.y-=padding
        
        self.topRight.x-=padding
        self.topRight.y-=padding
    
        self.x+=padding
        self.y+=padding
        self.w-=padding
        self.h-=padding
    
    def unpack(self):
        return self.x,self.y,self.w,self.h
    
    def intersects(self, other):
        return not (self.topRight.x < other.bottomLeft.x or self.bottomLeft.x > other.topRight.x or self.topRight.y < other.bottomLeft.y or self.bottomLeft.y > other.topRight.y)    