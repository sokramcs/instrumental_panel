# coding=utf-8
import tkinter as tk

from scripts.main import Main

from tkinter import filedialog
import datetime as datetime
import random
import serial
import os
import math

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Inicializar variables
        self.job = None
        self.reiniciar = False
        self.puerto = '/dev/ttyUSB0'
        self.fila = 0
        self.vuelta = 0
        self.diente = 0
        self.tiempo = 0
        self.presion = 0
        self.par = 0
        self.csv = []
        self.file = []
        self.modo = tk.StringVar()
        self.grabando = False
        # Se establece el modo adquisición por defecto
        self.modo.set('Adquisición')
        self.pausa = False
        self.serial_abierto = False
        # Obtener el directorio actual
        self.dir = os.getcwd()
        # Configurar la ventana
        self.config_ventana()
        # Arrancar el main.py
        self.main = Main(self)
        self.main.pantallaCompletaButton.configure(relief='sunken')
        self.main.estadoLabel.config(text=self.modo.get())
        # Arrancar la aplicación
        if self.modo.get() == 'Simulación':
            self.simular_datos(0)
        else:
            self.adquirir_datos(0)

    def config_ventana(self):
        """Configura la ventana de la aplicación"""
        # Título de la ventana
        self.title('Panel instrumental')
        # Pantalla completa
        self.attributes("-fullscreen", True)
        # Acciones de salir de pantalla completa
        self.state = False
        self.bind("<F11>", self.switch_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

    def simular_datos(self, fila):
        """Simula la entrada de datos recursivamente cada 1ms"""
        if self.pausa:
            return
        # Se generan los valores
        # Diente
        self.diente += 1
        if self.diente > 360:
            self.diente = 1
        self.diente = int(self.diente)
        # Vuelta
        if self.diente == 360:
            self.vuelta += 1
        # Presión
        self.presion = ''
        # Par
        if self.diente == 1:
            self.par = random.uniform(-2.3, -1.7)
        elif self.diente < 95:  # -2 -> 5
            self.par += 0.07368
        elif self.diente < 150:  # 5 -> 3.2
            self.par -= 0.03272
        elif self.diente < 222:  # 3.2 -> 6.5
            self.par += 0.04583
        elif self.diente < 340:  # 6.5 -> -2.7
            self.par -= 0.07797
        else:  # -2.7 -> -2.05
            self.par += 0.0325
        # Tiempo
        self.tiempo = math.pi /((self.par+4)*25)
        # Pasa los datos al main.py
        self.set_datos()
        # Si es la primera fila, se llama de nuevo a la función. Si no, también se guardan los datos en self.file
        if fila > 0:
            self.file.append(str(self.vuelta) + ',' + str(self.diente) + ',' + str(self.tiempo) + ',' + str(self.presion) + ',' + str(self.par) + '\n')
            self.job = self.after(1, self.simular_datos, fila + 1)
        else:
            self.job = self.after(1, self.simular_datos, 0)

    def adquirir_datos(self, fila):
        """Obtiene los datos por el puerto serial"""
        self.serial_abierto = True
        if self.puerto_disponible(self.puerto):
            # Obtiene los datos y los guarda en self.file
            while self.serial_abierto:
                # Definir los datos del puerto
                self.ser = serial.Serial(
                    port=self.puerto,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )
                datos = self.ser.readline()
                if self.diente > datos.diente:
                    self.vuelta += 1
                self.diente = datos.diente
                self.tiempo = datos.tiempo
                self.presion = datos.presion
                self.par = datos.par
                self.set_datos()
                if fila > 0:
                    self.file.append(str(self.vuelta) + ',' + str(self.diente) + ',' + str(self.tiempo) + ',' + str(self.presion) + ',' + str(self.par) + '\n')
                fila += 1
                self.fila = fila
        else:
            # Se desconecta
            self.cambiar_estado('desconexion')
            # Recargar TopLevel cuando se minimiza/maximiza o se abre de nuevo la ventana
            self.bind("<FocusIn>", self.on_map)
            self.bind("<Map>", self.on_map)
            # Mensaje de reconexión
            self.toplevel = tk.Toplevel(self, bd=2, relief="solid")
            # Posición del TopLevel
            g = "+%s+%s" % (500, 200)
            self.toplevel.geometry(g)
            # Ocultar botones de minimizar, cerrar, expandir
            self.toplevel.overrideredirect(1)
            # Elementos del TopLevel
            ERROR_CONEXION = 'No se ha podido establecer la conexión con ' + self.puerto + '.'
            label1 = tk.Label(self.toplevel, text=ERROR_CONEXION, height=5, width=60)
            desconexion = tk.PhotoImage(file='images/desconexion.png')
            imagen = tk.Label(self.toplevel, image=desconexion)
            imagen.image = desconexion
            boton = tk.Button(self.toplevel, text='Reconectar', command=self.reconectar)
            TIEMPO = 'Reconectando automáticamente en 10 segundos'
            self.label2 = tk.Label(self.toplevel, text=TIEMPO, font='Helvetica 12 bold')
            label1.grid(row=0, column=0)
            imagen.grid(row=1, column=0)
            boton.grid(row=3, column=0, pady=20)
            self.label2.grid(row=2, column=0)
            self.bucle_reconectar(10)

    def puerto_disponible(self, puerto):
        """Comprueba si el puerto está disponible y devuelve True/False"""
        try:
            serial.Serial(port=puerto)
            return True
        except:
            return False

    def desconectar(self):
        self.toplevel.destroy()
        self.after_cancel(self.cuenta_atras)
        self.cuenta_atras = None
        self.unbind("<FocusIn>")
        self.unbind("<Map>")
        self.cambiar_estado('marcha')

    def reconectar(self):
        self.desconectar()
        self.adquirir_datos(self.fila)

    def bucle_reconectar(self, i):
        self.label2.config(text='Reconectando automáticamente en ' + str(i) + ' segundos')
        if self.modo.get() != 'Adquisición':
            self.desconectar()
        elif i > 0:
            i -= 1
            self.cuenta_atras = self.after(1000, self.bucle_reconectar, i)
        else:
            self.reconectar()

    def on_map(self, event):
        self.reconectar()

    def leer_datos(self, fila):
        self.fila_actual = fila
        if fila == 0:
            self.stop_set_datos()
            self.reiniciar = True
            self.modo_anterior = self.modo.get()
            self.modo.set('Reproducción')
            self.main.estadoLabel.config(text=self.modo.get())
        datos = self.csv[fila]
        self.vuelta = int(datos[0])
        self.diente = int(datos[1])
        self.tiempo = float(datos[2])
        self.presion = float(datos[3])
        self.par = float(datos[4])
        self.fila = fila + 1
        self.set_datos()
        # Se calcula un nuevo valor cuando termina el intervalo
        if fila < len(self.csv) - 1:
            self.job = self.after(1, self.leer_datos, self.fila)
        else:
            self.cambiar_estado('pausa')
            self.reset()
            self.modo.set(self.modo_anterior)
            self.main.estadoLabel.config(text=self.modo.get())

    def set_datos(self):
        """Pasa los datos al main.py"""
        valores = {"vuelta": self.vuelta, "diente": self.diente, "tiempo": self.tiempo, "presion": self.presion, "par": self.par}
        self.main.set(valores, self.reiniciar)
        self.reiniciar = False

    def stop_set_datos(self):
        """Detiene el proceso de adquirir o simular datos"""
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
        self.serial_abierto = False

    def switch_fullscreen(self, event=None):
        """Activa o desactiva la pantalla completa"""
        self.attributes("-fullscreen", self.state)
        if self.state:
            self.main.pantallaCompletaButton.configure(relief='sunken')
        else:
            self.main.pantallaCompletaButton.configure(relief='raised')
        self.state = not self.state
        return "break"

    def end_fullscreen(self, event=None):
        """Desactiva la pantalla completa"""
        self.state = False
        self.attributes("-fullscreen", False)
        self.main.pantallaCompletaButton.configure(relief='raised')
        return "break"

    def set_opciones(self, opciones):
        """Aplica las opciones de la aplicación"""
        modo = opciones['modo']
        dientes_refresco = opciones['dientes_refresco']
        estadoActual = self.main.estadoLabel['text']
        # Si se ha definido un intervalo de refresco
        if dientes_refresco != '' and dientes_refresco.isdigit():
            self.main.dientes_refresco = int(dientes_refresco)
        # Si se ha cambiado el modo
        if estadoActual != self.modo.get():
            self.main.estadoLabel.config(text=modo)
            # Se detiene el proceso
            self.stop_set_datos()
            if modo == 'Simulación':
                self.reset()
                self.simular_datos(0)
            elif modo == 'Adquisición':
                self.reset()
                self.adquirir_datos(0)
        tipo_int = opciones["tipo_int"]
        # Si la interrupción está desactivada
        if tipo_int == 0:
            self.main.breakpoint = ''
            self.main.vuelta_limite = ''
            self.main.diente_limite = ''
            self.main.breakpointLabel.grid_remove()
        # Si la interrupción es de tiempo
        elif tipo_int == 1:
            horas = opciones['horas']
            if horas == '':
                horas = 0
            minutos = opciones['minutos']
            if minutos == '':
                minutos = 0
            segundos = opciones['segundos']
            if segundos == '':
                segundos = 0
            milisegundos = opciones['milisegundos']
            if milisegundos == '':
                milisegundos = 0
            tiempo = datetime.timedelta(hours=float(horas), minutes=float(minutos), seconds=float(segundos), milliseconds=float(milisegundos))
            self.main.breakpoint = tiempo
            self.main.breakpointLabel.grid()
        # Si la interrupción es de vuelta
        else:
            vuelta = opciones['vuelta']
            if vuelta != '':
                vuelta = int(vuelta)
            diente = opciones['diente']
            if diente != '':
                diente = int(diente)
            self.main.vuelta_limite = vuelta
            self.main.diente_limite = diente
            self.main.breakpointLabel.grid()

    def stop(self):
        """Detener la aplicación completamente"""
        self.pausa = True
        self.grabando = False
        self.cambiar_estado('pausa')
        self.stop_set_datos()
        if self.modo.get() == 'Simulación' or self.modo.get() == 'Adquisición':
            file = tk.filedialog.asksaveasfile(mode='w', defaultextension=".csv", initialdir=self.dir, title="Select file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
            if not file:
                return
            # Guardar el archivo
            for i in range(0, len(self.file), 1):
                file.write(self.file[i])
            file.close()
        elif self.modo.get() == 'Reproducción':
            # Volver al estado anterior
            self.modo.set(self.modo_anterior)
            self.main.estadoLabel.config(text=self.modo.get())

    def open(self):
        """Abrir y reproducir un archivo"""
        self.pausa = False
        self.grabando = False
        file = tk.filedialog.askopenfile(initialdir=self.dir, title="Select file",
                                         filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if not file:
            return
        self.cambiar_estado('reproduccion')
        datos = str(file.read())
        array = datos.split('\n')
        csv = []
        for i in range(1, len(array) - 1, 1):
            csv.append(array[i].split(','))
        file.close()
        self.csv = csv
        self.reset()
        self.leer_datos(0)

    def record(self):
        """Grabar los datos y arrancar la aplicación"""
        self.pausa = False
        self.grabando = True
        self.stop_set_datos()
        self.cambiar_estado('grabacion')
        if self.modo.get() == 'Simulación':
            self.simular_datos(1)
        else:
            self.adquirir_datos(1)

    def pause(self):
        """Pausar la aplicación"""
        self.pausa = True
        self.grabando = False
        self.cambiar_estado('pausa')
        if self.modo.get() == 'Reproducción':
            self.main.stopButton.configure(state='normal')
            self.main.recordButton.configure(state='disabled')
        self.stop_set_datos()

    def play(self):
        """Reanudar la aplicación"""
        self.pausa = False
        self.grabando = False
        self.cambiar_estado('marcha')
        if self.modo.get() == 'Simulación':
            self.simular_datos(0)
        elif self.modo.get() == 'Adquisición':
            self.adquirir_datos(0)
        else:
            self.cambiar_estado('reproduccion')
            self.leer_datos(self.fila_actual)

    def reset(self):
        """Reiniciar los datos (se hará efectivo cuando se termine la vuelta actual)"""
        self.reiniciar = True
        self.main.vuelta_actual = 0
        self.vuelta = 0
        self.main.indicadores['indicador0'].itemconfigure(self.main.indicadores['indicador0'].valorid, text=str(0))
        self.main.timeLabel.config(text=str(datetime.timedelta(milliseconds=0)))

    def cambiar_estado(self, estado):
        """Cambiar el aspecto de los botones según el modo actual"""
        if estado == 'marcha':
            self.main.stopButton.configure(state='disabled')
            self.main.recordButton.configure(relief='raised')
            self.main.recordButton.configure(state='normal')
            self.main.playButton.configure(relief='raised')
            self.main.playButton.configure(state='normal')
            self.main.pauseButton.configure(relief='raised')
            self.main.pauseButton.configure(state='normal')
            self.main.playButton.grid_remove()
            self.main.pauseButton.grid()
            self.main.openButton.configure(state='normal')
            self.main.openButton.configure(relief='raised')
        elif estado == 'grabacion':
            self.main.stopButton.configure(state='normal')
            self.main.recordButton.configure(relief='sunken')
            self.main.recordButton.configure(state='disabled')
            self.main.playButton.configure(state='disabled')
            self.main.pauseButton.configure(relief='raised')
            self.main.pauseButton.configure(state='disabled')
            self.main.openButton.configure(state='disabled')
            self.main.openButton.configure(relief='raised')
        elif estado == 'pausa':
            self.main.stopButton.configure(state='disabled')
            self.main.recordButton.configure(relief='raised')
            self.main.recordButton.configure(state='normal')
            self.main.playButton.configure(state='normal')
            self.main.playButton.grid()
            self.main.pauseButton.configure(relief='sunken')
            self.main.pauseButton.configure(state='disabled')
            self.main.pauseButton.grid_remove()
            self.main.openButton.configure(state='normal')
            self.main.openButton.configure(relief='raised')
        elif estado == 'reproduccion':
            self.main.stopButton.configure(state='normal')
            self.main.recordButton.configure(relief='raised')
            self.main.recordButton.configure(state='disabled')
            self.main.playButton.configure(relief='raised')
            self.main.playButton.configure(state='normal')
            self.main.pauseButton.configure(relief='raised')
            self.main.pauseButton.configure(state='normal')
            self.main.playButton.grid_remove()
            self.main.pauseButton.grid()
            self.main.openButton.configure(state='disabled')
            self.main.openButton.configure(relief='sunken')
        elif estado == 'desconexion':
            self.main.stopButton.configure(state='disabled')
            self.main.recordButton.configure(state='disabled')
            self.main.playButton.configure(state='disabled')
            self.main.pauseButton.configure(state='disabled')

if __name__ == '__main__':
    app = App()
    app.mainloop()
