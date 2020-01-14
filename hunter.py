"""
Nombre: Hunter Game
Autor:  Federico del Cid - thegreench1996@gmail.com
Desc.:  El juego se trata de capturar 'frutas' que aparecen de forma aleatoria en el tablero,
        cada captura otorga energía al jugador, que debe acumular la máxima cantidad en el menor
        número de movimientos posibles. Como contrapartida, cada movimiento que realiza el jugador
        le consume parte de la energía total que tiene, perdiendo el juego si ésta llega a 0.

Creado: 14/01/2020
Actualizado: 14/01/2020
Versión: 1.0.1b
"""

from tkinter import Canvas, mainloop, BOTH, Tk, Frame, NE
from random import randrange as rpos

main = Tk()
main.resizable(False, False)
main.title("Hunter Game v1.0")
w, h = 1080, 1080
cell = w//20
pasos = 0


#   SECCIÓN PUNTUACIONES
f = Frame(height=cell, bd=0, highlightthickness=0, bg='#520')
f.pack(fill=BOTH)

energy = Canvas(f, width=cell*5, height=cell, bd=0, highlightthickness=0, bg='#5B0')
energy.place(relx=0, rely=0)

#   SECCIÓN DE TABLERO DE JUEGO

c = Canvas(width=w, height=h, bg='#555', bd=0, highlightthickness=0)
c.pack()
c.create_rectangle(0,0,w-1,h-1)

class Food():
    global c
    def __init__(self, x=rpos(0, w, cell), y=rpos(0, h, cell)):
        self.fruit = c.create_rectangle(x, y, x+cell, y+cell, fill='gold', tags='fruit')
        self.coords = c.coords(self.fruit)
    
    def remove(self, Px, Py):
        x, y = rpos(0, w, cell), rpos(0, h, cell)
        if (x, y) == (Px, Py):
            self.remove(Px, Py)
        c.delete('fruit')
        self.fruit = c.create_rectangle(x, y, x+cell, y+cell, fill='gold', tags='fruit')
        self.coords = c.coords(self.fruit)

class Player():
    global c
    def __init__(self, x1, y1, x2, y2):
        self.player = c.create_rectangle(x1, y1, x2, y2, fill='salmon', tags='player')
        self.coords = c.coords(self.player)
    
    def move(self, x, y):
        c.move(self.player, x, y)
        self.coords = c.coords(self.player)

    def new_pos(self, x1, y1, x2, y2):
        c.delete('player')
        self.player = c.create_rectangle(x1, y1, x2, y2, fill='salmon', tags='player')
        self.coords = c.coords(self.player)

    def verificar(self):
        if self.coords[0] < 0:
            self.new_pos(w-cell, self.coords[1], w, self.coords[3])
        elif self.coords[1] < 0:
            self.new_pos(self.coords[0], h-cell, self.coords[2], h)
        elif self.coords[2] > w:
            self.new_pos(0, self.coords[1], cell, self.coords[3])
        elif self.coords[3] > h:
            self.new_pos(self.coords[0], 0, self.coords[2], cell)

def orientacion(A1, A2, A3):
    return 1 if (A1[0]-A3[0])*(A2[1]-A3[1])-(A1[1]-A3[1])*(A2[0]-A3[0]) >= 0 else 0

def verif(P, A1, A2, A3):
    R1 = orientacion(A1, A2, A3)
    R2 = orientacion(A1, A2, P)
    R3 = orientacion(A2, A3, P)
    R4 = orientacion(A3, A1, P)
    if R1==R2==R3==R4:
        return True
    else:
        return False

def mover(clic):
    global pasos
    P = [clic.x, clic.y]
    # Movimiento superior
    if P[1] < h/2:
        A1, A2, A3 = [0, 0], [w, 0], [w/2, h/2]
        if verif(P, A1, A2, A3):
            '''Movimiento superior'''
            player.move(0, -cell)
        elif P[0] < w/2:
            '''Movimiento izquierdo'''
            player.move(-cell, 0)
        else:
            '''Movimiento derecho'''
            player.move(cell, 0)
    # Movimiento inferior
    else:
        A1, A2, A3 = [0, h], [w, h], [w/2, h/2]
        if verif(P, A1, A2, A3):
            '''Movimiento inferior'''
            player.move(0, cell)
        elif P[0] < w/2:
            '''Movimiento izquierdo'''
            player.move(-cell, 0)
        else:
            '''Movimiento derecho'''
            player.move(cell, 0)
    player.verificar()
    pasos+=1
    c.delete('pasos')
    c.create_text(w, 0, anchor=NE, text=pasos, tags='pasos')
    energy.config(width=energy.winfo_width()-(cell*.05))
    if player.coords == food.coords:
        food.remove(player.coords[0], player.coords[1])
        energy.config(width=energy.winfo_width()+(cell*.25))
        main.update()
    if energy.winfo_width() == 1:
        c.unbind("<Button-1>")
        c.create_text(w/2, h/2, text='GAME OVER', font=('', 20, 'bold'), tags='gameover')
    elif energy.winfo_width() >= w:
        c.unbind("<Button-1>")
        c.create_text(w/2, h/2, text='HAS GANADO', font=('', 20, 'bold'), tags='gameover')



food = Food()
player = Player(w/2, h/2, (w/2)+cell, (h/2)+cell)
c.bind("<Button-1>", mover)
mainloop()