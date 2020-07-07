from interfaces.controlArchivos import ControlArchivos

from os import remove, listdir
from os.path import isfile, join



class ControlArchivosLinux(ControlArchivos):
    
    def borrarArchivo(self,abs_ruta):
        try:
            remove(abs_ruta)
            return True
        except FileNotFoundError:
            print("El archivo no fue encontrado")
            return False



    def buscarRutasAudios(self,abs_raiz):
        try:
            lista = [f for f in listdir(abs_raiz) if f.endswith(".wav")]
            return lista
        except FileNotFoundError:
            print("No se encuentra la ruta")
            return True
