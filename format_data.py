
import os
import glob
from tools import wav_utils
 


def split_wavs(root: str, seconds: int) -> None:

    genre_dirs = glob.glob(root)
    g_number = 0
    for genre in genre_dirs:

        formatted = f"{root}/{genre}/formatted"
        wavs = glob.glob(f"{root}/{genre}")

        if not os.path.exists(formatted):

            os.mkdir(formatted)

        wav_utils.spilt_wav_by_seconds(wav_list=wavs, 
                                       seconds=seconds, 
                                       root=formatted, 
                                       g_number=g_number)

        g_number += 1

        

        

if __name__ == '__main__':

    root = '<directory for resulting wav files>'

    split_wavs(root=root, seconds=10)


