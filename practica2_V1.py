from time import sleep
from multiprocessing import Value, Lock, Condition, Process
from enum import Enum
import numpy as np
import random

class ClaseUsuario(Enum):
    VehiculoNorte = "Vehículo procedente del norte"
    VehiculoSur = "Vehículo procedente del sur"
    Peaton = "Peatón"

    #Devuelve un iterable que 'contiene' las clases distintas a la del elemento que ejecuta la función.
    def otrasClases(self):
        if self == ClaseUsuario.VehiculoNorte:
            it = iter((ClaseUsuario.VehiculoSur, ClaseUsuario.Peaton))
        elif self == ClaseUsuario.VehiculoSur:
            it = iter((ClaseUsuario.Peaton, ClaseUsuario.VehiculoNorte))
        else:
            it = iter((ClaseUsuario.VehiculoNorte, ClaseUsuario.VehiculoSur))
        return it

    #Parámetros que se usan para simular cuando tarda cada clase en atravesar el puente siguiendo una distribución normal
    def tiempoCruce(self):
        if self == ClaseUsuario.VehiculoNorte:
            t= {'media': 1,'varianza': 0.5} # normal 1s, 0.5s
        elif self == ClaseUsuario.VehiculoSur:
            t= {'media': 1,'varianza': 0.5} # normal 1s, 0.5s
        else:
            t = {'media':30, 'varianza': 10} # normal 1s, 0.5s
        return t

    #Devuelve un parámetro que se usa para simular cuanto tarda un nuevo usuario de cada clase en llegar al puente.
    def tiempoLLegada(self):
        if self == ClaseUsuario.VehiculoNorte:
            t = 0.5
        elif self == ClaseUsuario.VehiculoSur:
            t = 0.5
        else:
            t = 5 
        return t

    # Devuelve la cantidad de usuarios de cada clase que se pretenden crear
    def cantidad(self):
        if self == ClaseUsuario.VehiculoNorte:
            c = 100
        elif self == ClaseUsuario.VehiculoSur:
            c = 100 
        else:
            c = 10
        return c
    
class Monitor():
    def __init__(self):
        self.lock = Lock()
        #Diccionario que asigna a cada clase una variable condición, donde se bloquean los usuarios de cada clase.
        self.cond = {clase: Condition(self.lock) for clase in ClaseUsuario}
        #Diccionario que asigna a cada clase una variable compartida con el número de dicha clase que hay atravesando el puente. 
        self.puente  = {clase: Value('i',0)      for clase in ClaseUsuario}

    # Función que hace que un usuario quede bloqueado en la variable condición correspondiente hasta que se den las condiciones adecuadas para que los usuarios puedan entrar.
    def esperandoCruzar(self, clase):
        with self.lock: #Pide el lock y lo libera al final, asegura que no se pueda acceder a los valores y los metodos a la vez
            self.cond[clase].wait_for(lambda: all(self.puente[otra].value == 0 for otra in clase.otrasClases())) #Espera a que no haya ususarios de otras clases en el puente para pasar
            self.puente[clase].value += 1 #Añade 1 al número de este tipo en el túnel
    
    def salirPuente(self, clase): 
        with self.lock:
            self.puente[clase].value -= 1 #Resta 1 al número de este tipo en el túnel
            for otra in clase.otrasClases(): #Notifica al resto de tipos
                self.cond[otra].notify_all()

#Proceso para esperar a poder entrar en el túnel y pasar. El parámetro flush sirve para que el print se muestre por pantalla en el momento en el que se genera.
def CruzarPuente(clase, pid :int, monitor, tiempoCruce: int):
    print(f"{clase.name} {pid} esperando", flush = True) 
    monitor.esperandoCruzar(clase)
    print(f"Entrando {clase.name} {pid}", flush = True)
    sleep(tiempoCruce)
    print(f"Saliendo {clase.name} {pid}", flush = True)
    monitor.salirPuente(clase)

#Genera los procesos que simulan los usuarios de una determinada clase
def generaClase(clase: ClaseUsuario, monitor: Monitor):    
    plst = [] #Lista de procesos
    #Modelizamos el tiempo que tarda un usuario de la clase en cruzar el tunel mediante una distribución normal.
    muestra = iter(np.random.normal(clase.tiempoCruce()['media'], clase.tiempoCruce()['varianza'], clase.cantidad() )) 
    plst = [Process(target=CruzarPuente, args=(clase, i, monitor, abs(next(muestra))))
                for i in range(clase.cantidad())] 
    
    for p in plst:
        p.start()
        #Usamos una variable aleatorria con distribución exponencial que usa como parametro el tiempoLLegada() 
        sleep(random.expovariate(1/clase.tiempoLLegada()))

    for p in plst:
        p.join()

#Genera procesos de cada clase de usuarios.  
def main():
    monitor = Monitor()
    simulacion = [Process(target=generaClase, args=(clase, monitor)) for clase in ClaseUsuario]

    for p in simulacion:
        p.start()

    for p in simulacion:
        p.join()
                                      
if __name__ == "__main__":
    main()