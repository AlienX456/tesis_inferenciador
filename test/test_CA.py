import os

from sys import path


path.append('src')

from controlArchivosLinux import ControlArchivosLinux



#TEST CONTROL DE ARCHIVOS LINUX


def test_controlArchivos_borrarArchivo():

    for f in os.listdir(os.path.abspath("test/basura")):
        os.remove(os.path.abspath("test/basura")+"/"+f)


    CAL = ControlArchivosLinux()

    archivo = open("test/basura/test.test", "a")

    archivo.close()

    resultado = CAL.borrarArchivo(os.path.abspath("test/basura/test.test"))

    for f in os.listdir(os.path.abspath("test/basura")):
        os.remove(os.path.abspath("test/basura")+"/"+f)

    assert resultado == True


def test_controlArchivos_buscarRutasAudios():

    for f in os.listdir(os.path.abspath("test/basura")):
        os.remove(os.path.abspath("test/basura")+"/"+f)

    CAL = ControlArchivosLinux()

    audio_fake_1 = open("test/basura/test1.wav", "a")

    audio_fake_1.close()

    audio_fake_2 = open("test/basura/test2.wav", "a")

    audio_fake_2.close()

    other = open("test/basura/test.wa", "a")

    other.close()

    resultado = CAL.buscarRutasAudios(os.path.abspath("test/basura"))

    for f in os.listdir(os.path.abspath("test/basura")):
        os.remove(os.path.abspath("test/basura")+"/"+f)

    assert len(resultado) == 2
