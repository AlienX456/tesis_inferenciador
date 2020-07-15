from abc import ABC, abstractmethod



#INTERFAZ DEL CONTROL DE ARCHIVOS

class Inferenciador(ABC):

    @abstractmethod
    def inferirAudio(self,ruta):
        pass