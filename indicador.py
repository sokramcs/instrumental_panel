# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import tkinter.font as tkf

# Clase Indicador: Engloba cada uno de los indicadores
class Indicador(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Indicador, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.titulo = configuracion["nombre"]
        self.unidad = configuracion["unidad"]
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        self.valor_anterior = ""
        # Se configura el indicador
        self.layoutparams(self.altura, self.ancho)
        self.createhand(self.altura, self.ancho)

    def layoutparams(self, altura, ancho):
        # find a square that fits in the window
        if altura * 2 > ancho:
            self.side = ancho
        else:
            self.side = altura * 2

        # set axis for hand
        self.centrex = self.side / 2
        self.centrey = self.side / 2


    def createhand(self, altura, ancho):
        # create text display
        self.tituloid = self.create_text(self.centrex
                                       ,  self.centrey - self.centrey*0.6
                                       , font=tkf.Font(size=-int(self.side/8),weight="bold"),width='225')
        self.valorid = self.create_text(self.centrex
                                       , self.centrey/1
                                       , font=tkf.Font(size=-int(self.side/4)))
        self.unidadid = self.create_text(self.centrex
                                       , self.centrey*1.3
                                       , font=tkf.Font(size=-int(self.side/10)))
        self.itemconfigure(self.unidadid, text=str(self.unidad), fill='black')
        self.itemconfigure(self.tituloid, text=str(self.titulo), fill='black')

    def set(self, valor):
        if self.valor_anterior != str(valor):
            self.itemconfigure(self.valorid, text=str(valor))
            self.valor_anterior = str(valor)

