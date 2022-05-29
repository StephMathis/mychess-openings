#! /usr/bin/env python3

import requests
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.sep.join([dir_path, '..'])

api_lichess_token = "lip_aGngjF1zO0LvHNKrGujX"
api_lichess_url = "https://lichess.org/api/games/user/metaheuristic"

nb=100
filepath = os.sep.join([project_dir, 'games', f'{nb}games.txt'])
#f'{dir_path}{os.sep}..{os.sep}games{os.sep}{nb}games.txt'
headers = {
    'Authorization' : f'Bearer {api_lichess_token}'
}
params = { "max":nb, 'perfType':'blitz'}
r = requests.get(api_lichess_url, params=params)

file = open(filepath,'wt')
file.write(r.text)
file.close()
