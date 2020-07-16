from flask import json
import os
import requests

def test_inferencia(app, client):

    if(not os.path.isfile(os.environ['DATA_PATH']+os.environ['TEST_AUDIO_NAME'])):
        print('Downloading Test Audio')
        r = requests.get(os.environ['TEST_AUDIO_URL'])
        open(os.environ['DATA_PATH']+os.environ['TEST_AUDIO_NAME'], 'wb').write(r.content)

    res = client.post('/api/inferencia',json={"audio_nombre":os.environ['TEST_AUDIO_NAME']})

    assert res.status_code == 200


    data = json.loads(res.get_data(as_text=True))

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
    


    assert [*data] == cols_in_order
    

