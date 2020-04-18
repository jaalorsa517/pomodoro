# -*- coding:utf-8 -*-

import os
import queue
import threading
import time
import tkinter as tk
import tkinter.font as f
import tkinter.messagebox as ms
from pomodoro import Pomodoro


class Ventana:
    def __init__(self):
        self._pomodoro = Pomodoro()
        self.isPomodoro = True

        #Cola que controla el temporizador
        self._fifo_counter = queue.Queue(1)
        #Cola que controla la permutacion del label
        self._fifo_evento_reloj = queue.Queue(2)
        #Cola que controla el hilo del evento del reloj
        self._fifo_evento_reloj_control = queue.Queue(1)

        self._evento_reloj = threading.Thread(name='evento_reloj',
                                              target=self._on_evento_reloj,
                                              daemon=True)

        self._evento_reloj.start()
        self._fifo_evento_reloj_control.put('Init')

        self._text_reloj = '00:00'

        ### Pantalla principal
        self._root = tk.Tk()
        self._root.title('Pomodoro')
        self._root.geometry('350x250+450+150')
        self._root.resizable(False, False)

        ### Frames
        self._frame_principal = tk.Frame(self._root)
        self._frame_principal.pack(expand=True, fill=tk.BOTH)

        self._frame_pomodoro = tk.Frame(self._frame_principal)
        self._frame_pomodoro.pack(expand=True, fill=tk.BOTH)

        self._frame_reloj = tk.Frame(self._frame_principal)
        self._frame_reloj.pack(expand=True, fill=tk.BOTH)

        self._frame_boton = tk.Frame(self._frame_principal)
        self._frame_boton.pack(expand=True, fill=tk.X, side=tk.BOTTOM)

        ### Fila del pomodoro
        fontPomodoro = ('Arial', 16)
        self._pomodoro_title = tk.Label(self._frame_pomodoro,
                                        text='Pomodoro #',
                                        font=fontPomodoro)
        self._pomodoro_title.grid(row=0, column=0, padx=20)
        self._pomodoro_count = tk.Label(self._frame_pomodoro,
                                        text='0',
                                        font=fontPomodoro)
        self._pomodoro_count.grid(row=0, column=1)

        ### Fila central o del reloj
        self._reloj = tk.Label(self._frame_reloj,
                               text=self._text_reloj,
                               font=('Times', 56))
        self._reloj.pack()

        ### Botones
        fontButton = ('Arial', 12)
        self._boton_iniciar = tk.Button(self._frame_boton,
                                        text='Iniciar',
                                        command=self._on_boton_iniciar_click,
                                        font=fontButton)
        self._boton_iniciar.grid(column=0, row=0, padx=50)
        self._boton_cancelar = tk.Button(self._frame_boton,
                                         text='Cancelar',
                                         command=self._on_boton_cancelar_click,
                                         font=fontButton)
        self._boton_cancelar.grid(column=2, row=0, padx=40)

    ### Metodos de la clase
    def _setReloj(self, tiempo):
        self._reloj.configure(text=tiempo)

    def _setPomodoroCount(self, count):
        self._pomodoro_count.configure(text=count)

    def run(self):
        self._root.mainloop()

    ### Eventos botones
    def _on_boton_iniciar_click(self):

        if (self.isPomodoro):
            tk.messagebox.showinfo('POMODORO', 'Inicio del pomodoro')
            self._hilo_counter = threading.Thread(
                name='hilo_counter',
                target=self._hilo_temporizador,
                args=(self._pomodoro.POMODORO_MIN, ))
            self.isPomodoro = False
        else:
            ms.showinfo('DESCANSO', 'Inicio del descanso')
            if (self._pomodoro.pomodoro == 4):
                self._pomodoro.pomodoro = 0
                self._pomodoro.descanso_final()
                self._hilo_counter = threading.Thread(
                    name='hilo_counter',
                    target=self._hilo_temporizador,
                    args=(self._pomodoro.DESCANSO_MIN * 4, ))

            else:
                self._hilo_counter = threading.Thread(
                    name='hilo_counter',
                    target=self._hilo_temporizador,
                    args=(self._pomodoro.DESCANSO_MIN, ))
            self.isPomodoro = True

        self._hilo_counter.start()
        self._fifo_counter.put('init')
        self._boton_iniciar.configure(state=tk.DISABLED)

    def _on_boton_cancelar_click(self):

        if (self._fifo_counter.full()):
            self._fifo_counter.get()
            self._fifo_evento_reloj.put(self._text_reloj)
            self._pomodoro.pomodoro = 0
            self._boton_iniciar.configure(state=tk.ACTIVE)

    ### Eventos de hilos
    def _on_evento_reloj(self):
        while (True):

            if (self._fifo_evento_reloj.full()):
                text_init = self._fifo_evento_reloj.get()
                text_update = self._fifo_evento_reloj.get()

                if (text_init == text_update):
                    self._fifo_evento_reloj.put(text_init)
                    self._fifo_evento_reloj.put(text_update)
                else:
                    self._setReloj(text_update)
                    self._fifo_evento_reloj.put(text_update)

    def _hilo_temporizador(self, limit):

        if (not self.isPomodoro):
            self._pomodoro.pomodoro += 1

        self._setPomodoroCount(self._pomodoro.pomodoro)

        sw = False  #Bandera para determinar si el hilo se cancela
        for i in range(limit * 60):
            if (not self.isPomodoro):
                self._fifo_evento_reloj.put(
                    self._pomodoro.initied_temporizador())
            else:
                self._fifo_evento_reloj.put(self._pomodoro.initied_descanso())

            if (self._fifo_counter.empty()):
                if (self.isPomodoro):
                    self.isPomodoro = False
                else:
                    self.isPomodoro = True
                sw = True
                break

        if (self._fifo_counter.full()):
            self._fifo_counter.get()

        self._pomodoro.init_attributes()

        if (not sw):

            respuesta = ms.askyesno('CONTINUAR', 'Desea continuar?')
            if (respuesta):
                self._on_boton_iniciar_click()
            else:
                self._on_boton_cancelar_click()


if __name__ == "__main__":
    reloj = Pomodoro()
    window = Ventana()
    window.run()
