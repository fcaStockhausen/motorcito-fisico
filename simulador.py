""" UWU """
import math
import random
import pygame

from funciones import *
from vectores import Vector2D
from pygame.locals import *
from pygame.color import THECOLORS

## IDEAS
## Agregar viento
## Tomar en cuenta aerodinamicidad de la cuestion
# Monitorizar estado de las bolas haciendoles click
# Velocidad
# Angulo
# Posicion
# Podria mostrar una representacion grafica del vector velocidad

# todu: 
# calcular dt_s
# Agregar texto y interaccion con el click del mouse (o seleccion por teclado)
# Hacer de mejor manera la creacion de las bolas (mejor interfaz)
# Agregar color según masa



############################################################
#
#                  -------------------->x
#                  |
#                  |
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
LARGO = 500
ALTO = 500
COEFICIENTE_CLOCK = 7,63 # CALCULAR, este esta mal
VIENTO = (5, 3*math.pi/4)
GRAVEDAD = (10, 3*math.pi/2)
ELASTICIDAD = 1
DRAGG = 1



        


class Particula:

    ''' Particula '''
    # Fuerzas Sobre el Particula
    vectorFuerzas = [0, 0]
    def __init__(self, masa, velocidad, coords_px, sizeObj, color):
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
        self.x = coords_px[0]
        self.y = coords_px[1]
        #self.largo = largo
        #self.ancho = ancho
    
    def display(self):
        pygame.draw.circle(mundo.pantalla, self.color, [int(self.x), int(self.y)] , self.size)


    def update(self, dt_s):
        '''Updatear el estado de la bola'''

        #Efectos gravitacionales
        if mundo.gravedad_on:
            self.calcGrav()
        
        #print(self.vectorFuerzas)

        #Efectos de viento
        if mundo.viento_on:
            self.fuerzaViento(VIENTO)

        #Calcula movimiento
        
        
        self.calculaMovimiento(dt_s)
        self.colision()

        
        #if self.velocidad[0]<0.09:
        #    self.velocidad[0]=1
       
        
        self.vectorFuerzas = [0, 0]


    def calcGrav(self):
        self.vectorFuerzas = sumaFuerzas(self.vectorFuerzas, [0, 10*self.masa])

    def fuerzaViento(self, viento):
        self.vectorFuerzas = sumaFuerzas(self.vectorFuerzas, transformaCartesiano(viento))
    
    def colision(self):
        #Colision derecha
        if self.x >= LARGO- self.size:
            self.x = 2*(LARGO-self.size)-self.x
            self.velocidad[1] = math.pi - self.velocidad[1]
            #self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico
            
            
        #Colision izquierda
        if  self.x <= self.size:
            self.x = 2*self.size - self.x
            self.velocidad[1] = math.pi - self.velocidad[1]
            #self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico

        #colision  abajo
        if self.y >= ALTO - self.size:
            self.y = 2*(ALTO-self.size)-self.y
            self.velocidad[1] =  - self.velocidad[1] 
            #self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico
                
        #colision arriba
        if  self.y <= self.size :
            self.y = 2*self.size - self.y
            self.velocidad[1] =   - self.velocidad[1]
            #self.velocidad[0] = self.velocidad[0]*ELASTICIDAD #Inelastico

    def dragg(self):
        self.velocidad[0]*=DRAGG
            
    
    def calculaMovimiento(self, dt_s):
        #PARCHE PARA LA GRAVEDAD
        # DEPRECATED
        # RECALCULAR TODAS LAS VELOCIDADES
        # USANDO dt_s

        # V_f = dt_s 
       
            
        accelx, accely  = [self.vectorFuerzas[0]/(self.masa), self.vectorFuerzas[1]/(self.masa)]
        

        # V cartesiano = V_Objeto 
        vCarte = transformaCartesiano(self.velocidad)
        
        # Vfinal = V_act + a*Dt
        vFinal = [vCarte[0] + accelx*dt_s, vCarte[1] + accely*dt_s]

        # Velocidad promedio
        vProm = sumaFuerzas(vFinal, vCarte)
        vProm = [vProm[0]/2.0, vProm[1]/2.0]

        # D x_t = D_t * V_prom
        self.x += vProm[0]*dt_s 
        self.y += vProm[1]*dt_s


        self.velocidad = transformaAngular(vFinal)
        
        self.dragg()


class Mundo:
    def __init__ (self, tamanoPantalla, m_per_px , px_per_m, color=THECOLORS["black"]):
        self.ancho_px, self.alto_px = tamanoPantalla
        self.m_per_px = float(m_per_px)
        self.px_per_m = int(px_per_m)
        self.ancho_m, self.alto_m = self.ancho_px * self.m_per_px, self.alto_px * self.m_per_px
        self.mostrar_stats_on = 0
        self.viento_on = 0
        self.gravedad_on = 0

        
        
    
    def init_pantalla(self):
        self.pantalla = pygame.display.set_mode([self.ancho_px, self.alto_px])
     
    def update_pantalla(self):
        self.pantalla.fill(THECOLORS['black'])
        if self.mostrar_stats_on:
            self.mostrar_stats()
    
    def get_user_input(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT): 
                    termina = 1
            elif (event.type == pygame.KEYDOWN):
                if event.key == K_1:
                    return 1
                if event.key == K_2:
                    return 2
                if event.key == K_3:
                    return 3
                if event.key == K_o:
                    return 'o'
                if event.key == K_ESCAPE:
                    return 0
                if event.key == K_s:
                    return 's'
                ### ACA ###

    
    # Tamanho particulas 
    def crear_particulas(self, numero_de_particulas, size_particulas_m=1, r_vel_mps=0.0, theta_mps=0.0, masa_part=1, color=THECOLORS['white']):
        self.coleccion_particulas = []
        for n in range(numero_de_particulas):
            print("PARTICULA CREADA")
            position_x_px = random.randint(int(size_particulas_m), self.ancho_px - size_particulas_m * self.px_per_m)
            position_y_px = random.randint(int(size_particulas_m), self.alto_px - size_particulas_m * self.px_per_m)
            self.coleccion_particulas.append(Particula(masa_part, [r_vel_mps, theta_mps], [position_x_px, position_y_px], size_particulas_m*self.px_per_m, color))

    def crea_particula(self, mouse_pos):
        self.coleccion_particulas.append(Particula(10, [0, 0], mouse_pos, 10*self.px_per_m, THECOLORS['white']))

    def mostrar_stats(self):
        font = pygame.font.SysFont('comicsans', 20)
        ### MOSTRAR FUERZAS SI EXISTEN, DRAGG, ELASTICIDAD ###


        string = "Elasticidad: "+ str(ELASTICIDAD) + " Dragg: " + str(DRAGG)  # DEBE HABER UNA MEJOR FORMA DE IMPLEMENTARLO
        

        text = font.render(string,1, THECOLORS['green'])
        
        textRect = text.get_rect()
        textRect = text.get_rect()
        textRect.x = 0
        textRect.y = 0
        self.pantalla.blit(text, textRect)


        

# FUNCIONES MOVIDAS A MODULO EXTERNO
def calcularColor(masa):
    valorColor = int(97*math.log(masa) + 30)
    return (0, valorColor, 0)


def detectorColision(p1,p2):

    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)

    if dist <= p1.size+p2.size:
        theta =  math.atan2(dy, dx) 
        masa_total = p1.masa + p2.masa 
        #El angulo de contacto para dos bolas es pi/2
        v1Finalx = ((p1.velocidad[0]*math.cos(p1.velocidad[1]-theta)*(p1.masa - p2.masa)+2*p2.masa*p2.velocidad[0]*math.cos(p2.velocidad[1]-theta))/masa_total)*math.cos(theta) + p1.velocidad[0]*math.sin(p1.velocidad[1]-theta)*math.cos(theta+math.pi/2)
        v1Finaly = ((p1.velocidad[0]*math.cos(p1.velocidad[1]-theta)*(p1.masa - p2.masa)+2*p2.masa*p2.velocidad[0]*math.cos(p2.velocidad[1]-theta))/masa_total)*math.sin(theta) + p1.velocidad[0]*math.sin(p1.velocidad[1]-theta)*math.sin(theta+math.pi/2)

        v2Finalx = ((p2.velocidad[0]*math.cos(p2.velocidad[1]-theta)*(p2.masa - p1.masa)+2*p1.masa*p1.velocidad[0]*math.cos(p1.velocidad[1]-theta))/masa_total)*math.cos(theta) + p2.velocidad[0]*math.sin(p2.velocidad[1]-theta)*math.cos(theta+math.pi/2)
        v2Finaly = ((p2.velocidad[0]*math.cos(p2.velocidad[1]-theta)*(p2.masa - p1.masa)+2*p1.masa*p1.velocidad[0]*math.cos(p1.velocidad[1]-theta))/masa_total)*math.sin(theta) + p2.velocidad[0]*math.sin(p2.velocidad[1]-theta)*math.sin(theta+math.pi/2)

        p1.velocidad = transformaAngular([v1Finalx, v1Finaly])
        p2.velocidad = transformaAngular([v2Finalx, v2Finaly])

        p1.velocidad[0]*=ELASTICIDAD
        p1.velocidad[0]*=ELASTICIDAD


        

        angle = 0.5*math.pi + theta
        p1.x += math.sin(angle)*1.5
        p1.y -= math.cos(angle)*1.5
        p2.x -= math.sin(angle)*1.5
        p2.y += math.cos(angle)*1.5


def main():
    global mundo, left_mouse_click, termina
    left_mouse_click = 0

    pygame.init() # Inicializacion
    pygame.font.init() # Inicialización de fuentes
    
    mundo = Mundo([500, 500], 1, 1)
    mundo.init_pantalla()

    clock = pygame.time.Clock()
    framerate_limit = 400
    

    # Calculo del tiempo
    tiempo_s = 0.0 

    # 
    Mx, My = 0, 0
    # Game Loop
    # Seleccionada
    particula_seleccionada = None

    # Crear particulas
    mundo.crear_particulas(2, 20)
    
    termina = 0
    while not termina:
        #Borrar todo
        mundo.update_pantalla()

        # Recoleccion de eventos
        
        user_input = mundo.get_user_input()

        # Acciones a hacer por el click

        if user_input == 0:
            termina = 1
        elif user_input == 1: #
            mouse_pos = pygame.mouse.get_pos()
            mundo.crea_particula(mouse_pos) # que caracteristicas? HACER SUBMENUU
        elif user_input == 2:
            mundo.gravedad_on = 1
        elif user_input == 3:
            mundo.viento_on = 1
        elif user_input == 's':
            mundo.mostrar_stats_on = 1

        #if left_mouse_click:
        #    mouse_pos = pygame.mouse.get_pos()
        #    if user_input == 0:
        #        print(user_input)
        #    elif user_input == 1: #
        #        print(user_input)
        #        mundo.crea_particula(mouse_pos) # que caracteristicas? HACER SUBMENUU
        #    elif user_input == 2:
        #        print(user_input)
 


        # delta de tiempo
        dt_s = float(clock.tick(framerate_limit)*1e-3*8)
        
        
        for i, particula in enumerate(mundo.coleccion_particulas):
            particula.display()
            particula.update(dt_s)
            #print(particula.velocidad)¡
            for particula2 in mundo.coleccion_particulas[i+1:]:
                detectorColision(particula, particula2)

        
        tiempo_s += dt_s
        pygame.display.flip()   
        #180



    #tamanoPantalla = (LARGO, ALTO)
    #PANTALLA = pygame.display.set_mode(tamanoPantalla)
    #PANTALLA.fill((100, 0, 100))
    #
    #particulas = []
    #sumador = 0
    #numero_de_particulas =  10
    #for n in range(numero_de_particulas):
    #    sizePart = 10
    #    x = random.randint(sizePart, LARGO-sizePart)
    #    y = random.randint(sizePart, ALTO-sizePart)
    #    #x = 150 
    #    #y = 0 + sumSador
    #    #rVelocidad = random.randint(20, 30)
    #    #rVelocidad = 0
    #    #thetaVelocidad = random.uniform(0,2*math.pi)
    #    masaP = random.randint(1, 10)
    #    colorP = (random.randint(30, 255), random.randint(30, 255), random.randint(30,255))
    #
    #    sumador = sumador + sizePart*4
    #    particulas.append(Particula(masaP, [rVelocidad, thetaVelocidad], colorP, [int(x), int(y)], sizePart))

main()