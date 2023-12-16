import customtkinter as ctk
import os
from PIL import Image
import psutil
import time
import sys
import time
import socket
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askokcancel, showinfo

#from ChatBackend import Client

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class ClientApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cliente")
        self.resizable(0,0)
        self.geometry("555x570")
        self.font_title = ctk.CTkFont(family="Arial",size=18,weight="bold")
        self.fotn_normal = ctk.CTkFont(family='Arial',size=10) 
        self.HEADER_SIZE = 10
        
        frm_principal = ctk.CTkFrame(master=self)
        frm_principal.pack(fill="both",expand=True)
        
        frm_DatosConexion = ctk.CTkFrame(master=frm_principal)
        frm_VentanaChat = ctk.CTkFrame(master=frm_principal)
        
        #self.lbl_DatosConexion.pack(fill='x',padx=15,pady=5)
        
        frm_DatosConexion.pack(fill='x',padx=10,pady=10)
        frm_VentanaChat.pack(fill='both',padx=10,pady=10)
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "arrow_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "arrow_light.png")), size=(20, 20))
        self.user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "face.jpg")),
                                                 dark_image=Image.open(os.path.join(image_path, "face.jpg")), size=(20, 20))
        #---------------------------- frm_DatosConexion----------------------------------------------------------------------------
        
        lbl_DatosConexion = ctk.CTkLabel(master=frm_DatosConexion,
                                         text="Conexion",
                                         font=self.font_title,anchor='w')
        frm_Widgets_DatosConexion = ctk.CTkFrame(frm_DatosConexion) 
        
        lbl_DatosConexion.pack(padx=20,pady=5,fill='x')
        frm_Widgets_DatosConexion.pack(padx=5,pady=5)
        
        
        #---------------------------- frm_Widgets_DatosConexion----------------------------------------------------------------------------
        
        lbl_UserName = ctk.CTkLabel(master = frm_Widgets_DatosConexion,
                                    text="Nombre de Usuario", anchor="center",
                                    width=150)
        lbl_IPAddress = ctk.CTkLabel(master = frm_Widgets_DatosConexion,
                                     text="Direccion IP", anchor="center",
                                     width=150)
        lbl_Port = ctk.CTkLabel(master = frm_Widgets_DatosConexion,
                                text="Puerto", anchor="center",width=150)
        
        self.ent_UserName = ctk.CTkEntry(master = frm_Widgets_DatosConexion,
                                         placeholder_text="Ingrese nombre de usuario",
                                         width=220)
        self.ent_IPAddress = ctk.CTkEntry(master = frm_Widgets_DatosConexion,
                                          placeholder_text="Ingrese direccion IP",
                                          width=220)
        self.ent_IPAddress.insert(0,'127.0.0.1')
        self.ent_Port = ctk.CTkEntry(master = frm_Widgets_DatosConexion,
                                     placeholder_text="Ingrese N° de Puerto",
                                     width=220)
        self.ent_Port.insert(0,'5000')
        
        self.btn_Connect = ctk.CTkButton(master = frm_Widgets_DatosConexion,
                                         text="Conectar",width=120, 
                                         command=self.CrearConexion)
        
        
        lbl_UserName.grid(row=1, column=0, padx=5, pady=5)
        lbl_IPAddress.grid(row=2, column=0, padx=5, pady=5)
        lbl_Port.grid(row=3, column=0, padx=5, pady=5)
        self.ent_UserName.grid(row=1, column=1, padx=5, pady=5)
        self.ent_IPAddress.grid(row=2, column=1, padx=5, pady=5)
        self.ent_Port.grid(row=3, column=1, padx=5, pady=5)
        self.btn_Connect.grid(row=1, column=2, padx=5, pady=5)
        
        #---------------------------- frm_Chat----------------------------------------------------------------------------
        
        self.lbl_chat = ctk.CTkLabel(frm_VentanaChat,text="Chat",anchor='w',font=self.font_title)
        self.txt_chat = ctk.CTkTextbox(frm_VentanaChat,wrap="word",height=250,
                                       width=530,state="disable")
        frm_mensaje = ctk.CTkFrame(frm_VentanaChat)
        
        self.lbl_chat.pack(padx=20,pady=5,fill='x')
        self.txt_chat.pack(padx=5,pady=5)
        frm_mensaje.pack(padx=5,pady=5,fill='x')
        
        #---------------------------- frm_Mensaje----------------------------------------------------------------------------
        
        self.btn_emojis = ctk.CTkButton(frm_mensaje,state='disable',text='Emojis',
                                        width=70)
        self.ent_mensaje = ctk.CTkEntry(master=frm_mensaje, state='disable',
                                        placeholder_text="Escribe un mensaje", width=350)
        self.btn_enviar = ctk.CTkButton(frm_mensaje, state='disable',text='',
                                        width=70,height=20,command=self.EnviarMensajes , image=self.chat_image)
        
        self.btn_emojis.grid(row=0,column=0,padx=5,pady=5)
        self.ent_mensaje.grid(row=0,column=1,padx=5,pady=5)
        self.btn_enviar.grid(row=0,column=2,padx=5,pady=5)
        
        self.ent_mensaje.bind('<Return>',self.EnviarMensajes)
        
        self.statusBar = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.protocol("WM_DELETE_WINDOW",self.DestruirVentana)
        
        # ------------- tags para el texto -----------
    
        #self.txtChat.tag     
    
        
    def CrearConexion(self):
#       
        self.username = self.ent_UserName.get()
        #Se establece el socket del cliente (socket, connect)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ent_IPAddress.get(),int(self.ent_Port.get())))        
        
        th1=threading.Thread(target=self.RecepcionMensajes,daemon=True)
        th1.start()
            
        #self.ChatClient = Client(self.ent_IPAddress.get(),int(self.ent_Port.get()),
        #                         self.ent_UserName.get())
        self.lbl_chat.configure(image=self.user_image, text=f'\t {self.ent_UserName.get()}')
        self.ent_UserName.configure(state='disable')
        self.ent_IPAddress.configure(state='disable')
        self.ent_Port.configure(state='disable')
        self.btn_Connect.configure(text='Desconectar', command=self.DestruirConexion)
        self.txt_chat.configure(state='normal',)
        self.btn_emojis.configure(state='normal')
        self.ent_mensaje.configure(state='normal',placeholder_text="Escribe un mensaje")
        self.btn_enviar.configure(state= 'normal')
    
    def RecepcionMensajes(self):
        while True:
            # Recibe el encabezado de los mensajes entrantes
            data_header = self.sock.recv(self.HEADER_SIZE)
            
            # Si no hay datos entrantes se cancela el proceso
            if not data_header:
                break
            
            # De lo contrario, se recibe el mensaje y se muestra
            # "username > mensaje"
            data = self.sock.recv(int(data_header))
            self.txt_chat.configure(state='normal')
            self.txt_chat.insert(tk.INSERT, data.decode('utf-8')+'\n')
            self.txt_chat.configure(state='disable')
            print(data.decode('utf-8'))
    
    def EnviarMensajes(self, event=None):
        if self.ent_mensaje.get()=='':
            return
        mensaje=self.ent_mensaje.get()
        # Se pide al usuario que ingrese el mensaje y se encapsula con un header
        # para su envio
        strData = f"{self.username}: {mensaje} " 
        data_len = len(strData + self.username + "> ")
                
        self.sock.send(f"{data_len:<{self.HEADER_SIZE}}{strData}".encode('utf-8'))
        self.ent_mensaje.delete(0,tk.END)
        
        
    def DestruirConexion(self):
    
        data_len = len("END")
                
        self.sock.send(f"{data_len:<{self.HEADER_SIZE}}END".encode('utf-8'))
        
        print('conexion destruida')
        
        
        self.ent_UserName.configure(state='normal')
        self.ent_IPAddress.configure(state='normal')
        self.ent_Port.configure(state='normal')
        self.btn_Connect.configure(text='Conectar', command=self.CrearConexion)
        self.txt_chat.configure(state='disable',)
        self.btn_emojis.configure(state='disable')
        self.ent_mensaje.configure(state='disable',placeholder_text="Escribe un mensaje")
        self.btn_enviar.configure(state= 'disable')
        
    def UpdateStatusBar(self,opcion):
        if opcion==0:
            self.statusBar.config(text='')
        elif opcion==1:
            self.statusBar.config(text="Conexion Establecida")
            self.root.after(2000,lambda:self.UpdateStatusBar(0))
        elif opcion==2:
            self.statusBar.config(text="Conexion Finalizada")
            self.root.after(2000,lambda:self.UpdateStatusBar(0))
        elif opcion==3:
            self.statusBar.config(text='Algo salio mal...')
            self.root.after(2000,lambda:self.UpdateStatusBar(0))
        elif opcion==4:
            self.statusBar.config(text='Enviando Mensaje...')
            self.root.after(2000,lambda:self.UpdateStatusBar(0))
        elif opcion==5:
            self.statusBar.config(text='Recibiendo Mensaje...')
            self.root.after(2000,lambda:self.UpdateStatusBar(0))
        
    def DestruirVentana(self):
        try:
            self.DestruirConexion()
        except:
            pass
        self.destroy()        
           

        
        
    
        
app=ClientApp()
app.mainloop()