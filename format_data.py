
import os
import glob
from tools import wav_utils

import warnings
warnings.filterwarnings("ignore", message='PySoundFile failed. Trying audioread instead.')
 


def split_wavs(root: str, seconds: int) -> None:

    """
    recieves directory of genre datasets and the seconds of equal divisons for each wav
    """

    genre_dirs = glob.glob(f"{root}/*")

    g_number = 0
    for genre in genre_dirs:

        if genre[-3:] == 'csv' or genre[-3:] == 'wav':

            continue
        else:

            print(f'Getting {genre} formatted wavs')
            formatted = f"{genre}/formatted"
            wavs = glob.glob(f"{genre}/*")

            if not os.path.exists(formatted):

                os.mkdir(formatted)

            wav_utils.spilt_wav_by_seconds(wav_list=wavs, 
                                        seconds=seconds, 
                                        root=formatted, 
                                        g_number=g_number)

            g_number += 1

        

        

if __name__ == '__main__':

    root = '<dataset directory>'

    split_wavs(root=root, seconds=10)


