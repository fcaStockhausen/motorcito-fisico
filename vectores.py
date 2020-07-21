import math
### ACA PONDRE TODAS LAS OP DE VECTORES

#Vector en euclidiano
class Vector2D:
    def __init__(self, coords):
        self.x, self.y = coords

    def __add__(self, vector2):
        return self.x + vector2.x, self.y + vector2.y

    def __sub__(self, vector2):
        return self.x - vector2.x, self.y - vector2.y
    
    def dot_product(self, vector2):
        return self.x * vector2.x + self.y * vector2.y

    def norma(self):
        return math.sqrt(self.dot_product(self, self))
    
    #def cross_product(self, vector2): No lo uso


    
        