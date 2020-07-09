import os
import shutil
from sys import path


path.append('src')
path.append('interfaz')

from controlArchivosLinux import ControlArchivosLinux



#TEST CONTROL DE ARCHIVOS LINUX


def test_controlArchivos_borrarArchivo():

    os.mkdir(os.path.abspath("test/cache"))

    for f in os.listdir(os.path.abspath("test/cache")):
        os.remove(os.path.abspath("test/cache")+"/"+f)


    CAL = ControlArchivosLinux()

    archivo = open("test/cache/test.test", "a")

    archivo.close()

    resultado = CAL.borrarArchivo(os.path.abspath("test/cache/test.test"))
    
    shutil.rmtree(os.path.abspath("test/cache"))

    assert resultado == True


def test_controlArchivos_buscarRutasAudios():

    os.mkdir(os.path.abspath("test/cache"))

    CAL = ControlArchivosLinux()

    audio_fake_1 = open("test/cache/test1.wav", "a")

    audio_fake_1.close()

    audio_fake_2 = open("test/cache/test2.wav", "a")

    audio_fake_2.close()

    other = open("test/cache/test.wa", "a")

    other.close()

    resultado = CAL.buscarRutasAudios(os.path.abspath("test/cache"))

    shutil.rmtree(os.path.abspath("test/cache"))

    assert len(resultado) == 2
