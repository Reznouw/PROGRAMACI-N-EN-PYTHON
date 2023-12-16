import sys
import time
import socket
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askokcancel, showinfo

header_size=10

class Cliente:
    def __init__(self, master):
        self.master = master             
        self.master.title(f"Pantalla de CHAT")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)
        self.ip=tk.StringVar()
        self.ip.set("127.0.0.1")        
        self.puerto=tk.StringVar()
        self.puerto.set("5000")        
        self.username=tk.StringVar()        
        self.header_size=10        
        self.text = tk.StringVar()
        self.text.set("Conectar")
        
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self.master, text="Datos para la conexion")
        frm3 = tk.Frame(self.master)
        frm2 = tk.LabelFrame(self.master, text="Enviar mensaje")
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm3.pack(padx=5, pady=5, fill='y', expand=True)
        frm2.pack(padx=5, pady=5)        
        # ------------------------ FRAME 1 ----------------------------
        self.usuario=tk.Label(frm1, text="Nickname")
        self.user=tk.Entry(frm1, textvariable=self.username)       
        self.direccion=tk.Label(frm1, text="Dirección IP")
        self.ip_direccion=tk.Entry(frm1, textvariable=self.ip)
        self.ip_direccion.config(state="disable")        
        self.port=tk.Label(frm1, text="Puerto")
        self.port_number=tk.Entry(frm1,textvariable=self.puerto)
        self.port_number.config(state="disable")        
        self.btnConnect = ttk.Button(frm1, textvariable=self.text, width=16, command=self.validacion )
        self.usuario.grid(row=0, column=0, padx=5, pady=5)
        self.user.grid(row=0, column=1, padx=5, pady=5)
        self.direccion.grid(row=1,column=0, padx=30, pady=5)
        self.ip_direccion.grid(row=1, column=1, padx=5, pady=5)
        self.port.grid(row=2,column=0,padx=5,pady=5)
        self.port_number.grid(row=2,column=1, padx=5,pady=5)        
        self.btnConnect.grid(row=0, column=2,padx=5, pady=5)        
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=15, width=50, wrap=tk.WORD, state='disable')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)                
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Texto:")
        self.inText = tk.Entry(frm3, width=45, state='disable')
        self.btnSend = ttk.Button(frm3, text="Enviar", width=12, state='disable', command=self.enviar_mensaje)
        self.lblText.grid(row=0, column=0, padx=5, pady=5)
        self.inText.grid(row=0, column=1, padx=5, pady=5)
        self.btnSend.grid(row=0, column=2, padx=5, pady=5)               
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)            
        # ------------- Control del boton "X" de la ventana -----------
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)                        
            
    def recibir_mensaje (self):
        while True:
            data_header=self.sock.recv(10)
          
            if not data_header:
                break
            else:
                self.txtChat.config(state="normal")
                data=self.sock.recv(int(data_header))
                mensaje_entrada=data.decode("utf-8")
                print(mensaje_entrada)
                if ":" in mensaje_entrada:
                    self.txtChat.insert(tk.INSERT,mensaje_entrada+'\n',"black")
                    self.txtChat.tag_config('black', foreground='black')
                else:
                    self.txtChat.insert(tk.INSERT,mensaje_entrada+'\n',"rojo")
                    self.txtChat.tag_config('rojo', foreground='red')
                    self.txtChat.tag_configure("rojo", justify="center")
                self.txtChat.config(state="disable")
        
    def enviar_mensaje (self):
       
        try:
            mensaje=self.inText.get()
            self.inText.delete(0,"end")
            username=self.username.get()
            
            self.txtChat.config(state="normal")
            times=time.strftime("%I:%M:%S %p", time.localtime())
            self.txtChat.insert(tk.INSERT,username+":"+" "+mensaje+'\n'+"\t\t\t\t       "+times+'\n', "blue")
            self.txtChat.tag_config('blue', foreground='blue')
            
            newmsg=username+":"+" "+mensaje+'\n'+"\t\t\t\t       "+times+'\n'
            self.txtChat.config(state="disable")
            
            data_len = len(newmsg)
            self.sock.send(f"{data_len:<{header_size}}{username}: {mensaje}\n\t\t\t\t       {times}".encode("utf-8"))
        
        except:
            self.statusBar.config(text="Error al enviar mensaje")

    def conectar_servidor(self):
        try:
            
            self.text.set("Desconectar")
            self.inText.config(state="normal")
            self.btnSend.config(state="normal")
            self.user.config(state="disable")
            address=self.ip.get()
            port=self.puerto.get()
            username=self.username.get()
      
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((address,int(port)))
            self.statusBar.config(text="Conectando")
            
            threading.Thread(target=self.recibir_mensaje, daemon=True).start()
            
        except:
            self.statusBar.config(text="Error de conexion") 
    
    def desconectar_servidor(self):
        try:
            
            self.statusBar.config(text="")
            self.text.set("Conectar")
            self.btnSend.config(state="disabled")
            self.inText.delete(0,"end")
            self.inText.config(state="disabled")
            data_len = len("END")
            self.sock.send(f"{data_len:<{header_size}}END".encode("utf-8"))
            self.txtChat.config(state="normal")
            self.txtChat.delete("1.0",tk.END) 
            self.txtChat.config(state="disabled")
            self.user.config(state="normal")          
            
        except:
            pass
                
    def validacion(self):#validamos si presiona el boton para que inicie la conexion
        i=self.text.get()
        if i=="Conectar":
            self.conectar_servidor()
        else:
            self.desconectar_servidor()
            
    def cerrar_puertos(self):# Se cierran los puertos COM y la ventana de tkinter
        
        try:
            data_len = len("END")
            self.sock.send(f"{data_len:<{header_size}}END".encode("utf-8"))    
        except:
            pass
        self.master.destroy()
        
root = tk.Tk()
app = Cliente(root)
root.mainloop()