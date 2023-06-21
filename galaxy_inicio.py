import pygame
from elements_v_3 import *
from configuracion import *
from archivos_galaxy import *
from variables_galaxy import *

# Inicialización de pygame
pygame.init()
puntaje = parse_puntaje(ruta)
lista_top5 = mostrar_top5(puntaje)
nombre = ''
font_input = pygame.font.SysFont("Arial", 24)
efecto_disparo = pygame.mixer_music.load("alien_9.mp3") 
sonido_impacto = pygame.mixer.Sound("sonido_impacto.mp3")
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos, 100)
clock = pygame.time.Clock()
lista_inicial = []
lista_ordenada = []
mostrar_ranking = False
correr = False
pantalla_inicio = True
pantalla_salida = False
principal = True
# Bucle principal
while principal:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           principal = False
        if pantalla_inicio:
            ventana.fill(colores.NEGRO)
            # Renderizar y mostrar los botones
            imagen_logo.mostrar(ventana)
            boton_play.mostrar(ventana)
            boton_ranking.mostrar(ventana)
            # Renderizar y mostrar el campo de entrada de texto para el nombre
            pygame.draw.rect(ventana, colores.CELESTE, nombre_rect, 2)
            font_input_nombre = font_input.render(nombre, True, colores.VERDEFLUOR)
            ventana.blit(font_input_nombre, (nombre_rect.x + 5, nombre_rect.y + 5))     
            if mostrar_ranking:
               ver_ranking(lista_top5,ventana)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.rect_colision.collidepoint(event.pos):
                    correr = True
                    pantalla_inicio = False
                if boton_ranking.rect_colision.collidepoint(event.pos):
                    mostrar_ranking = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode       
    if correr:
        # Aquí comienza el juego     
        pantalla.fill(colores.NEGRO)
        y_relativa = y % imagen_fondo.get_rect().height
        pantalla.blit(imagen_fondo, (x, y_relativa - imagen_fondo.get_rect().height))
        if y_relativa < ALTO_VENTANA:
            pantalla.blit(imagen_fondo, (x, y_relativa))
        y += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
                principal = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    nave.disparar()
                    pygame.mixer_music.play()
            if evento.type == pygame.USEREVENT:
                if evento.type == timer_segundos:                                       
                    nave_enemiga.mover_naves_enemigas(lista_naves_enemigas, ALTO_VENTANA)
                    for ovni in lista_ovnis:
                        ovni.mover_ovnis(lista_ovnis, ANCHO_VENTANA)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            nave.mover_der(ANCHO_VENTANA)
        if keys[pygame.K_LEFT]:
            nave.mover_izq()
        if keys[pygame.K_UP]:
            nave.mover_up(ALTO_VENTANA)
        if keys[pygame.K_DOWN]:
            nave.mover_down(ALTO_VENTANA)

        if len(lista_naves_enemigas) == 5:
            lista_naves_enemigas = Enemigo.crear_lista_naves(ruta_nave_enemiga, medidas_enemigo, 10)
       
        nave.mostrar(pantalla)
        nave_enemiga.mostrar(pantalla, lista_naves_enemigas)

        for ovni in lista_ovnis:
            ovni.mostrar(pantalla)
            ovni.disparar()
            ovni.actualizar_disparos(ALTO_VENTANA, nave, sonido_impacto)
            ovni.mostrar_disparos(pantalla)
        
        actualizar_pantalla(lista_naves_enemigas, pantalla, nave)

        for bala in nave.lista_balas:
            if bala.disparo_activo:
                bala.mover(ALTO_VENTANA)
                bala.mostrar_disparo(pantalla)

        actualizar_vida(ovni.lista_balas, nave)
        barra_vida(pantalla, 680, 0, nave.vida)
      
        font = pygame.font.SysFont("Arial Narrow", 30)
        tiempo = font.render("TIEMPO: {0}".format(SEGUNDOS), True, colores.ROJO)
        pantalla.blit(tiempo, (340, 0))
        conteo += 1
        if conteo == 56:
            conteo = 0
            SEGUNDOS -= 1
        if nave.vida <= 0 or SEGUNDOS == 0:
                correr = False
                pantalla_salida = True

        if pantalla_salida:
            pantalla.fill(colores.NEGRO)       
            texto_game_over = font.render("Game Over", True, colores.BLANCO)
            texto_rect = texto_game_over.get_rect(center=(ANCHO_VENTANA / 2, ALTO_VENTANA / 2))
            pantalla.blit(texto_game_over, texto_rect)
            lista_inicial = agregar_jugador(puntaje,nombre,nave.puntaje)
            lista_ordenada = sorted(lista_inicial, key=lambda i: i['puntos'], reverse=True)      
            guardar_json(ruta,lista_ordenada)
            pygame.display.flip()
            clock.tick(60)
        # Actualizar la ventana
    pygame.display.flip()
    #clock.tick(60)
pygame.quit()