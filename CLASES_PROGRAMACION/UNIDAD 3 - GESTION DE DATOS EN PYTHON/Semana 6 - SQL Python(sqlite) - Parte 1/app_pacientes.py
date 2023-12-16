# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from data_tools import Database
from tkinter.messagebox import showerror, askokcancel

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Pacientes")
        self.resizable(0, 0)
        
        self.dB = Database()
        
        self.var_nombre = tk.StringVar()
        self.var_peso = tk.StringVar()
        self.var_altura = tk.StringVar()
        self.cambiando_db = False
        
        frm = tk.Frame(self)
        frm.pack()
        
        frm1 = tk.Frame(frm)
        frm2 = tk.Frame(frm)
        frm1.pack(padx=10, pady=10)
        frm2.pack(padx=10, pady=10)
        
        frmCombo = tk.Frame(frm1)
        frmEntrys = tk.Frame(frm1)
        frmCombo.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.N)
        frmEntrys.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.N)
        
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        
        self.menu.add_command(label="Mostrar Tabla", command=self.table_window)
        
        # ----------------------------- frm1 ----------------------------------
        self.cboNombres = ttk.Combobox(frmCombo, state='readonly', 
                                       values=self.dB.listar_pacientes_by_nombre())
        self.lblNombre = tk.Label(frmEntrys, text="Nombre:")
        self.lblPeso = tk.Label(frmEntrys, text="Peso:")
        self.lblAltura = tk.Label(frmEntrys, text="Altura:")
        self.entNombre = tk.Entry(frmEntrys, state='disable', textvariable=self.var_nombre)
        self.entPeso = tk.Entry(frmEntrys, state='disable', textvariable=self.var_peso)
        self.entAltura = tk.Entry(frmEntrys, state='disable', textvariable=self.var_altura)
        
        self.cboNombres.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.lblNombre.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.lblPeso.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.lblAltura.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.entNombre.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.entPeso.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.entAltura.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # ----------------------------- frm2 ----------------------------------
        self.btnCrear = tk.Button(frm2, text="Agregar Paciente", 
                                  state='normal', width=16,
                                  command=self.agregar_paciente)
        self.btnActualizar = tk.Button(frm2, text="Actualizar Paciente", 
                                       state='disable', width=16, 
                                       command=self.actualizar_paciente)
        self.btnEliminar = tk.Button(frm2, text="Eliminar Paciente", 
                                     state='disable', width=16, 
                                     command=self.eliminar_paciente)
        
        self.btnCrear.grid(row=0, column=0, padx=5, pady=5)
        self.btnActualizar.grid(row=0, column=1, padx=5, pady=5)
        self.btnEliminar.grid(row=0, column=2, padx=5, pady=5)
        
        self.cboNombres.bind("<<ComboboxSelected>>", self.mostrar_campos)
        
        
    def mostrar_campos(self, event):
        # Se muestran los campos segun lo seleccionado en el 
        # Combobox
        nombre = self.cboNombres.get()
        peso, altura = self.dB.data_paciente_by_name(nombre)
        self.var_nombre.set(nombre)
        self.var_peso.set(peso)
        self.var_altura.set(altura)
        
        self.btnActualizar.config(state='normal')
        self.btnEliminar.config(state='normal')
        
        
    def agregar_paciente(self):
        if self.cambiando_db:
            # Agregar un registro
            ret = self.dB.agregar_paciente(self.var_nombre.get(), 
                                        self.var_peso.get(), 
                                        self.var_altura.get())
            
            # Actualizar el Combobox
            self.cboNombres.config(values=self.dB.listar_pacientes_by_nombre())
            
            self.btnCrear.config(text="Agregar Paciente")
            self.var_nombre.set('')
            self.var_peso.set('')
            self.var_altura.set('')            
            self.entNombre.config(state="disable")
            self.entPeso.config(state="disable")
            self.entAltura.config(state="disable")
            self.btnActualizar.config(state='disable')
            self.btnEliminar.config(state='disable')
            self.cambiando_db = False
            
            if not ret:
                showerror("Error", "No se pudo agregar la informacion del paciente a la base de datos")
                
        else:
            self.var_nombre.set('')
            self.var_peso.set('')
            self.var_altura.set('') 
            self.cboNombres.set('')
            self.btnCrear.config(text="Guardar Paciente")
            self.entNombre.config(state="normal")
            self.entPeso.config(state="normal")
            self.entAltura.config(state="normal")
            self.btnActualizar.config(state='disable')
            self.btnEliminar.config(state='disable')
            self.cambiando_db = True
            
            
            
    def actualizar_paciente(self):
        if self.cambiando_db:
            # Actualizar un registro
            ret = self.dB.actualiza_paciente_by_name(self.var_nombre.get(), 
                                                     self.var_peso.get(), 
                                                     self.var_altura.get())
            
            self.btnActualizar.config(text="Actualizar Paciente")
            self.var_nombre.set('')
            self.var_peso.set('')
            self.var_altura.set('')            
            self.entNombre.config(state="disable")
            self.entPeso.config(state="disable")
            self.entAltura.config(state="disable")
            self.btnCrear.config(state='normal')
            self.btnActualizar.config(state='disable')
            self.btnEliminar.config(state='disable')
            self.cambiando_db = False
            
            self.mostrar_campos(None)
            
            if not ret:
                showerror("Error", "No se pudo actualizar los cambios del paciente a la base de datos")
            
        else:
            self.btnActualizar.config(text="Guardar Paciente")
            self.entNombre.config(state="disable")
            self.entPeso.config(state="normal")
            self.entAltura.config(state="normal")
            self.btnCrear.config(state='disable')
            self.btnEliminar.config(state='disable')
            self.cambiando_db = True
    
    
    def eliminar_paciente(self):
        # Confirmar si se quiere eliminar el paciente
        # en caso de confirmar se debe de eliminar el registro
        if askokcancel("Eliminar Paciente", 
                       "Esta seguro que quiere eliminar este registro?"):
            ret = self.dB.eliminar_paciente(self.var_nombre.get())
            
            self.var_nombre.set('')
            self.var_peso.set('')
            self.var_altura.set('') 
            self.cboNombres.set('')
            self.cboNombres.config(values=self.dB.listar_pacientes_by_nombre())
            self.btnActualizar.config(state='disable')
            self.btnEliminar.config(state='disable')
    
            if not ret:
                showerror("Error", "No se pudo eliminar el registro de la base de datos")
        else:
            self.var_nombre.set('')
            self.var_peso.set('')
            self.var_altura.set('') 
            self.cboNombres.set('')
        
        
    def table_window(self):
        Table_Window(self.dB)
    
        
class Table_Window(tk.Toplevel):
    def __init__(self, dB):
        super().__init__()
        self.title("Tabla de Pacientes")
        self.resizable(0, 0)
        self.focus()
        self.grab_set()
        
        frm = tk.Frame(self)
        frm.pack(padx=10, pady=10)
        
        style = ttk.Style()
        style.theme_use('default')
        
        table = ttk.Treeview(frm, columns=(1, 2, 3))
        table.pack()
        
        table.tag_configure('par', background='#888888')
        table.tag_configure('impar', background='#474747')
        
        table.heading('#0', text="ID")
        table.heading('#1', text="Nombre")
        table.heading('#2', text="Peso")
        table.heading('#3', text="Altura")
        
        table.column('#0', width=30, minwidth=30, stretch=tk.NO)
        table.column('#1', width=150, minwidth=150, stretch=tk.NO)
        table.column('#2', width=80, minwidth=80, stretch=tk.NO, anchor=tk.CENTER)
        table.column('#3', width=80, minwidth=80, stretch=tk.NO, anchor=tk.CENTER)
        
        for idx, item in enumerate(dB.data_pacientes()):
            if idx % 2 == 0:
                table.insert("", tk.END, text=item[0], values=item[1:], tags=("par",))
            else:
                table.insert("", tk.END, text=item[0], values=item[1:], tags=("impar",))
            


App().mainloop()