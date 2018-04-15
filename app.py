import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import medidor as Medidor
import indicador as Indicador
import grafico as Grafico


class Window:
    def __init__(self, master):
        def toggle_fullscreen(self, event=None):
            self.state = not self.state  # Just toggling the boolean
            master.attributes("-fullscreen", self.state)
            return "break"

        def end_fullscreen(self, event=None):
            self.state = False
            master.attributes("-fullscreen", False)
            return "break"

        # Obtener ancho/alto de la pantalla
        self.ancho_total = master.winfo_screenwidth()
        self.altura_total = master.winfo_screenheight()
        # Título de la ventana
        master.title('Gauge')
        # Pantalla completa
        master.attributes("-fullscreen", True)
        # Acciones de salir de pantalla completa
        self.state = False
        master.bind("<F11>", toggle_fullscreen)
        master.bind("<Escape>", end_fullscreen)
        # Elementos
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.mainContainer = tk.Frame(self.master)
        self.mainContainer.grid(column=0, row=0)


        # Medidores ****************************************************************************************************
        n_medidores = 2
        ancho_medidor = self.ancho_total / n_medidores/2.5
        altura_medidor = self.altura_total/ n_medidores/1.25
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_medidor = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100,"intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100, "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"}
        ]
        i = 0
        altura = configuracion_medidor[i]['altura']
        ancho = configuracion_medidor[i]['ancho']
        while i < len(configuracion_medidor):
            self.medidor = Medidor.Medidor(self.mainContainer, configuracion=configuracion_medidor[i],
                bd=2, height=altura, width=ancho, bg='white', highlightbackground="black")
            self.medidor.grid(column=(i+1)+(i+1), row=0, columnspan=2,padx=20)
            i += 1
        # Gráficos **************************************************************************************************
        n_graficos = 3
        ancho_grafico = self.ancho_total / n_graficos / 1.5
        altura_grafico = self.altura_total/2.5
        configuracion_grafico = [
            {"nombreX": "Nº de grado de cigüeñal", "nombreY": "Presión/Par",
             "ancho": ancho_grafico, "altura": altura_grafico, "intervalo": 3000},
            {"nombreX": "Volumen", "nombreY": "Presión",
             "ancho": ancho_grafico, "altura": altura_grafico, "intervalo": 3000},
            {"nombreX": "ω promedio/vuelta", "nombreY": "Potencia/vuelta",
             "ancho": ancho_grafico, "altura": altura_grafico,"intervalo": 3000}
        ]
        i = 0
        while i < len(configuracion_grafico):
            self.grafico = Grafico.Grafico(self.mainContainer, configuracion=configuracion_grafico[i])
            self.grafico.grid(row=1, column=(i*2)+1, columnspan=2,padx=20,pady=10)
            i += 1

        # Indicadores **************************************************************************************************
        n_indicadores = 8
        ancho_indicador = (self.ancho_total / n_indicadores) - n_indicadores*2
        altura_indicador = self.altura_total / n_indicadores
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_indicador = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Vuelta de cigüeñal", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "I/vuelta", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "ω instantánea", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "ω promedio/vuelta", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Volumen", "unidad": "m^3", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Potencia", "unidad": "W", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"}
        ]
        i = 0
        while i < len(configuracion_indicador):
            altura = configuracion_indicador[i]['altura']
            ancho = configuracion_indicador[i]['ancho']
            self.indicador = Indicador.Indicador(self.mainContainer,
                bd=2,height=altura,width=ancho, bg='white',highlightbackground="black",
                configuracion=configuracion_indicador[i])
            self.indicador.grid(row=2, column=i)
            i += 1

        # Botón de salir ***********************************************************************************************
        self.salirButton = tk.Button(self.mainContainer, text='Salir', width=10, command=master.destroy)
        self.salirButton.grid(row=0, column=7, sticky="N")
def main():
    root = tk.Tk()
    Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()