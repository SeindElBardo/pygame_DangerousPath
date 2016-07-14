#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *
import random
 
# Constantes
WIDTH = 640
HEIGHT = 480
DERECHA = 425
IZQUIERDA = 215
CENTRO = 320
ACELERACION = 1.0019


 
# Clases
# ---------------------------------------------------------------------
 
#Shit, la nave es el objeto con el que jugará el jugador.
#Se situa en la parte central inferior de la pantalla y tiene 3 posiciones: centro, derecha e izquierda.
class Shit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/shit.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = CENTRO
        self.rect.centery = HEIGHT-47

    def mover(self, keys):        
        if keys[K_a]:
            self.rect.centerx = IZQUIERDA    
        elif keys[K_d]:
            self.rect.centerx = DERECHA
        else:
            self.rect.centerx = CENTRO
 
 
#Obstaculo, a lo largo del juego apareceran lineas de obstaculos que descenderán hacia el jugador y deberán ser esquivadas.
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/obstaculo.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos
        self.rect.centery = 2

    def actualizar(self, time, shit, speed):
        self.rect.centery += time * speed
        if self.rect.centery <=  HEIGHT+100: #Los obstaculos han sido esquivados, por lo que se eliminan
            self.kill()
        if pygame.sprite.collide_rect(self, shit):
            sys.exit(0) #Paso de pantalla de game over
            a=3 
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
 
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

def generarObstaculos(listaObstaculos):
    opcion = random.randrange(6)
    if opcion == 0:
        listaObstaculos.append(Obstaculo(DERECHA))
    if opcion == 1:
        listaObstaculos.append(Obstaculo(CENTRO))
    elif opcion == 2:
        listaObstaculos.append(Obstaculo(IZQUIERDA))
    elif opcion == 3:
        listaObstaculos.append(Obstaculo(DERECHA))
        listaObstaculos.append(Obstaculo(CENTRO))
    elif opcion == 4:
        listaObstaculos.append(Obstaculo(DERECHA))
        listaObstaculos.append(Obstaculo(IZQUIERDA))
    elif opcion == 5:
        listaObstaculos.append(Obstaculo(CENTRO))
        listaObstaculos.append(Obstaculo(IZQUIERDA))

def actualizarObstaculos(listaObstaculos, time, shit, speed):
    for obstaculo in listaObstaculos:
        obstaculo.actualizar(time, shit, speed)

def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("images/DroidSans.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect        
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DangerousPath")
 
    background_image = load_image('images/fondo_DP.png')
    shit = Shit()
    
    clock = pygame.time.Clock()
    listaObstaculos = []
    nuevoObstaculo = 0 #Usaremos esta variable para saber cuando generar una nueva linea de obstáculos
    speed = 0.6
    
    puntuacion = 0
    generarObstaculos(listaObstaculos)

    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
 
        actualizarObstaculos(listaObstaculos, time, shit, speed)
        shit.mover(keys)
        puntos, puntos_rect = texto(str(puntuacion), 80, 40)
        if nuevoObstaculo > 300:
            generarObstaculos(listaObstaculos)
            nuevoObstaculo = 0
            puntuacion += 1
            if speed < 1.1:
                speed *= ACELERACION    #Aceleramos
        else:
            nuevoObstaculo += time * speed
            if len(listaObstaculos) > 9: #Nos aseguramos de ir retirando los objetos fuera de juego de la lista
                listaObstaculos.pop(0)
        screen.blit(background_image, (0, 0))
        screen.blit(puntos, puntos_rect)
        screen.blit(shit.image, shit.rect)
        for obstaculo in listaObstaculos:
            screen.blit(obstaculo.image, obstaculo.rect)
        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()