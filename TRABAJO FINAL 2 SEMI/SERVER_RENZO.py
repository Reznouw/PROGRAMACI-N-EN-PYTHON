import customtkinter
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


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Servidor.py")
        self.geometry("700x500")
        self.font_title = customtkinter.CTkFont(family="Arial",size=24,weight="bold")
        self.font_button = customtkinter.CTkFont(family="Arial",size=18,weight="bold")
        self.lista_uso_cpu = [0] * 50  # Lista circular para el uso de CPU en tiempo real
        self.idx_uso_cpu = 0  # Índice actual en la lista circular
        self.delay = 1000
        self.HEADER_SIZE = 10
        # ------------------------ Establecer diseño de cuadrícula 1x2 -----------------------------
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ------------------------ Cargamos imágenes con imagen en modo claro y oscuro -----------------------------
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(100, 100))
        
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.apagar = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "apagar_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "apagar_light.png")), size=(20, 20))
        self.stop = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "stop_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "stop_light.png")), size=(20, 20))
        # ------------------------ Frame de Navegacion -----------------------------
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Aternos", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Servidor",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Consola",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Rendimiento",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # ------------------------ Frames Home -----------------------------
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        
       # ------------------------ FRAME 1 ----------------------------
        self.home_frame_label_1 = customtkinter.CTkLabel(self.home_frame,text="Aternos.com",font=self.font_title )
        self.home_frame_label_1.grid(row=1, column=0, padx=20, pady=10)
        # ------------------------ FRAME 2 ----------------------------
        self.home_frame_label_2 = customtkinter.CTkLabel(self.home_frame,text="Desconectado",font=self.font_button, fg_color="red",width=150)
        self.home_frame_label_2.grid(row=2, column=0, padx=20, pady=10)
        
        # ------------------------ FRAME 3 ----------------------------
        self.home_frame_label_3 = customtkinter.CTkLabel(self.home_frame, text="")
        self.home_frame_label_3.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_Connect2 = customtkinter.CTkButton(master = self.home_frame_label_3,
                                         text="Iniciar",width=200, height=30, 
                                         command=self.CrearConexion,font=self.font_button, image=self.apagar)
        
        self.btn_Connect2.grid(row=1, column=2, padx=5, pady=5)
        
        # ------------------------ FRAME 4 ----------------------------
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=4, column=0, padx=20, pady=10)
        # ------------------------ FRAME 5 ----------------------------
        self.home_frame_label_4 = customtkinter.CTkLabel(self.home_frame, text="", corner_radius=0, fg_color="transparent")
        self.home_frame_label_4.grid(row=5, column=0, padx=20, pady=10)
        
        self.lbl_UserName = customtkinter.CTkLabel(master = self.home_frame_label_4,
                                    text="Dominio", anchor="center",
                                    width=150,fg_color="transparent", text_color=("gray10", "gray90"))
        lbl_IPAddress = customtkinter.CTkLabel(master = self.home_frame_label_4,
                                     text="Direccion IP", anchor="center",
                                     width=150,fg_color="transparent",)
        lbl_Port = customtkinter.CTkLabel(master = self.home_frame_label_4,
                                text="Puerto", anchor="center",width=150 ,fg_color="transparent")
        
        self.ent_UserName = customtkinter.CTkEntry(master = self.home_frame_label_4,
                                         placeholder_text="Ingrese nombre de dominio",
                                         width=220,fg_color="transparent")
        self.ent_IPAddress = customtkinter.CTkEntry(master = self.home_frame_label_4,
                                          placeholder_text="Ingrese direccion IP",
                                          width=220,fg_color="transparent")
        self.ent_IPAddress.insert(0,'127.0.0.1')
        self.ent_Port = customtkinter.CTkEntry(master = self.home_frame_label_4,
                                     placeholder_text="Ingrese N° de Puerto",
                                     width=220,fg_color="transparent")
        self.ent_Port.insert(0,'5000')
        self.btn_Connect = customtkinter.CTkButton(master = self.home_frame_label_4,
                                         text="Enviar",width=120, 
                                         command=self.dominio)
        
        self.lbl_UserName.grid(row=1, column=0, padx=5, pady=5)
        lbl_IPAddress.grid(row=2, column=0, padx=5, pady=5)
        lbl_Port.grid(row=3, column=0, padx=5, pady=5)
        self.ent_UserName.grid(row=1, column=1, padx=5, pady=5)
        self.ent_IPAddress.grid(row=2, column=1, padx=5, pady=5)
        self.ent_Port.grid(row=3, column=1, padx=5, pady=5)
        self.btn_Connect.grid(row=1, column=2, padx=5, pady=5)    
        
        

        # ------------------------ Frames Second -----------------------------
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid(row=1, column=0, padx=20, pady=10)
        
        lbl_chat = customtkinter.CTkLabel(self.second_frame,text="Consola",anchor='w',font=self.font_title)
        self.txt_chat = customtkinter.CTkTextbox(self.second_frame,wrap="word",height=250,width=530,state="disable")
        
        
        lbl_chat.pack(padx=20,pady=5,fill='x')
        self.txt_chat.pack(padx=5,pady=5)
        
        
        # ------------------------ Frames Third -----------------------------
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid(row=1, column=0, padx=20, pady=10)
        
        self.rendimiento = customtkinter.CTkLabel(self.third_frame,text="Rendimiento",anchor='w',font=self.font_title)
        self.lbl_cpu_usage = tk.Label(self.third_frame, text='CPU Usage:',bg="gray15",fg="white")
        self.progressbar_cpu_usage = ttk.Progressbar(self.third_frame, length=500)
        self.lbl_ram_usage = tk.Label(self.third_frame, text='RAM Usage',bg="gray15",fg="white")
        self.progressbar_ram_usage = ttk.Progressbar(self.third_frame, length=500)
        self.lbl_hdd_usage = tk.Label(self.third_frame, text='HDD Usage',bg="gray15",fg="white")
        self.progressbar_hdd_usage = ttk.Progressbar(self.third_frame, length=500)

        self.rendimiento.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        self.lbl_cpu_usage.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        self.progressbar_cpu_usage.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_ram_usage.grid(row=2, column=0, padx=5, pady=5, sticky='W')
        self.progressbar_ram_usage.grid(row=3, column=0, padx=5, pady=5)
        self.lbl_hdd_usage.grid(row=4, column=0, padx=5, pady=5, sticky='W')
        self.progressbar_hdd_usage.grid(row=5, column=0, padx=5, pady=5)
        self.Actualizar_info()

        # ------------------------ Select default Frame -----------------------------
        self.select_frame_by_name("home")
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,bg="gray15",fg="white")
        self.statusBar.grid(row=8, column=1, padx=5, pady=5)
        # ------------- Control del boton "X" de la ventana -----------
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)  
        
        
    def run(self):
        self.txt_chat.configure(state='normal')
        self.txt_chat.insert(tk.INSERT, "Servidor iniciado. Esperando conexiones...\n" )
        self.txt_chat.configure(state='disable')
        print("Servidor iniciado. Esperando conexiones...")
        while True:
            # Se aceptan las conexiones entrantes
            conn, addr = self.sock.accept()
            
            # Se levanta el thread de manejo de las conexiones entrantes
            th2 = threading.Thread(target=self.handler, args=(conn, addr), daemon=True)
            th2.start()
            
            # Informa sobre la conexion entrante
            frase=str(addr[0]) + ':' + str(addr[1])+" " + "connected\n"
            self.txt_chat.configure(state='normal')
            self.txt_chat.insert(tk.INSERT, frase )
            self.txt_chat.configure(state='disable')
            print(frase)
            
            # Se agrega el socket cliente a la lista de conexiones
            self.connections.append(conn)    
        
    def handler(self, conn, addr):
        while True:
            # Si es que no hay problemas con la conexion del cliente...
            try:
                # Lee el encabezdo para el buffer y los datos entrantes
                data_header = conn.recv(self.HEADER_SIZE)
                data = conn.recv(int(data_header))
                data_decode = data.decode("utf-8")
                print("probando")
                print(data_decode)
                self.txt_chat.configure(state='normal')
                self.txt_chat.insert(tk.INSERT, data_decode+'\n' )
                self.txt_chat.configure(state='disable')
                # Hace ub broadcast del dato entrante a los otros sockets
                for connection in self.connections:
                    connection.send(data_header + data)
                    
            # Si hay problemas con la conexion del cliente...
            except:
                # El cliente se ha desconectado. Informar y eliminar a conexionj
                frase=str(addr[0]) + ':' + str(addr[1])+" " + "disconencted\n"
                self.txt_chat.configure(state='normal')
                self.txt_chat.insert(tk.INSERT, frase)
                self.txt_chat.configure(state='disable')
                print(frase)
                self.connections.remove(conn)
                conn.close()
                break      
    
    def CrearConexion(self):
        try:
            self.connections = []
            # Se establece el socket del servidor (socket, bind, listen)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permite eliminar el error "socket already in use"
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.ent_IPAddress.get(), int(self.ent_Port.get())))
            self.sock.listen()
            print('chatserver creado')
            
        except:
            self.UpdateStatusBar(3)
            return
        
        self.btn_Connect2.configure(text="Apagar",width=200, height=30, 
                                        font=self.font_button, image=self.stop, fg_color="red",command=self.DestruirConexion)
        self.home_frame_label_2.configure(text="Conectado",fg_color="green")
        self.ent_UserName.configure(state='disable')
        self.ent_IPAddress.configure(state='disable')
        self.ent_Port.configure(state='disable')
        self.btn_Connect.configure(state='disable')
        self.UpdateStatusBar(1)
        #self.txt_chat.configure(state='normal',)
        th1= threading.Thread(target=self.run,daemon=True)
        th1.start()
        
             
    
    def DestruirConexion(self):
        try:
            try:
                for conexion in self.connections:
                    conexion.close()
            except:
                pass
        except:
            self.UpdateStatusBar(3)
            return
        self.btn_Connect2.configure(text="Iniciar",width=200, height=30, 
                                        font=self.font_button, image=self.stop, fg_color="green",command=self.CrearConexion)
        self.home_frame_label_2.configure(text="Desconectado",fg_color="red")
        self.ent_Port.configure(state="normal")
        self.ent_IPAddress.configure(state="normal")
        self.txt_chat.configure(state='normal')
        self.txt_chat.insert(tk.INSERT, "Servidor Desconectado\n" )
        self.txt_chat.configure(state='disable')
        self.UpdateStatusBar(2)
        print('chatserver Cerrando')
    
    def UpdateStatusBar(self,opcion):
        if opcion==0:
            self.statusBar.config(text='')
        elif opcion==1:
            self.statusBar.config(text="Conexion Establecida")
            self.after(2000,lambda:self.UpdateStatusBar(0))
        elif opcion==2:
            self.statusBar.config(text="Conexion Finalizada")
            self.after(2000,lambda:self.UpdateStatusBar(0))
        elif opcion==3:
            self.statusBar.config(text='Algo salio mal...')
            self.after(2000,lambda:self.UpdateStatusBar(0))
    
    def cerrar_ventana(self):
        
        try:
            try:
                for conexion in self.connections:
                    conexion.close()
            except:
                pass 
        except:
            pass
        self.destroy()
        
    def dominio(self):
      #  if self.ent_UserName != "":
        self.home_frame_label_1.configure(text=self.ent_UserName.get())
   # else:
    def Actualizar_info(self):
        # Obtenemos las estadísticas de uso
        cpu_percent = psutil.cpu_percent()
        virtual_memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('C:\\')

        # Actualizamos nuestras etiquetas y barras de progreso
        self.lbl_cpu_usage.config(text=f"CPU Usage ({psutil.cpu_count()} cores): {cpu_percent:.2f}%")
        self.progressbar_cpu_usage['value'] = cpu_percent
        self.lbl_ram_usage.config(text=f"RAM Usage (Total: {virtual_memory.total / (1024 ** 3):.2f} Gb): {virtual_memory.percent}%")
        self.progressbar_ram_usage['value'] = virtual_memory.percent
        self.lbl_hdd_usage.config(text=f"HDD Usage (Total: {disk_usage.total / (1024 ** 3):.2f} Gb): {disk_usage.percent}%")
        self.progressbar_hdd_usage['value'] = disk_usage.percent

        

        

        
        self.after(self.delay, self.Actualizar_info)
        
    
        
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
    
    
    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
