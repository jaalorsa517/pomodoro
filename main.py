# -*- coding:utf-8 -*-

import tkinter as tk
import threading
import queue
import time
from pomodoro import Pomodoro


class Ventana:
    def __init__(self):

        self._pomodoro = Pomodoro()

        self._fifo_counter = queue.Queue(1)
        self._fifo_evento_reloj = queue.Queue(2)
        self._fifo_evento_reloj_control = queue.Queue(1)

        self._evento_reloj = threading.Thread(name='evento_reloj',
                                              target=self._on_evento_reloj,
                                              daemon=True)

        self._evento_reloj.start()
        self._fifo_evento_reloj_control.put('Init')

        self._text_reloj = '00:00'

        self._root = tk.Tk()
        self._root.title('Pomodoro')
        self._root.geometry('400x400')

        self._frame_principal = tk.Frame(self._root)
        self._frame_principal.pack(expand=True, fill=tk.BOTH)

        self._frame_pomodoro = tk.Frame(self._frame_principal)
        self._frame_pomodoro.pack(expand=True, fill=tk.BOTH)

        self._frame_reloj = tk.Frame(self._frame_principal)
        self._frame_reloj.pack(expand=True, fill=tk.BOTH)

        self._frame_boton = tk.Frame(self._frame_principal)
        self._frame_boton.pack(expand=True, fill=tk.X, side=tk.BOTTOM)

        self._pomodoro_title = tk.Label(self._frame_pomodoro,
                                        text='Pomodoro #')
        self._pomodoro_title.grid(row=0, column=0)
        self._pomodoro_count = tk.Label(self._frame_pomodoro, text='0')
        self._pomodoro_count.grid(row=0, column=1)

        self._reloj = tk.Label(self._frame_reloj, text=self._text_reloj)
        self._reloj.pack()

        self._boton_iniciar = tk.Button(self._frame_boton,
                                        text='Iniciar',
                                        command=self._on_boton_iniciar_click)
        self._boton_iniciar.grid(column=0, row=0)
        self._boton_reiniciar = tk.Button(
            self._frame_boton,
            text='Reiniciar',
            command=self._on_boton_reiniciar_clic)
        self._boton_reiniciar.grid(column=1, row=0)
        self._boton_cancelar = tk.Button(self._frame_boton,
                                         text='Cancelar',
                                         command=self._on_boton_cancelar_click)
        self._boton_cancelar.grid(column=2, row=0)

    def _setReloj(self, tiempo):
        self._reloj.configure(text=tiempo)

    def _setPomodoroCount(self, count):
        self._pomodoro_count.configure(text=count)

    def run(self):
        self._root.mainloop()

    def _on_boton_iniciar_click(self):
        self._setPomodoroCount(self._pomodoro.pomodoro)
        self._hilo_counter = threading.Thread(name='hilo_counter',
                                              target=self._hilo_temporizador)
        self._hilo_counter.start()
        self._fifo_counter.put('init')
        self._boton_iniciar.configure(state=tk.DISABLED)
        self._boton_reiniciar.configure(state=tk.DISABLED)

    def _on_boton_reiniciar_clic(self):
        self._fifo_evento_reloj.put(self._text_reloj)
        self._setReloj(self._text_reloj)
        self._pomodoro.init_attributes()
        self._boton_iniciar.configure(state=tk.ACTIVE)

    def _on_boton_cancelar_click(self):

        if (self._fifo_counter.full()):
            self._fifo_counter.get()
            self._boton_reiniciar.configure(state=tk.ACTIVE)

    def _on_evento_reloj(self):
        while (True):
            time.sleep(0.5)

            if (self._fifo_evento_reloj.full()):
                text_init = self._fifo_evento_reloj.get()
                text_update = self._fifo_evento_reloj.get()

                if (text_init == text_update):
                    self._fifo_evento_reloj.put(text_init)
                    self._fifo_evento_reloj.put(text_update)
                else:
                    self._setReloj(text_update)
                    self._fifo_evento_reloj.put(text_update)

            if (self._fifo_evento_reloj_control.empty()):
                break

        print('Fin hilo ' + self._evento_reloj.getName())

    def _hilo_temporizador(self):

        for i in range(self._pomodoro.POMODORO_MIN * 60):
            self._fifo_evento_reloj.put(self._pomodoro.initied_temporizador())
            if (self._fifo_counter.empty()):
                break
        print('Fin hilo' + self._hilo_counter.getName())


if __name__ == "__main__":
    reloj = Pomodoro()
    window = Ventana()
    window.run()
