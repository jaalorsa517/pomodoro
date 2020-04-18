# -*- coding:utf-8 -*-
import time as t


class Pomodoro:
    def __init__(self):
        self.POMODORO_MIN = 1
        self.DESCANSO_MIN = 5
        self.pomodoro = 0  #Ciclo de 25 minutos
        self.init_attributes()

    def init_attributes(self):
        '''Metodo que inicializa todos los atributos de la clase'''
        self._temporizador = self.POMODORO_MIN * 60  #en segundos
        self._descanso = self.DESCANSO_MIN * 60  #en segundos

    def initied_temporizador(self):
        '''Función que devuelve el estado del temporizador'''
        t.sleep(1)
        self._temporizador = self._temporizador - 1
        return t.strftime('%M:%S', t.gmtime(self._temporizador))

    def initied_descanso(self):
        '''Función que devuelve el estado del descanso'''
        t.sleep(1)
        self._descanso = self._descanso - 1
        return t.strftime('%M:%S', t.gmtime(self._descanso))

    def descanso_final(self):
        self._descanso = self.DESCANSO_MIN * 60 * 4
