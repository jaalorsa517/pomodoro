# -*- coding:utf-8 -*-

import tkinter as tk
from pomodoro import Pomodoro


class Ventana:
    def __init__(self):
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

        self._reloj = tk.Label(self._frame_reloj, text='00:00')
        self._reloj.pack()

        self._boton_iniciar = tk.Button(self._frame_boton, text='Iniciar')
        self._boton_iniciar.grid(column=0, row=0)
        self._boton_reiniciar = tk.Button(self._frame_boton, text='Reiniciar')
        self._boton_reiniciar.grid(column=1, row=0)
        self._boton_cancelar = tk.Button(self._frame_boton, text='Cancelar')
        self._boton_cancelar.grid(column=2, row=0)

    def setReloj(self, tiempo):
        self._reloj.configure(text=tiempo)

    def setPomodoroCount(self, count):
        self._pomodoro_count.configure(text=count)

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    reloj = Pomodoro()
    window = Ventana()
    window.run()
