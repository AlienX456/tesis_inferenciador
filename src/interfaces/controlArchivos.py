from abc import ABC, abstractmethod



#INTERFAZ DEL CONTROL DE ARCHIVOS

class ControlArchivos(ABC):

    @abstractmethod
    def borrarArchivo(self,ruta):
        pass

    @abstractmethod
    def buscarRutasAudios(self,raiz):
        pass