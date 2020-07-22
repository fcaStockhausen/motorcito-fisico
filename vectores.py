import math
### ACA PONDRE TODAS LAS OP DE VECTORES

#Vector en euclidiano
class Vector2D:
    def __init__(self, coords):
        self.x, self.y = coords

    def __add__(self, vector2):
        return Vector2D([self.x + vector2.x, self.y + vector2.y])

    def __sub__(self, vector2):
        return Vector2D([self.x - vector2.x, self.y - vector2.y])
    
    def dot_product(self, vector2):
        return self.x * vector2.x + self.y * vector2.y

    def set_misma_direccion(self, vector2):
        if self.x * vector2.x < 0:
            # Misma direccion
            # No hacer nada en x
            self.x *= -1

        if self.y * vector2.y < 0:
            # Distinta direccion
            self.y *= -1


    #def norma(self):
    #    return math.sqrt(self.dot_product(self, self))
    
    #def cross_product(self, vector2): No lo uso


    
        