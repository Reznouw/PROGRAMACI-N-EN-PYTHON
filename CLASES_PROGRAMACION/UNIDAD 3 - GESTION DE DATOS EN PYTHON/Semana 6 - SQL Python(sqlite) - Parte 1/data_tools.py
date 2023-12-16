# -*- coding: utf-8 -*-
import sqlite3

class Database:
    datafile = "database.db"
    def __init__(self):
        self.conn = sqlite3.connect(Database.datafile)
        self.cur = self.conn.cursor()
        
        
    def __del__(self):
        self.conn.close()
        
        
    def data_pacientes(self):
        '''Retorna una lista con todos los campos de los pacientes en
        tuplas'''
        return self.cur.execute("SELECT * FROM pacientes").fetchall()
    
    
    def peso_altura_by_id(self, id_pac):
        '''Retorna una tupla con en formato (peso, altura) de una paciente
        segun el id'''
        self.cur.execute("SELECT peso, altura FROM pacientes WHERE id = ?", (id_pac,))
        data = self.cur.fetchone()
        if data != None:
            return data
        else:
             raise ValueError("El campo 'id' no existe en la tabla PACIENTES")
        
    
    
    def data_paciente_by_name(self, name):
        '''Retorna una tupla con el formato (peso, altura) de un paciente
        segun el nombre'''
        self.cur.execute("SELECT peso, altura FROM pacientes WHERE nombre = ?",
                         (name,))
        data = self.cur.fetchone()
        if data != None:
            return data
        else:
             raise ValueError("El campo 'name' no existe en la tabla PACIENTES")
        
    
    def listar_pacientes_by_nombre(self):
        '''Retorna una lista con los nombres de los pacientes de la tabla pacientes 
        ordenados de forma alfabetica'''
        self.cur.execute("SELECT nombre FROM pacientes ORDER BY nombre")
        return [item[0] for item in self.cur]
    
    
    def agregar_paciente(self, nombre, peso, altura):
        '''Agrega un registro a la base de datos pacientes'''
        try:
            self.cur.execute("""INSERT INTO pacientes 
                             (nombre, peso, altura) 
                             VALUES (?, ?, ?)""", (nombre, peso, altura))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False
        
        
    def actualiza_paciente_by_name(self, nombre, peso, altura):
        '''Actualiza los datos de un paciente segun el nombre en la tabla
        pacientes'''
        try:
            self.cur.execute("""UPDATE pacientes 
                                 SET peso = ?, altura = ? 
                                 WHERE nombre = ?""", (peso, altura, nombre))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False
            
                                
    def eliminar_paciente(self, nombre):
        '''Elimina un registro de la tabla pacientes segun el nombre'''
        try:
            self.cur.execute("DELETE FROM pacientes WHERE nombre = ?", (nombre,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False
    
    
    
    
def test_db():
    # Rutina de prueba de un clase Database
    dB = Database()
    
    for item in dB.data_pacientes():
        print(item)
    else:
        print()
        
    print(dB.peso_altura_by_id(4))
    print()
    
    print(dB.data_paciente_by_name('Elsa Payo'))
    print()
        
    for name in dB.listar_pacientes_by_nombre():
        print(name)
        
    #print()
    #print(dB.agregar_paciente('Elvis Tek', 80, 1.78))
        
    del(dB)


if __name__ == "__main__":
    test_db()