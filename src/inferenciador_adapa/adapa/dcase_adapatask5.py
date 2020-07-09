from sys import path

#argumentos libreria
import argparse

path.append('../interfaz')

#interfaz
from inferenciador import Inferenciador

#Cargando librerias
import os 
import torch
import numpy as np
import torch.nn as nn
import torchvision.models
import librosa
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import requests

#modelo de adapa_task 5 (Obtenido de utils)

class Task5Model(nn.Module):

    def __init__(self, num_classes):

        super().__init__()

        self.bw2col = nn.Sequential(
            nn.BatchNorm2d(1),
            nn.Conv2d(1, 10, 1, padding=0), nn.ReLU(),
            nn.Conv2d(10, 3, 1, padding=0), nn.ReLU())

        self.mv2 = torchvision.models.mobilenet_v2(pretrained=True)

        self.final = nn.Sequential(
            nn.Linear(1280, 512), nn.ReLU(), nn.BatchNorm1d(512),
            nn.Linear(512, num_classes))

    def forward(self, x):
        x = self.bw2col(x)
        x = self.mv2.features(x)
        x = x.max(dim=-1)[0].max(dim=-1)[0]
        x = self.final(x)
        return x
##############################################

#clase dataset de 10-generate-submission-system-1

class AudioDataset(Dataset):
    def __init__(self, X):
        self.X = X

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        sample = self.X[idx, ...]
        i = np.random.randint(sample.shape[1])
        sample = torch.cat([
                sample[:, i:, :],
                sample[:, :i, :]],
                dim=1)
        return sample

################################################


#preparación de datos log -MEl Spectogram (Obtenido de 02-compute-log-mel)

def compute_melspec(filename):
    wav = librosa.load(filename, sr=44100)[0]
    melspec = librosa.feature.melspectrogram(
        wav,
        sr=44100,
        n_fft=128*20,
        hop_length=347*2,
        n_mels=128,
        fmin=20,
        fmax=44100 // 2)
    logmel = librosa.core.power_to_db(melspec)
    return logmel


##############################################################################

#CLASE PRINCIPAL

class Dcase_Adapatask5(Inferenciador):

    def __init__(self):
        self.device = None
        self.model = None

    
    #interfaz

    def inferirAudio(self,ruta):

        try:

            logmel = compute_melspec(ruta)


            X = np.expand_dims(logmel.T[:635, :], axis=0)

            X = X[:, None, :, :]

            channel_means = np.load('./data/channel_means.npy')
            channel_stds = np.load('./data/channel_stds.npy')
            X = (X - channel_means) / channel_stds

            dataset = AudioDataset(torch.Tensor(X))
            loader = DataLoader(dataset, 64, shuffle=False)

            all_preds = []
            for _ in range(10):
                preds = []
                for inputs in loader:
                        inputs = inputs.to(self.device)
                        with torch.set_grad_enabled(False):
                            self.model = self.model.eval()
                            outputs = self.model(inputs)
                            preds.append(outputs.detach().cpu().numpy())
                preds = np.concatenate(preds, axis=0)
                preds = (1 / (1 + np.exp(-preds)))
                all_preds.append(preds)
            tmp = all_preds[0]
            for x in all_preds[1:]:
                tmp += x
            tmp = tmp / 10
            preds = tmp

            output_df = pd.DataFrame(
                preds, columns=[
                    '1_engine', '2_machinery-impact', '3_non-machinery-impact',
                    '4_powered-saw', '5_alert-signal', '6_music', '7_human-voice', '8_dog',
                    '1-1_small-sounding-engine', '1-2_medium-sounding-engine',
                    '1-3_large-sounding-engine', '2-1_rock-drill', '2-2_jackhammer',
                    '2-3_hoe-ram', '2-4_pile-driver', '3-1_non-machinery-impact',
                    '4-1_chainsaw', '4-2_small-medium-rotating-saw',
                    '4-3_large-rotating-saw', '5-1_car-horn', '5-2_car-alarm', '5-3_siren',
                    '5-4_reverse-beeper', '6-1_stationary-music', '6-2_mobile-music',
                    '6-3_ice-cream-truck', '7-1_person-or-small-group-talking',
                    '7-2_person-or-small-group-shouting', '7-3_large-crowd',
                    '7-4_amplified-speech', '8-1_dog-barking-whining'])
            output_df['audio_filename'] = pd.Series('resultado', index=output_df.index)

            for x in [
                    '1-X_engine-of-uncertain-size', '2-X_other-unknown-impact-machinery',
                    '4-X_other-unknown-powered-saw', '5-X_other-unknown-alert-signal',
                    '6-X_music-from-uncertain-source', '7-X_other-unknown-human-voice']:
                output_df[x] = 0

            cols_in_order = [
                "audio_filename", "1-1_small-sounding-engine",
                "1-2_medium-sounding-engine", "1-3_large-sounding-engine",
                "1-X_engine-of-uncertain-size", "2-1_rock-drill",
                "2-2_jackhammer", "2-3_hoe-ram", "2-4_pile-driver",
                "2-X_other-unknown-impact-machinery", "3-1_non-machinery-impact",
                "4-1_chainsaw", "4-2_small-medium-rotating-saw",
                "4-3_large-rotating-saw", "4-X_other-unknown-powered-saw",
                "5-1_car-horn", "5-2_car-alarm", "5-3_siren", "5-4_reverse-beeper",
                "5-X_other-unknown-alert-signal", "6-1_stationary-music",
                "6-2_mobile-music", "6-3_ice-cream-truck",
                "6-X_music-from-uncertain-source", "7-1_person-or-small-group-talking",
                "7-2_person-or-small-group-shouting", "7-3_large-crowd",
                "7-4_amplified-speech", "7-X_other-unknown-human-voice",
                "8-1_dog-barking-whining", "1_engine", "2_machinery-impact",
                "3_non-machinery-impact", "4_powered-saw", "5_alert-signal",
                "6_music", "7_human-voice", "8_dog"]
            output_df = output_df.loc[:, cols_in_order]

            return output_df
        
        except Exception as e:
            print('Error en inferirAudio() '+str(e))
            return None


    def iniciarInferenciador(self,options):

        try:
            #Download Model

            if(not os.path.isfile('./data/model_system1')):
                print('Downloading model')
                r = requests.get('https://github.com/sainathadapa/dcase2019-task5-urban-sound-tagging/releases/download/1.0/model_system1')
                open('./data/model_system1', 'wb').write(r.content)


            cuda = options['cuda']
            self.device = torch.device('cuda:0' if cuda else 'cpu')
            print('Device: ', self.device)

            self.model = Task5Model(31).to(self.device)

            if cuda:
                self.model.load_state_dict(torch.load('./data/model_system1'))
            else:
                self.model.load_state_dict(torch.load('./data/model_system1',map_location='cpu'))
            
            return True

        except Exception as e:

            print('Error en iniciarInferenciador() '+str(e))

            return False

    #adapa

    def compute_melspec(self,filename):
        wav = librosa.load(filename, sr=44100)[0]
        melspec = librosa.feature.melspectrogram(
            wav,
            sr=44100,
            n_fft=128*20,
            hop_length=347*2,
            n_mels=128,
            fmin=20,
            fmax=44100 // 2)
        logmel = librosa.core.power_to_db(melspec)
        return logmel


################################################

def main():

    inferenciador = Dcase_Adapatask5()

    result = inferenciador.iniciarInferenciador({'cuda':True})

    if result:

        df = inferenciador.inferirAudio('/audios/05_001151.wav')

        print(df)

        df.to_csv('submission-system-1.csv', index=False)

if __name__ == "__main__":
    main()