""" UWU """
import math
import random
import pygame

## IDEAS
## Agregar viento
## Tomar en cuenta aerodinamicidad de la cuestion

# todu: Dibujar un punto al centro
# Que el punto se mueva
# 60 fps
# Si la bola sale de la pantalla que vuelva

# Monitorizar estado de las bolas haciendoles click
# Velocidad
# Angulo
# Posicion

############################################################
#
#                  |-------------------->x
#                  |
#                  |
#                  |
#                  |
#                  v
#                   y
#
#
#
#
#
###########################################################
LARGO = 800
ALTO = 800
COEFICIENTE_CLOCK = 7,63
pygame.init() # Inicializacion

VIENTO = (2, math.pi/4)
GRAVEDAD = (10, 3*math.pi/2)
ELASTICIDAD = 0.95
DRAGG = 1

#def move(posicion, deltaCito):
#    ''' Mueve la posicion '''
#    return (posicion[0]+deltaCito[0], posicion[1]-deltaCito[1])
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

def detectorColision(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)

    if dist <= p1.size+p2.size:
        theta = math.pi
        masa_total = p1.masa + p2.masa 
        #El angulo de contacto para dos bolas es pi/2
        v1Finalx = ((p1.velocidad[0]*math.cos(p1.velocidad[1]-theta)*(p1.masa - p2.masa)+2*p2.masa*p2.velocidad[0]*math.cos(p2.velocidad[1]-theta))/masa_total)*math.cos(theta) + p1.velocidad[0]*math.sin(p1.velocidad[1]-theta)*math.cos(theta+math.pi/2)
        v1Finaly = ((p1.velocidad[0]*math.cos(p1.velocidad[1]-theta)*(p1.masa - p2.masa)+2*p2.masa*p2.velocidad[0]*math.cos(p2.velocidad[1]-theta))/masa_total)*math.sin(theta) + p1.velocidad[0]*math.sin(p1.velocidad[1]-theta)*math.sin(theta+math.pi/2)

        v2Finalx = ((p2.velocidad[0]*math.cos(p2.velocidad[1]-theta)*(p2.masa - p1.masa)+2*p1.masa*p1.velocidad[0]*math.cos(p1.velocidad[1]-theta))/masa_total)*math.cos(theta) + p2.velocidad[0]*math.sin(p2.velocidad[1]-theta)*math.cos(theta+math.pi/2)
        v2Finaly = ((p2.velocidad[0]*math.cos(p2.velocidad[1]-theta)*(p2.masa - p1.masa)+2*p1.masa*p1.velocidad[0]*math.cos(p1.velocidad[1]-theta))/masa_total)*math.sin(theta) + p2.velocidad[0]*math.sin(p2.velocidad[1]-theta)*math.sin(theta+math.pi/2)


        angle = theta - 0.5 * math.pi
        p1.x += math.sin(angle)*1
        p1.y -= math.cos(angle)*1
        p2.x -= math.sin(angle)*1
        p2.y += math.cos(angle)*1
        
        p1.velocidad = transformaAngular([v1Finalx, v1Finaly])
        p2.velocidad = transformaAngular([v2Finalx, v2Finaly])

        p1.velocidad[0]*=ELASTICIDAD
        p1.velocidad[0]*=ELASTICIDAD

    
        

class Particula:

    ''' Particula '''
    # Fuerzas Sobre el Particula
    vectorFuerzas = [0, 0]
    def __init__(self, masa, velocidad, color, coords, sizeObj):
        self.masa = masa #
        self.velocidad = velocidad # (r, theta)
        self.size = int(sizeObj)
        self.color = color
        #self.reboto = 0
        #self.acel
        #self.image = pygame.Surface(self.radio)
        #self.image.fill(color)
        #Referencia hacia la imagen rectangular
        #self.rect = self.image.get_rect()
        self.x = coords[0]
        self.y = coords[1]
        #self.largo = largo
        #self.ancho = ancho
    
    def display(self):
        pygame.draw.circle(PANTALLA, self.color,[int(self.x), int(self.y)] , self.size)

    def update(self):
        '''Updatear el estado de la bola'''

        #Efectos gravitacionales
        self.calcGrav()
        
        #print(self.vectorFuerzas)
        #Efectos de viento

        #self.fuerzaViento(VIENTO)

        #Calcula movimiento
        
        
        self.calculaMovimiento()
        self.colision()

        
        #if self.velocidad[0]<0.09:
        #    self.velocidad[0]=1
       
        
        self.vectorFuerzas = [0, 0]


    def calcGrav(self):
        self.vectorFuerzas = sumaFuerzas(self.vectorFuerzas, [0, 1.2])

    def fuerzaViento(self, viento):
        self.vectorFuerzas = sumaFuerzas(self.vectorFuerzas, transformaCartesiano(viento))
    
    def colision(self):
        #Colision derecha
        if self.x >= LARGO- self.size:
            self.x = 2*(LARGO-self.size)-self.x
            self.velocidad[1] = math.pi - self.velocidad[1]
            self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico
            
            
        #Colision izquierda
        if  self.x <= self.size:
            self.x = 2*self.size - self.x
            self.velocidad[1] = math.pi - self.velocidad[1]
            self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico

        #colision  abajo
        if self.y >= ALTO - self.size:
            self.y = 2*(ALTO-self.size)-self.y
            self.velocidad[1] =  self.velocidad[1] - math.pi
            self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico
                
        #colision arriba
        if  self.y <= self.size :
            self.y = 2*self.size - self.y
            self.velocidad[1] =  self.velocidad[1] - math.pi
            self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico

    def dragg(self):
        self.velocidad[0]*=DRAGG
            
    
    def calculaMovimiento(self):
        #PARCHE PARA LA GRAVEDAD
        # DEPRECATED
       
            
        dvx, dvy = [self.vectorFuerzas[0]/(self.masa), self.vectorFuerzas[1]/(self.masa)]
        

        
        vCarte = transformaCartesiano(self.velocidad)
        vCarte[0] += dvx
        vCarte[1] += dvy

        self.velocidad = transformaAngular(vCarte)
        dx, dy = vCarte
        self.x += dx
        self.y += dy
        
        self.dragg()
        





        

        




tamanoPantalla = (LARGO, ALTO)
PANTALLA = pygame.display.set_mode(tamanoPantalla)
PANTALLA.fill((0, 0, 0))

#pelotita = Particula(10, (10, 3*math.pi/2), (150, 150))
#pelotita = Particula(1, [random.randint(1,20), random.uniform(0,2*math.pi)], (0,255,255), [50,50], (random.randint(10, 40), random.randint(10, 40)))
#pelotita2 = Particula(1, [random.randint(1,20), random.uniform(0,2*math.pi)], (255,255,0), [200,30], (random.randint(10, 40), random.randint(10, 40)))
#pelotita3 = Particula(1, [random.randint(1,20), random.uniform(0,2*math.pi)], (255,0,0), [200,80], (random.randint(10, 40), random.randint(10, 40)))

particulas = []
sumador = 0
numero_de_particulas = 10
for n in range(numero_de_particulas):
    sizePart = 20
    x = random.randint(sizePart, LARGO-sizePart)
    y = random.randint(sizePart, ALTO-sizePart)
    #x = 150 
    #y = 0 + sumador
    rVelocidad = random.randint(1, 5)
    #rVelocidad = 0
    thetaVelocidad = 0.1
    masaP = random.randint(10,30)
    colorP = (random.randint(30, 255), random.randint(30, 255), random.randint(30,255))

    sumador = sumador + sizePart*4
    particulas.append(Particula(masaP, [rVelocidad, thetaVelocidad], colorP, [int(x), int(y)], sizePart))


clock = pygame.time.Clock()



# Game Loop
while True:
    PANTALLA.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()    

    
    for i, particula in enumerate(particulas):
        particula.display()
        particula.update()
        #print(particula.velocidad)
        for particula2 in particulas[i+1:]:
            detectorColision(particula, particula2)

    
    #PANTALLA.blit(pelotita.image, pelotita.rect)
    #ANTALLA.blit(pelotita2.image, pelotita2.rect)
    #PANTALLA.blit(pelotita3.image, pelotita3.rect)
    #pelotita.vector = (random.randint(0, 10), random.uniform(0, 2*math.pi))
    #pelotita.vector = alpha

    #pelotita.update()
    #pelotita2.update()
    #pelotita3.update()
    
    
    
    #pygame.draw.rect(PANTALLA, color, pygame.Rect(x, y, largoAncho, largoAncho))
    
    pygame.display.flip()
    clock.tick(180)
    