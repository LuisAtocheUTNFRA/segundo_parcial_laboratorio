import pygame
import colores
import random
from variables_galaxy import *

class Nave:
    def __init__(self, ruta, medidas, x, y):
        self.imagen = pygame.image.load(ruta)
        self.imagen = pygame.transform.scale(self.imagen, medidas)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.puntaje = 0
        self.vida = 100
        self.lista_balas = []

    def mostrar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def mover_up(self, ALTO_VENTANA):
        if self.rect.top > ALTO_VENTANA/2:
            self.rect.y -= 5      

    def mover_down(self, ALTO_VENTANA):
        if self.rect.bottom < ALTO_VENTANA:
            self.rect.y += 5 

    def mover_der(self, ANCHO_VENTANA):
        if self.rect.right < ANCHO_VENTANA:
            self.rect.x += 5

    def mover_izq(self):
        if self.rect.left > 0:
            self.rect.x -= 5  

    def disparar(self):      
        bala = Disparos(self.rect.centerx, self.rect.y,"disparo.png",[10,20],True)
        self.lista_balas.append(bala)              
        bala.disparo_activo = True

class Enemigo:
    def __init__(self, ruta, medidas, x, y):
        self.imagen = pygame.image.load(ruta)
        self.imagen = pygame.transform.scale(self.imagen, medidas)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 20

    def mostrar(self, pantalla, lista):
        for nave in lista:
            pantalla.blit(nave.imagen, nave.rect)
    
    def crear_lista_naves(ruta, medidas, cantidad):
        lista_naves = []
        for _ in range(cantidad):
            x = random.randint(0, 755)
            y = random.randint(-600, 0)
            lista_naves.append(Enemigo(ruta, medidas, x, y))
        return lista_naves

    def mover_naves_enemigas(self, lista, ALTO_VENTANA):
        for nave in lista:
            if nave.rect.y < ALTO_VENTANA: 
                nave.rect.y += self.velocidad
            else:
                nave.rect.y = 0   
 
class Ovni(Enemigo):
    def __init__(self, ruta, medidas, x, y):
        super().__init__(ruta, medidas, x, y)
        self.lista_balas = [] 
    
    def mostrar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def crear_lista_ovnis(cantidad, ruta, medidas):
        lista_naves = []
        for _ in range(cantidad):
            x = random.randint(0, 755)
            y = random.randint(0, 250)
            lista_naves.append(Ovni(ruta, medidas, x, y))
        return lista_naves
    
    def mover_ovnis(self,lista,ANCHO_VENTANA):
        for ovni in lista:
            if ovni.rect.x < ANCHO_VENTANA: 
               ovni.rect.x = ovni.rect.x + 5
            else:
                ovni.rect.right = 0 
                
    def disparar(self):
        if random.randint(1, 1000) <= 3: 
            bala = Disparos(self.rect.centerx, self.rect.bottom,"proyectil_rojo.png",[20,40],False)
            bala.velocidad = 5 
            bala.disparo_activo = True
            self.lista_balas.append(bala)

    def actualizar_disparos(self, ALTO_VENTANA, nave,sonido_impacto):
        for bala in self.lista_balas:
            if bala.disparo_activo:
                if bala.rect.y < ALTO_VENTANA:
                    bala.rect.y += self.velocidad
                    if bala.rect.colliderect(nave.rect):
                        bala.disparo_activo = False
                        nave.vida -= 10
                        sonido_impacto.play()
                else:
                    self.disparo_activo = False

    def mostrar_disparos(self, pantalla):
        for bala in self.lista_balas:
            if bala.disparo_activo:
                bala.mostrar_disparo(pantalla)        

class Disparos:
    def __init__(self, x, y,ruta,medidas,flag):
        self.imagen = pygame.image.load(ruta)
        self.imagen = pygame.transform.scale(self.imagen, medidas)
        if not flag:
            self.imagen = pygame.transform.rotate(self.imagen,180)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.y = y        
        self.disparo_activo = False
        self.velocidad = 10 
   
    def mover(self, ALTO_VENTANA):             
        if self.rect.y < ALTO_VENTANA:                     
            self.rect.y -= self.velocidad         
        if self.rect.y <= 0:    
            self.disparo_activo = False

    def mostrar_disparo(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class Boton:
    def __init__(self, ruta, medidas, x, y):
        self.imagen = pygame.image.load(ruta)
        self.imagen = pygame.transform.scale(self.imagen, medidas)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_colision = pygame.Rect(self.rect.left+15,self.rect.top+20,125,28)

    def mostrar(self, pantalla):
        #pygame.draw.rect(pantalla,colores.VERDEFLUOR,self.rect_colision)
        pantalla.blit(self.imagen, self.rect)
    

def actualizar_pantalla(enemigos, pantalla, nave):
    for enemigo in enemigos:
        for bala in nave.lista_balas:
            if bala.disparo_activo:
                if bala.rect.colliderect(enemigo.rect):
                    nave.puntaje += 100
                    enemigos.remove(enemigo)
                    bala.disparo_activo = False

    font = pygame.font.SysFont("Arial Narrow", 30)
    text = font.render("PUNTOS: {0}".format(nave.puntaje), True, colores.ROJO)
    pantalla.blit(text, (20, 0))
    
def barra_vida(pantalla,x,y,nivel_vida):
    ancho = 100
    alto = 20
    fill = int((nivel_vida/100) * ancho)
    border = pygame.Rect(x,y,ancho,alto)
    fill = pygame.Rect(x,y,fill,alto)  
    pygame.draw.rect(pantalla,colores.ROJO,fill)  
    pygame.draw.rect(pantalla,colores.BLANCO,border,2) 

def actualizar_vida(lista_balas,nave):
    for bala in lista_balas:
        if bala.disparo_activo:
            if bala.rect.colliderect(nave.rect):
                lista_balas.remove(bala)
                nave.vida -= 5

def ver_ranking(puntaje,ventana):
    for i in range(len(puntaje)):
        font_nombre = pygame.font.SysFont("Arial", 24)
        texto_nombre = font_nombre.render(puntaje[i]["nombre"], True, colores.BLANCO)
        ventana.blit(texto_nombre, (LEFT_TEXTO, TOP_TEXTO + (i * 25)))

        font_puntos = pygame.font.SysFont("Arial", 24)
        texto_puntos = font_puntos.render(str(puntaje[i]["puntos"]), True, colores.BLANCO)
        ventana.blit(texto_puntos, (LEFT_TEXTO * 1.5, TOP_TEXTO + (i * 25))) 


    
        


                      