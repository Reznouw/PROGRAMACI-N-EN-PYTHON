import os
import sys
import time
import socket
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

header_size=10

class Server:
    def __init__(self, master):
        
        self.master = master        
        self.master.title(f"Servidor para clientes (SERVIDOR)")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)        
        self.text=tk.StringVar()
        self.text.set("Conectar")
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self.master, text="Ingrese al servidor")
        frm2 = tk.Frame(self.master)
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)  
        # ------------------------ FRAME 1 ----------------------------
        self.btn_guardar = ttk.Button(frm2, text="Guardar", width=16, command=self.boton_guardar)
        self.btn_guardar.grid(row=0, column=2, padx=15, pady=5)
        self.btn_conectar = ttk.Button(frm2, textvariable=self.text, width=16, command=self.validacion)
        self.btn_conectar.grid(row=2, column=0, padx=5, pady=5)
        self.direccion=tk.Label(frm2, text="Dirección IP: 127.0.0.1")    
        self.direccion.grid(row=2,column=2, padx=50, pady=5)
        self.port=tk.Label(frm1, text="Puerto: 5000")
        self.port.grid(row=1,column=4, padx=30, pady=5)
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=25, width=50, wrap=tk.WORD, state='normal')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        # ------------- Control del boton "X" de la ventana -----------
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)                
  
    def run(self):
        
        print("\n**************************************************")
        print("\n---Servidor iniciado, esperando conexiones---------")
        print("\n***************************************************")
        hora=time.strftime("Inicio: %d-%m-%Y, %H:%M:%S", time.localtime())
        self.statusBar.config(text="Servidor conectado")
        self.txtChat.config(state="normal")
        self.txtChat.insert(tk.INSERT,"\n*************************\n   Esperando Conexión "+"\n"+hora+'\n'+"-------------------------------------------------\n", "green")
        self.txtChat.tag_config('green', foreground='green', justify="center")
        self.txtChat.config(state="disable")
        
        while True:
            conn, addr= self.sock.accept() 
            
            if len(self.connections)==0:
                pass
            else:
                strdata="----Un nuevo usuario se ha unido----"
                data_len=str(len(strdata))
                data=f"{data_len:<{header_size}}{strdata}".encode("utf-8")
                self.txtChat.config(state="normal")
                self.txtChat.insert(tk.INSERT,strdata+'\n', "blue")
                self.txtChat.tag_config('blue', foreground='blue',justify="center")
                self.txtChat.config(state="disable")
        
                for i in self.connections:
                    i.send(data)
                        
            threading.Thread(target=self.handler, args=(conn,addr),daemon=True).start()
            a=f"{addr[0]}:{addr[1]}  conectado"
            print(a)            
            self.txtChat.config(state="normal")
            self.txtChat.insert(tk.INSERT,a+'\n', "blue")
            self.txtChat.tag_config('blue', foreground='blue')
            self.txtChat.config(state="disable")
            self.connections.append(conn)      
            
            strdata2="Se ha unido al servidor "
            
            data_len2=str(len(strdata2))
            data2=f"{data_len2:<{header_size}}{strdata2}".encode("utf-8")
            conn.send(data2)
            
    def handler(self, conn,addr):
        while True:
            try:
                data_header=conn.recv(header_size)
                data = conn.recv(int(data_header))
                data_decode=data.decode("utf-8")
                if data_decode[-3:]=="END":
                    usuario=f"Un usuario se ha desconectado"
                    print(usuario)
                    self.txtChat.config(state="normal")
                    self.txtChat.insert(tk.INSERT,f"{addr[0]}:{addr[1]}  desconectado"+"\n", "blue")
                    self.txtChat.tag_config('blue', foreground='blue', justify="center")
                    self.txtChat.config(state="disable")
                    self.connections.remove(conn)
                    conn.close
                    salida_len=str(len(usuario))
                    data_de=f"{salida_len:<{header_size}}{usuario}".encode("utf-8")
                    for connection in self.connections:
                        connection.send(data_de)
                else:
                    print(data)
                       
                    self.txtChat.config(state="normal")
                    self.txtChat.insert(tk.INSERT,data_decode+"\n", "black")
                    self.txtChat.tag_config('black', foreground='black')
                    self.txtChat.config(state="disable")
                    
                    for connection in self.connections:
                        if connection ==conn:
                            pass
                        else:
                            connection.send(data_header+data)
                    
            except:
                break
            
    def boton_guardar(self):#guardamos el servidor en una direccion especifica
        
        self.txtChat.config(state="normal")
        self.statusBar.config(text="Servidor guardado")
        texto=self.txtChat.get("1.0", tk.END)
        archivo=open("nombre_servidor.txt","w")
        archivo.write(texto)
        archivo.close()
        
    def conectar_servidor(self):#conectamos el servidor
        try:
            self.text.set("Desconectar")      
            header_size=10 
            port=5000
            host="127.0.0.1"                                   
            self.connections=[]
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.sock.bind((host,port))
            self.sock.listen()
            threading.Thread(target=self.run, daemon=True).start()
             
        except:
            self.statusBar.config(text="El server no se pudo iniciar")
            
    def desconectar_servidor(self):#desconectamos el servidoro
        try:
            for conn in self.connections:
                conn.close()
            
            self.text.set("Conectar")
            
            self.txtChat.config(state="normal")
            self.txtChat.insert(tk.INSERT,f"Server desconectado"+"\n", "red")
            self.txtChat.tag_config('red', foreground='red', justify="center")            
            self.txtChat.config(state="disable")
            self.txtChat.config(state="normal")
            self.txtChat.delete("1.0",tk.END) 
            self.txtChat.config(state="disabled")
            self.statusBar.config(text="Servidor desconectado")
        except:
            pass
         
    def validacion (self):#validamos si presiona el boton para que inicie la conexion
        i=self.text.get()
        if i=="Conectar":
            self.conectar_servidor()            
        else:
            self.desconectar_servidor()            
                
    def cerrar_puertos(self): # Se cierran los puertos COM y la ventana de tkinter
       
        try:
            for conn in self.connections:
                conn.close()           
        except:
            pass
        self.master.destroy()   
        
root = tk.Tk()
app = Server(root)
root.mainloop()