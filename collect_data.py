
import sys
import os
import datetime
from typing import List
import pandas as pd
from tools.sp_utils import Spoti


def collect_from_spotify(genres: List[str], data_fname: str) -> None:

    dfs = []
    for genre in genres:
        try:
            print(f"\n{genre}")
            df = Spoti().search(genre=genre)
            df['genre'] = genre
            print(f"\n{len(df)}")
            dfs.append(df)
            print('\nappended')
        except:
            print('\nRefresh-Token')
            print(genre)
            df = Spoti().search(genre=genre)
            df['genre'] = genre
            print(f"\n{len(df)}")
            dfs.append(df)
            print('\nappened')
            continue

    df = pd.concat(dfs, ignore_index=True)
    print(f"Total tracks: {len(df)}")
    df.to_csv(data_fname)



def fetch_wav(fname: str, location: str) -> None:

    data = pd.read_csv(fname)
    ix = 0
    collected = 0
    no_preview = 0
    for idx in range(0, len(data)):
        ix += 1
        z = (f'Progress: {round((ix/len(data))*100,2)} %  Complete | Collected: {collected} | No preview avail: {no_preview}')
        try:
            if not os.path.exists(f"{location}/{data.iloc[idx]['genre']}/"):
                os.mkdir(f"{location}/{data.iloc[idx]['genre']}")

            Spoti.collect_wav(endpoint=data.iloc[idx]['preview_url'],
                                out=f"{location}/{data.iloc[idx]['genre']}/{data.iloc[idx]['genre']}_{data.iloc[idx]['artist_name']}_{data.iloc[idx]['title']}.wav")

            collected += 1
            sys.stdout.write('\r'+z)
        except:
            no_preview += 1
            sys.stdout.write('\r'+z)
            continue


if __name__ == '__main__':

    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(f"File Date: {date}")
    genres = [
        "shoegaze", 
        "indie",
        "deep house", 
        "blues", 
        "psychrock", 
        "dreampop",
        "doom metal",
        "classical",
        "lofi beats"
        ]
    print(f"Seeking Genres: {genres}")
    outload_location = '<diectory for resulting wav files>' 
    data_fname = f'{outload_location}/{date}_meta.csv'
    

    collect_from_spotify(genres=genres, data_fname=data_fname)
    fetch_wav(fname=data_fname, location=outload_location)
