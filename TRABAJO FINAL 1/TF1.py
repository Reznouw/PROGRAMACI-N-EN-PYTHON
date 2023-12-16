.# -*- coding: utf-8 -*-
#%%
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port in ports:
    print(port)
#%%
#pip install pyserial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port in ports:
    print(type(port))
    print(port)
    
#%%
#RX
import serial

PORT ="COM2"

try:
    print(f"Conectado a {PORT}")
    ser=serial.Serial(port=PORT,
                      baudrate=9600,
                      bytesize=8,
                      timeout=2,
                      stopbits=serial.STOPBITS_ONE)
    print("Hecho!")
    
    while True:
        try:
            #si hay datos en el buffer de entrada
            if ser.in_waiting>0:
                #hay que leer los datos
                data = ser.readline()
                #los datos son binarios
                #hay que convertirlos a str
                string = data.decode("utf-8")
                print(f"Rx:{string}")
            
        #presionando Ctrl + C
        except KeyboardInterrupt:
            print("Cerrando conexion")
            ser.close()
            break
except:
    print(f"Puerto {PORT} no esta disponible")
    
#%%
#TXS
import serial

PORT = "COM3"

try:
    print(f"Estableciendo comunicación con puerto serial {PORT}...")
    ser = serial.Serial(port=PORT, 
                        baudrate=9600, 
                        bytesize=8, 
                        timeout=2, 
                        stopbits=serial.STOPBITS_ONE)
    print("Conexión extablecida")

    while True:
        # Se ingresa el texto a enviar por el puerto
        string = input("Datos a enviar:")
        # Se define una palabra para cerrar el puerto
        if string == "END":
            break
        else:
            # Se codifica como bytes el texto a enviar y se envia por el puerto
            data = string.encode("utf-8")
            ser.write(data)
    
    print("Conexion cerrada")
    ser.close()
except:
    print(f"Puerto {PORT} no disponible")
#%%
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import serial

class SerialChat(tk.Tk):
    def __init__(self):
        super().__init__()
        self.PORT = "COM1"
        
        self.title(f"Serial Chat")
        self.geometry("+50+50")
        self.resizable(0, 0)
        
        # ---------------------- SERIAL PORT --------------------------
        self.serial = None
        
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self, text="Conexion")
        frm2 = tk.Frame(self)
        frm3 = tk.LabelFrame(self, text="Enviar mensaje")
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)
        frm3.pack(padx=5, pady=5)
        
        # ------------------------ FRAME 1 ----------------------------
        self.lblCOM = tk.Label(frm1, text="Puerto COM:") 
        self.cboPort = ttk.Combobox(frm1, values=['COM1', 'COM2'])
        self.lblSpace = tk.Label(frm1, text="")
        self.btnConnect = ttk.Button(frm1, text="Conectar", width=16)
        self.lblCOM.grid(row=0, column=0, padx=5, pady=5)
        self.cboPort.grid(row=0, column=1, padx=5, pady=5)
        self.lblSpace.grid(row=0,column=2, padx=30, pady=5)
        self.btnConnect.grid(row=0, column=3, padx=5, pady=5)
        
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=25, width=50, wrap=tk.WORD, state='disable')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
                
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Texto:")
        self.inText = tk.Entry(frm3, width=45, state='disable')
        self.btnSend = ttk.Button(frm3, text="Enviar", width=12, state='disable')
        self.lblText.grid(row=0, column=0, padx=5, pady=5)
        self.inText.grid(row=0, column=1, padx=5, pady=5)
        self.btnSend.grid(row=0, column=2, padx=5, pady=5)
               
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
            
        # ------------- Control del boton "X" de la ventana -----------
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)
    
    
    def cerrar_puertos(self):
        # Se cierran los puertos COM y la ventana de tkinter
        try:
            pass
            #self.serial.close()
        except:
            pass

        self.destroy()
    
    
#root = tk.Tk()
app = SerialChat.mainloop()
#root.mainloop()
#%%
import threading
import time

def func1(delay):
    for _ in range(25):
        print("*", end='')
        time.sleep(delay)



def func2(delay):
    for _ in range(25):
        print("+", end='')
        time.sleep(delay)      
        
# El keyword daemon=True permite eliminar el thread si es que el programa principal se cierra.        
th1 = threading.Thread(target=func1, args=(0.25,), daemon=True)
th1.start()

th2 = threading.Thread(target=func2, args=(0.25,), daemon=True)
th2.start()
#%%
from time import sleep
import threading
def func1(delay):
    for _ in range(20):
        print("+",end='')
        sleep(delay)

def func2(delay):
    for _ in range(20):
        print("*",end='')
        sleep(delay)
        
th1 = threading.Thread(target=func1, args=(0.25,), daemon=True)
th2 = threading.Thread(target=func1, args=(0.25,), daemon=True)

th1.start()
th2.start()
#%%
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import serial
import serial.tools.list_ports
import threading
import time

class SerialChat(tk.Tk):
    def __init__(self):
        super().__init__()
        self.PORT = "COM1"
        
        self.title("Serial Chat")
        self.geometry("+50+50")
        self.resizable(0, 0)
        
        # ---------------------- SERIAL PORT --------------------------
        self.serial = None
        
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self, text="Conexion")
        frm2 = tk.Frame(self)
        frm3 = tk.LabelFrame(self, text="Enviar mensaje")
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)
        frm3.pack(padx=5, pady=5)
        
        # ------------------------ FRAME 1 ----------------------------
        self.lblCOM = tk.Label(frm1, text="Puerto COM:") 
        self.cboPort = ttk.Combobox(frm1, values=['COM1', 'COM2','COM3'])
        self.lblSpace = tk.Label(frm1, text="")
        self.btnConnect = ttk.Button(frm1, text="Conectar", width=16, command=self.connect)
        self.lblCOM.grid(row=0, column=0, padx=5, pady=5)
        self.cboPort.grid(row=0, column=1, padx=5, pady=5)
        self.lblSpace.grid(row=0,column=2, padx=30, pady=5)
        self.btnConnect.grid(row=0, column=3, padx=5, pady=5)
        
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=25, width=50, wrap=tk.WORD, state='disable')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.txtChat.tag_config('verde', foreground='green')
        self.txtChat.tag_config('rojo', foreground='red')
                
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Texto:")
        self.var_msj = tk.StringVar()
        self.inText = tk.Entry(frm3, width=45, state='disable', textvariable=self.var_msj)
        self.btnSend = ttk.Button(frm3, text="Enviar", width=12, state='disable', command=lambda:self.enviar_msg(None))
        self.lblText.grid(row=0, column=0, padx=5, pady=5)
        self.inText.grid(row=0, column=1, padx=5, pady=5)
        self.btnSend.grid(row=0, column=2, padx=5, pady=5)
        
        self.inText.bind('<Return>', self.enviar_msg)
        self.inText.bind('<KeyRelease>', self.update_writing)
        
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        self.cboPort.bind("<<ComboboxSelected>>", self.COM_select)
        # ------------- Control del boton "X" de la ventana -----------
        self.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)
        # Recibir mensajes:
        self.th1 = threading.Thread(target=self.recibir_msg, daemon=True)
        
    def COM_select(self, event):
        self.PORT = self.cboPort.get()
        
    
    def connect(self):
        if self.btnConnect["text"]== "Conectar":
            self.statusBar.config(text=f"Conectando al {self.PORT} a 9600")
            try:
                self.ser = serial.Serial(port=self.PORT, 
                                    baudrate=9600, 
                                    bytesize=8, 
                                    timeout=2, 
                                    stopbits=serial.STOPBITS_ONE)
                                    #print("Conexión extablecida")
                self.cboPort.config(state='disable')
                self.btnConnect.config(text='Desconectar')
                self.inText.config(state='normal')
                self.btnSend.config(state='normal')
                self.txtChat.config(state='normal')
                self.th1.start()
                self.inText.delete(0,tk.END)
            except:
                self.statusBar.config(text=f"Error al conectarse a {self.PORT}")
                
        else:
            try:
                
                self.ser.close()
                self.cboPort.config(state='enable')
                self.btnConnect.config(text='Conectar')
                self.inText.config(state='disable')
                self.btnSend.config(state='disable')
                self.txtChat.config(state='disable')
                self.inText.delete(0,tk.END)
                
            except:
                None
            finally:
                self.th1 = None
    def recibir_msg(self):
        while True:
            try:
                if self.ser.in_waiting > 0:
                    # Se leen los datos y se espera el caracter EOL
                    data = self.ser.readline()
                    # Los datos recibidos son bytes. Para verlos es necesarios decodificarlos
                    string = data.decode('utf-8')
                    self.statusBar.config(text="Recibiendo mensaje...")
                    time.sleep(1)
                    self.txtChat.insert(tk.INSERT, f"{string}" + "\n", 'verde')
                    self.th1;
                
                    #print(f"Rx: {string}")
        
            except:
                print("Conexion cerrada")
                break
            
    
    def enviar_msg(self, event):
    
            string = self.var_msj.get()
            string = self.PORT+": " +string
            data = string.encode("utf-8")
            self.ser.write(data)
            self.statusBar.config(text="Enviando mensaje...")
            time.sleep(1)
            self.txtChat.insert(tk.INSERT, f"{string}" + "\n", 'rojo')
            self.inText.delete(0,tk.END)

    def cerrar_puertos(self):
        # Se cierran los puertos COM y la ventana de tkinter
        try:
            
            self.serial.close()
        except:
            pass

        self.destroy()
        
    def update_statusbar(self, message):
        self.statusBar.config(text=message)
        time.sleep(1)
        self.statusBar.config(text="")
        
    def update_writing(self, event):
        threading.Thread(target=self.update_statusbar, args=("...",)).start()
    
    
    
app = SerialChat()
app.mainloop()
#%%








