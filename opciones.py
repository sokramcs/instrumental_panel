# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

class Opciones(tk.Frame, object):
    def __init__(self, master, app, configuracion, **kwargs):
        super(Opciones, self).__init__(master,configuracion=None, **kwargs)
        # Parámetros
        self.master = master
        self.app = app
        self.modo = configuracion["modo"]
        # Elementos
        self.modoRadioLabel = tk.Label(master, text="Modo de funcionamiento", bg='white', font='Helvetica 10 bold')
        self.modoRadio0 = tk.Radiobutton(master, text="Adquisición de datos", variable=self.modo, value='Adquisición', bg='white')
        self.modoRadio1 = tk.Radiobutton(master, text="Simulación de datos", variable=self.modo, value='Simulación', bg='white')

        self.tipoInterrupcion = tk.IntVar()
        self.interrupcionLabel = tk.Label(master, text="Punto de interrupción", bg='white', font='Helvetica 10 bold')
        self.interrupcionRadio0 = tk.Radiobutton(master, text="Desactivado", variable=self.tipoInterrupcion, value='0', bg='white', command=self.cambiar_interrupcion)
        self.interrupcionRadio1 = tk.Radiobutton(master, text="Por tiempo", variable=self.tipoInterrupcion, value='1', bg='white', command=self.cambiar_interrupcion)
        self.interrupcionRadio2 = tk.Radiobutton(master, text="Por vuelta", variable=self.tipoInterrupcion, value='2', bg='white', command=self.cambiar_interrupcion)

        self.numeroVueltaLabel = tk.Label(master, text="Vuelta", bg='white', font='Helvetica 10 bold')
        self.numeroVueltaEntry = tk.Entry(master, bd=5, width="5")
        self.numeroDienteLabel = tk.Label(master, text="Diente", bg='white', font='Helvetica 10 bold')
        self.numeroDienteEntry = tk.Entry(master, bd=5, width="5")

        self.horasLabel = tk.Label(master, text="h", bg='white', font='Helvetica 10 bold')
        self.horasEntry = tk.Entry(master, bd=5, width="5")
        self.minutosLabel = tk.Label(master, text="min", bg='white', font='Helvetica 10 bold')
        self.minutosEntry = tk.Entry(master, bd=5, width="5")
        self.segundosLabel = tk.Label(master, text="s", bg='white', font='Helvetica 10 bold')
        self.segundosEntry = tk.Entry(master, bd=5, width="5")
        self.milisegundosLabel = tk.Label(master, text="ms", bg='white', font='Helvetica 10 bold')
        self.milisegundosEntry = tk.Entry(master, bd=5, width="5")


        self.aplicarButton = tk.Button(master, text='Aplicar', width=10, command=self.guardar_opciones)
        self.aceptarButton = tk.Button(master, text='Aceptar', width=10, command=self.aceptar_opciones)

        self.modoRadioLabel.grid(row=0, column=0, columnspan=2)
        self.modoRadio0.grid(row=1, column=0, columnspan=2)
        self.modoRadio1.grid(row=2, column=0, columnspan=2)
        self.interrupcionLabel.grid(row=3, column=0, columnspan=2)
        self.interrupcionRadio0.grid(row=4, column=0, columnspan=2)
        self.interrupcionRadio1.grid(row=5, column=0, columnspan=2)
        self.interrupcionRadio2.grid(row=6, column=0, columnspan=2)
        self.numeroVueltaLabel.grid(row=7, column=0)
        self.numeroVueltaLabel.grid_remove()
        self.numeroVueltaEntry.grid(row=8, column=0)
        self.numeroVueltaEntry.grid_remove()
        self.numeroDienteLabel.grid(row=7, column=1)
        self.numeroDienteLabel.grid_remove()
        self.numeroDienteEntry.grid(row=8, column=1)
        self.numeroDienteEntry.grid_remove()
        self.horasLabel.grid(row=7, column=0, sticky="W", padx=(14, 0))
        self.horasLabel.grid_remove()
        self.horasEntry.grid(row=8, column=0, sticky="W")
        self.horasEntry.grid_remove()
        self.minutosLabel.grid(row=7, column=0, sticky="E", padx=(0, 7))
        self.minutosLabel.grid_remove()
        self.minutosEntry.grid(row=8, column=0, sticky="E")
        self.minutosEntry.grid_remove()
        self.segundosLabel.grid(row=7, column=1, sticky="W", padx=(14, 0))
        self.segundosLabel.grid_remove()
        self.segundosEntry.grid(row=8, column=1, sticky="W")
        self.segundosEntry.grid_remove()
        self.milisegundosLabel.grid(row=7, column=1, sticky="E", padx=(0, 10))
        self.milisegundosLabel.grid_remove()
        self.milisegundosEntry.grid(row=8, column=1, sticky="E")
        self.milisegundosEntry.grid_remove()
        self.aplicarButton.grid(row=9, column=0)
        self.aceptarButton.grid(row=9, column=1)

    def aceptar_opciones(self):
        self.app.main.desplegar_opciones()
        self.guardar_opciones()

    def guardar_opciones(self):
        if self.tipoInterrupcion.get() == 0:
            opciones = {
                "modo": self.modo.get(),
                "tipo_int": self.tipoInterrupcion.get()
            }
        elif self.tipoInterrupcion.get() == 1:
            opciones = {
                "modo": self.modo.get(),
                "tipo_int": self.tipoInterrupcion.get(),
                "horas": self.horasEntry.get(),
                "minutos": self.minutosEntry.get(),
                "segundos": self.segundosEntry.get(),
                "milisegundos": self.milisegundosEntry.get()
            }
        else:
            opciones = {
                "modo": self.modo.get(),
                "tipo_int": self.tipoInterrupcion.get(),
                "vuelta": self.numeroVueltaEntry.get(),
                "diente": self.numeroDienteEntry.get()
            }

        self.app.set_opciones(opciones)

    def cambiar_interrupcion(self):
        if self.tipoInterrupcion.get() == 0:
            self.horasLabel.grid_remove()
            self.horasEntry.grid_remove()
            self.minutosLabel.grid_remove()
            self.minutosEntry.grid_remove()
            self.segundosLabel.grid_remove()
            self.segundosEntry.grid_remove()
            self.milisegundosLabel.grid_remove()
            self.milisegundosEntry.grid_remove()
            self.numeroVueltaLabel.grid_remove()
            self.numeroVueltaEntry.grid_remove()
            self.numeroDienteLabel.grid_remove()
            self.numeroDienteEntry.grid_remove()
        elif self.tipoInterrupcion.get() == 1:
            self.horasLabel.grid()
            self.horasEntry.grid()
            self.minutosLabel.grid()
            self.minutosEntry.grid()
            self.segundosLabel.grid()
            self.segundosEntry.grid()
            self.milisegundosLabel.grid()
            self.milisegundosEntry.grid()

            self.numeroVueltaLabel.grid_remove()
            self.numeroVueltaEntry.grid_remove()
            self.numeroDienteLabel.grid_remove()
            self.numeroDienteEntry.grid_remove()
        else:
            self.numeroVueltaLabel.grid()
            self.numeroVueltaEntry.grid()
            self.numeroDienteLabel.grid()
            self.numeroDienteEntry.grid()
            self.horasLabel.grid_remove()
            self.horasEntry.grid_remove()
            self.minutosLabel.grid_remove()
            self.minutosEntry.grid_remove()
            self.segundosLabel.grid_remove()
            self.segundosEntry.grid_remove()
            self.milisegundosLabel.grid_remove()
            self.milisegundosEntry.grid_remove()

