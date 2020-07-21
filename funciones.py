''' Funciones  '''
import math

# Module file: funciones.py


def detectaDiferenciaPosicion(p1, coords2):
    '''Calcula la distancia radial entre un'''
    puntoX, puntoY = coords2

    if math.hypot((p1.x-puntoX),(p1.y-puntoY))<=p1.size:
        return 1
    else:
        return 0


def sumaFuerzas(f1,f2):
    '''Suma dos fuerzas xd'''
    return [f1[0]+f2[0], f1[1]+f2[1]]

def addVectors(v1, v2):
    ''' Suma dos vectores en general, de la forma (r, theta) '''
    r1, theta1 = v1
    r2, theta2 = v2
    x  = math.cos(theta1) * r1 + math.cos(theta2) * r2
    y  = math.sin(theta1) * r1 + math.sin(theta2) * r2
    
    theta = math.atan2(y, x)
    r  = math.hypot(x, y)

    return [r, theta]

def transformaCartesiano(vector): # (r, theta)
    '''El viento es mas facil representarlo en cartesiano'''
    return [vector[0]*math.cos(vector[1]), -vector[0]*math.sin(vector[1])] # LLeva un - porque el sistema de ref esta al reve

def transformaAngular(vector):
    return [math.hypot(vector[0], vector[1]), math.atan2(-vector[1], vector[0])]

