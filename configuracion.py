import pygame
from elements_v_3 import *
from variables_galaxy import *
ruta = "galaxy.json"
nombre_rect = pygame.Rect(325, 320, 150, 40)
boton_play = Boton("imagen_boton_play.png", [150, 70], 325, 220)
boton_ranking = Boton("imagen_ranking.png", [150, 70], 325, 260)
imagen_logo = Boton("imagen_logo.png", [500, 250], 150, 0)
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
nave = Nave("nave5.png", [62, 50], ANCHO_VENTANA/2, 520)
# Creación de naves enemigas
ruta_nave_enemiga = "nave_araña.png"
nave_enemiga = Enemigo(ruta_nave_enemiga, medidas_enemigo, 0, 0)
lista_naves_enemigas = Enemigo.crear_lista_naves(ruta_nave_enemiga, medidas_enemigo, 20)
ruta_ovni = "ovni.png"
lista_ovnis = Ovni.crear_lista_ovnis(10, ruta_ovni, medidas_ovni) 
# Crear la ventana de juego
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Galaxy Game")
imagen_fondo = pygame.image.load("fondo_galaxy.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

