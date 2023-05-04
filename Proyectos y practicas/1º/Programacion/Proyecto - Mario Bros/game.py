import pyxel
from clases.atrezzo.atrezzo import atrezzo
from clases.bloques.bloque import bloque
from clases.bloques.suelo import suelo
from clases.bloques.escalera import escalera
from clases.bloques.ladrillo_con_monedas import ladrillo_con_monedas
from clases.bloques.ladrillo_rompible import ladrillo_rompible
from clases.bloques.tuberia import tuberia
from clases.bloques.invisible import bloque_invisible
from clases.bloques.interrogacion import interrogacion
from clases.bloques.lanzabill import cañon_lanza_bills
from clases.atrezzo.castillo import castillo
from clases.objetos.moneda import moneda
from clases.objetos.champi import champi
from clases.objetos.champiverde import champi_verde
from clases.objetos.estrella import estrella
from clases.objetos.flor import flor
from clases.objetos.bandera import bandera
from clases.atrezzo.mastil import mastil
from clases import player
from clases.npcs.goompa import goomba
from clases.npcs.koopa_troopa import koopa_troopa
from clases.npcs.bala import bill_bala
from clases.atrezzo.montaña import montaña
from clases.atrezzo.nube import nube
from clases.atrezzo.arbusto import arbusto
import random

import constants as c
class game():
    def __init__(self) -> None:
        pyxel.init(c.ancho_pantalla, c.alto_pantalla, caption="Cañerias Mariano", fps=c.fps)
        pyxel.load(c.assets_path)
        self.en_menu = True
        self.tiempo = c.tiempo # contador de la esquina superior derecha
        self.jugador = player.mario([1500, c.altura_suelo-35])
        self.__generar_bloques()
        self.__generar_suelo()
        self.__generar_npcs()
        self.__generar_objetos()
        self.__generar_atrezzo()
        self.__posicion_mario = 105
        self.__animacion = False
        pyxel.run(self.update,self.draw)
    @property
    def posicion_mario(self):
        return self.__posicion_mario 
    @posicion_mario.setter
    def posicion_mario(self,new_posicion_mario):
        self.posicion_mario = new_posicion_mario 
    @property
    def animacion(self):
        return self.__animacion 
    @animacion.setter
    def animacion(self,new_animacion):
        self.__animacion = new_animacion  
         
    
    def update(self):
        if self.en_menu: # comprueba si estamos en el menu de inicio para que no se ejecute el nivel
            if pyxel.btnp(pyxel.KEY_ENTER):
                self.__animacion = True
            if self.__animacion:
                self.animacion_de_inicio()
        elif self.jugador.muerto:  # comprueba si estamos en el menu de muerte para que no se ejecute el nivel
            if self.jugador.vidas <= 0:  # si no te quedan vidas reinicia el juego entero
                if pyxel.btnp(pyxel.KEY_ENTER):
                    self.reset_game()
            if pyxel.btnp(pyxel.KEY_ENTER):  # reinicia el nivel
                self.reset_level()
                self.jugador.muerto=False
        elif self.tiempo < 0:  # mueres si te quedas sin tiempo
            self.jugador.morir()

        else: # ejecucion normal del nivel tras comprobar que no estamos en un menu
            self.jugador.actualizar_estado(self.__bloques,self.npcs,self.objetos,self.jugador)
            self.__borrar_entidades(self.__bloques, self.npcs, self.objetos,self.atrezzo)
            self.__mantener_jugador_en_pantalla()
            for npc in self.npcs: # actualiza a los npcs uno por uno
                npc.actualizar_estado(self.__bloques , (other_npc for other_npc in self.npcs if other_npc != npc),self.objetos,self.jugador ) # hay que excluir al propio npc
            for bloque in self.__bloques: # actualiza los bloques uno por uno
                bloque.reposicionar()
                if (pyxel.frame_count) % (c.fps) == 0:
                    self.generar_balas(bloque)

            for objeto in self.objetos:  # actualiza los objetos uno por uno
                objeto.actualizar(self.__bloques)
            if not self.jugador.en_bandera:
                self.tiempo -= 1 if pyxel.frame_count%c.fps==0 else 0 # actualiza el contador de la derecha

            if self.jugador.juego_finalizado and pyxel.btnp(pyxel.KEY_ENTER): # reinicia al llegar al final del juego
                self.reset_game()
    
    def draw(self):
        if self.en_menu: #si estas en el menu de inicio dibuja solo el menu de inicio
            pyxel.cls(c.azul)
            pyxel.blt(0,0,*c.sprite_cartel)
            pyxel.blt(122,self.posicion_mario,*c.sprite_mario_quieto)
            pyxel.blt(112,120,*c.tuberia(25,True))
        elif self.jugador.muerto:  # si estas en el menu de muerte dibuja solo el menu de muerte
            pyxel.cls(c.negro)
            if self.jugador.vidas <= 0: # si te has quedado sin vidas muestra la pantalla para reiniciar el juego
                pyxel.blt(108,80,*c.game_over)
                pyxel.text(pyxel.width/2+c.ancho_mario+3, pyxel.height/2+70,"pulsa intro para reiniciar",c.blanco)
            else:  # si  no te has quedado sin vidas muestra la pantalla para reiniciar el nivel
                pyxel.blt(pyxel.width/2,pyxel.height/2, *c.sprite_mario_quieto)
                pyxel.text(pyxel.width/2+c.ancho_mario+3, pyxel.height/2,"x  {}".format(self.jugador.vidas),c.blanco)
                pyxel.text(pyxel.width/2+c.ancho_mario+3, pyxel.height/2+15,"pulsa intro",c.blanco)
        else: # dibujado normal del nivel
            pyxel.cls(c.azul)
            #bloques, objetos, npcs y atrezzo
            for i in range(len(self.atrezzo)):
                if not self.atrezzo[i].coord[0]>1.5*pyxel.width:
                    pyxel.blt(self.__redondear(self.atrezzo[i].coord[0]),self.__redondear(self.atrezzo[i].coord[1]), *self.atrezzo[i].sprite)
            for i in range(len(self.objetos)):
                if not self.objetos[i].coord[0]>1.5*pyxel.width:
                    pyxel.blt(*self.objetos[i].coord, *self.objetos[i].sprite)
            for i in range(len(self.__bloques)):
                if not self.__bloques[i].coord[0]>1.5*pyxel.width and not self.__bloques[i].coord[0]<-self.__bloques[i].ancho:
                    pyxel.blt(self.__redondear(self.__bloques[i].coord[0]),self.__redondear(self.__bloques[i].coord[1]),*self.__bloques[i].sprite)
            for i in range(len(self.npcs)):
                if not self.npcs[i].coord[0]>1.5*pyxel.width:
                    pyxel.blt(*self.npcs[i].coord, *self.npcs[i].sprite)
            
            #el jugador
            pyxel.blt(*self.jugador.coord,*self.jugador.sprite)
            if self.jugador.estrella:# hace la animacion del brillo del modo estrella   
                if pyxel.frame_count % (c.fps/6) == 0:
                    pyxel.blt(self.jugador.coord[0], self.jugador.coord[1],
                              *c.sprite_animacion_estrella_amarillo(self.jugador.alto))
                if pyxel.frame_count % (c.fps/10) == 0:
                    pyxel.blt(self.jugador.coord[0], self.jugador.coord[1],
                              *c.sprite_estrella)
            
            #timer
            pyxel.text(pyxel.width-40, 10, "TIME",c.blanco)
            pyxel.text(pyxel.width-20,10,str(self.tiempo),c.blanco)
            #monedas
            pyxel.blt(100,9,*c.sprite_moneda_chiquita)
            pyxel.text(104, 13, "{:02d}".format(self.jugador.dinero), c.negro)
            #puntuacion mario
            pyxel.text(30, 10, "MARIO", c.blanco)
            pyxel.text(30, 20, "{:06d}".format(self.jugador.score), c.blanco)
            #vidas mario
            pyxel.blt(150,10, *c.sprite_mario_quieto)
            pyxel.text(170, 10,"x  {}".format(self.jugador.vidas),c.blanco)
        if self.jugador.juego_finalizado: # mensaje de final del juego
            pyxel.text(pyxel.width/4-20, pyxel.height/2-50,"GRACIAS POR JUGAR, PULSA INTRO PARA REINICIAR",c.blanco)
            

    def __generar_atrezzo(self):
        self.atrezzo = [
            castillo([3000, c.altura_suelo-c.alto_castillo]),
            montaña([20,c.altura_suelo-33]), montaña([500,c.altura_suelo-33]), 
            montaña([1150,c.altura_suelo-33]), montaña([1600,c.altura_suelo-33]),
            montaña([2300,c.altura_suelo-33]), montaña([3100,c.altura_suelo-33]),
            
            arbusto([200, c.altura_suelo-15]),arbusto([500, c.altura_suelo-15]),
            arbusto([600, c.altura_suelo-15]),arbusto([1870, c.altura_suelo-15]),
            arbusto([2400, c.altura_suelo-15]),arbusto([2600, c.altura_suelo-15]),
            arbusto([2920, c.altura_suelo-15]), mastil([2906, 20])
        
            
        ]
        for _ in range(20):
            self.atrezzo.append(nube([random.randint(0,3000),random.randint(0,100)])) 
       
    def __generar_objetos(self):
        self.objetos = [bandera([2896, 30])]
    
    def __generar_suelo(self):
        """el suelo son bloques, pero es comodo y visual generarlos a parte"""
        x = 0
        while x < 1000:
            self.__bloques.append(suelo([x, c.altura_suelo]))
            x += c.ancho_suelo
        
        x+=45
        while x < 1335:
            self.__bloques.append(suelo([x, c.altura_suelo]))
            x += c.ancho_suelo
        x += 60
        while x < 2002:
            self.__bloques.append(suelo([x, c.altura_suelo]))
            x += c.ancho_suelo
        x=2035
        while x < 3700:
            self.__bloques.append(suelo([x, c.altura_suelo]))
            x += c.ancho_suelo
    
    def __generar_bloques(self):
        self.__bloques = [
            #primera tanda de bloques
            cañon_lanza_bills([16,c.altura_suelo-16],1),cañon_lanza_bills([0,c.altura_suelo-24],1),
            bloque_invisible([0,c.altura_suelo-100]), tuberia([118,c.altura_suelo-c.alto_smario],c.alto_smario,True),
            interrogacion([256,c.altura_suelo-55],True),ladrillo_rompible([301,c.altura_suelo-55]),
            interrogacion([316, c.altura_suelo-55], True),ladrillo_rompible([331,c.altura_suelo-55]),
            interrogacion([346, c.altura_suelo-55], False),ladrillo_rompible([361,c.altura_suelo-55]),
            interrogacion([331, c.altura_suelo-110],True),
            # escaleras de tuberias
            tuberia([415, c.altura_suelo-c.alto_smario-3], c.alto_smario+3),
            tuberia([565, c.altura_suelo-c.alto_smario-20], c.alto_smario+20),
            tuberia([715, c.altura_suelo-c.alto_smario-25], c.alto_smario+25),
            tuberia([865, c.altura_suelo-c.alto_smario-25], c.alto_smario+25),
            #segunda tanda de bloques despues de la caida
            ladrillo_rompible([1200, c.altura_suelo-55]),interrogacion([1215, c.altura_suelo-55], False),
            ladrillo_rompible([1230, c.altura_suelo-55]),
            #los bloques que van por encima de los anteriores
            ladrillo_rompible([1245, c.altura_suelo-110]),ladrillo_rompible([1260, c.altura_suelo-110]),
            ladrillo_rompible([1275, c.altura_suelo-110]),ladrillo_rompible([1290, c.altura_suelo-110]),
            ladrillo_rompible([1305, c.altura_suelo-110]),ladrillo_rompible([1320, c.altura_suelo-110]),
            ladrillo_rompible([1335, c.altura_suelo-110]),ladrillo_rompible([1350, c.altura_suelo-110]),
            ladrillo_rompible([1365, c.altura_suelo-110]),
            #tercera tanda 
            ladrillo_rompible([1415, c.altura_suelo-110]),ladrillo_rompible([1430, c.altura_suelo-110]),
            ladrillo_rompible([1445, c.altura_suelo-110]),interrogacion([1460, c.altura_suelo-110],True),
            ladrillo_rompible([1460, c.altura_suelo-55]),
            # cuarta 
            ladrillo_rompible([1550, c.altura_suelo-55]),ladrillo_rompible([1565, c.altura_suelo-55],True),
            #quinta

            #sexta
            ladrillo_rompible([1550, c.altura_suelo-55]),ladrillo_rompible([1580, c.altura_suelo-110]),
            ladrillo_rompible([1595, c.altura_suelo-110]),ladrillo_rompible([1610, c.altura_suelo-110]),
            #septima
            ladrillo_rompible([1660, c.altura_suelo-55]),ladrillo_rompible([1675, c.altura_suelo-55]),
            interrogacion([1660, c.altura_suelo-110],True),interrogacion([1675, c.altura_suelo-110], False),
            ladrillo_rompible([1645, c.altura_suelo-110]),ladrillo_rompible([1690, c.altura_suelo-110]),
            #octava escaleras
            #subida
            escalera([1720,c.altura_suelo-c.alto_escalera],c.alto_escalera),
            escalera([1735,c.altura_suelo-2*c.alto_escalera],2*c.alto_escalera),
            escalera([1750,c.altura_suelo-3*c.alto_escalera],3*c.alto_escalera),
            escalera([1765,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            #bajada
            escalera([1810,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            escalera([1825,c.altura_suelo-3*c.alto_escalera],3*c.alto_escalera),
            escalera([1840,c.altura_suelo-2*c.alto_escalera],2*c.alto_escalera),
            #novena escaleras
            #subida
            escalera([1947,c.altura_suelo-2*c.alto_escalera],2*c.alto_escalera),
            escalera([1962,c.altura_suelo-3*c.alto_escalera],3*c.alto_escalera),
            escalera([1977,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            escalera([1992,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            #bajada
            escalera([2035,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            escalera([2050,c.altura_suelo-3*c.alto_escalera],3*c.alto_escalera),
            escalera([2065,c.altura_suelo-2*c.alto_escalera],2*c.alto_escalera),
            escalera([2080,c.altura_suelo-c.alto_escalera],c.alto_escalera),
            #decimo
            tuberia([2155,c.altura_suelo-c.alto_smario-3],c.alto_smario+3),
            ladrillo_con_monedas([2230,c.altura_suelo-55]),
            ladrillo_con_monedas([2245,c.altura_suelo-55]),
            interrogacion([2260,c.altura_suelo-55],True),ladrillo_rompible([2275,c.altura_suelo-55]),
            #undecimo
            tuberia([2395,c.altura_suelo-c.alto_smario-3],c.alto_smario+3),
            # parte diseñada por nosotros
            interrogacion([2465,c.altura_suelo-55],True),interrogacion([2495,c.altura_suelo-55],True),
            interrogacion([2525,c.altura_suelo-55],True),interrogacion([2495,c.altura_suelo-110],False),
            cañon_lanza_bills([2495,c.altura_suelo-16],2),
            #bloque de la bandera
            cañon_lanza_bills([2700,c.altura_suelo-16],0),
            cañon_lanza_bills([2715,c.altura_suelo-32],0,True),
            escalera([2730,c.altura_suelo-3*c.alto_escalera],3*c.alto_escalera),
            escalera([2745,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            escalera([2760,c.altura_suelo-5*c.alto_escalera],1*c.alto_escalera),
            escalera([2775,c.altura_suelo-6*c.alto_escalera],2*c.alto_escalera),
            escalera([2790,c.altura_suelo-7*c.alto_escalera],3*c.alto_escalera),
            escalera([2760,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            escalera([2775,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
            escalera([2790,c.altura_suelo-4*c.alto_escalera],4*c.alto_escalera),
        

            ladrillo_rompible([2900, c.altura_suelo-15])
            ]
    
    def __generar_npcs(self):
        self.npcs = [
            goomba([760,c.altura_suelo-c.alto_goomba]),goomba([800,c.altura_suelo-c.alto_goomba]),
            goomba([2280,c.altura_suelo-c.alto_goomba]),goomba([2300,c.altura_suelo-c.alto_goomba]),
            goomba([1330, c.altura_suelo-110-c.alto_goomba]),goomba([1350, c.altura_suelo-110-c.alto_goomba]),
            goomba([1470, c.altura_suelo-c.alto_goomba]),goomba([1520, c.altura_suelo-c.alto_goomba]),koopa_troopa([1540,c.altura_suelo-c.alto_koopa_troopa]),
            goomba([280,c.altura_suelo-c.alto_koopa_troopa]),koopa_troopa([1870,c.altura_suelo-c.alto_koopa_troopa])
                    ]

    def __mantener_jugador_en_pantalla(self):
        """hace que el jugador no puda salir por la izquierda y si llega al centro mueve el nivel"""
        if self.jugador.coord[0]<0:
            self.jugador.coord[0] =0
        if self.jugador.coord[0] > pyxel.width/2:
            self.jugador.coord[0] = pyxel.width/2
            self.__desplazar_nivel()
     
    def __desplazar_nivel(self):
        """se asegura de que el jugador se mantiene en el centro de la pantalla trasmitiendo su movimiento a las demas entidades"""
        for bloque in self.__bloques:
            bloque.coord[0]-=self.jugador.v_x

        for objeto in self.objetos:
            objeto.coord[0] -= self.jugador.v_x
        for npc in self.npcs:
            npc.coord[0] -= self.jugador.v_x
        for decorado in self.atrezzo:
            decorado.coord[0] -= self.jugador.v_x

    def __redondear(self,n:float)->int:
        """esta funcion es necesaria para evitar que visualmente las entidades no vibren al desplazarse"""
        return round(n-0.000001) # el metodo round funciona un poco mal en este caso pero asi siempre redondea correctamente

    def reset_level(self):
        """reinicia el nivel manteniendo las vidas del jugador"""
        self.jugador.reset_state()
        self.tiempo = c.tiempo  # contador de la esquina superior derecha
        self.__generar_bloques()
        self.__generar_suelo()
        self.__generar_npcs()
        self.__generar_objetos()
        self.__generar_atrezzo()

    def reset_game(self):
        """reinicia el juego entero"""
        self.en_menu = True
        self.jugador.reset_state()
        self.tiempo = c.tiempo  # contador de la esquina superior derecha
        self.jugador = player.mario([130, c.altura_suelo-35])
        self.__generar_bloques()
        self.__generar_suelo()
        self.__generar_npcs()
        self.__generar_objetos()
        self.__generar_atrezzo()

    def __borrar_entidades(self, bloques: list, npcs: list, objetos: list, decoracion: list):
        """un bucle que va recorriendo todas las entidades del juego viendo si deben ser eliminadas:
            las elimina si no existen(bloques y objetos),estan muertas(npcs) o salen por la izquierda de la pantalla,
            no elimina si sale spor la izquierda ya que influye negativamente en el rendimiento"""
        i = 0
        while i < len(bloques):  # revisa los bloques
                bloque = bloques[i]
                if not bloque.existe:
                    del(bloques[i])
                else:
                    i += 1
        i = 0
        while i < len(npcs):  # revisa los npcs
            npc = npcs[i]
            if not npc.esta_vivo or npc.coord[0]<-npc.ancho:
                del(npcs[i])
            else:
                i += 1
        i = 0
        while i < len(objetos):  # revisa los objetos
            objeto = objetos[i]
            if not objeto.existe:
                if isinstance(objeto, moneda):
                    self.jugador.score += c.punt_moneda
                del(objetos[i])
            else:
                i += 1
    
    def animacion_de_inicio(self):
        self.__posicion_mario += 1
        if self.__posicion_mario > 130:
            self.en_menu=False
            self.__posicion_mario = 105
            self.__animacion = False


    def generar_balas(self, bloque):
       if isinstance(bloque, cañon_lanza_bills):
                bloque.lanzar(self.npcs)
            
                
       
game()