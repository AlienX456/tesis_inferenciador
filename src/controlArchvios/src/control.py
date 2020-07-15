import os
import asyncio
import requests


from controlArchivosLinux import ControlArchivosLinux

class Control:

    def __init__(self):
        self.controlArchivosLinux = ControlArchivosLinux()

        #INFERENCIADOR
        self.inferenciador_url = os.environ['API_URL']
        self.inferenciador_url_inicio = os.environ['API_URL_INICIO']
        self.inferenciador_url_inderenciador = os.environ['API_URL_INFERENCIADOR']

        #TIEMPO DE ESPERA
        self.espera = int(os.environ['ESPERA'])

        #RUTA
        self.audio_container_path = os.environ['AUDIO_PATH']



    async def iniciar(self):

        try:

            print('Iniciando Inferenciador')

            inicioInf = requests.get(self.inferenciador_url + self.inferenciador_url_inicio)

            print("Iniciando inferencias")

            while True:

                lista = [audio for audio in self.controlArchivosLinux.buscarRutasAudios(self.audio_container_path)]

                if len(lista) == 0:

                    print("Lista vacia, función en espera {}...".format(self.espera))

                    await asyncio.sleep(self.espera)

                
                for audio in lista:

                    json = self.inferirAudio(audio)

                    print('Removing'+self.audio_container_path+'/'+audio)

                    self.controlArchivosLinux.borrarArchivo(self.audio_container_path+'/'+audio)

        
        except Exception as e:

            print(e)
                


        
    def inferirAudio(self,audio_nombre):

        print("Realizando inferencia sobre audio : "+audio_nombre)

        try:

            r = requests.post(self.inferenciador_url + self.inferenciador_url_inderenciador, json={"audio_nombre":audio_nombre})

            print("Inferencia completada para audio :"+audio_nombre)

            return r.json()
        
        except Exception as e:

            print(e)
            
            raise

            
    


async def main():
    
    control = Control()

    await control.iniciar()



asyncio.run(main())

