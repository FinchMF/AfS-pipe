
import wave
import soundfile
import librosa
from scipy.io.wavfile import read, write
from typing import List, Any, TypeVar
WAV = TypeVar('wave.Wave_read')



def intervals(bins: int, duration_frames: float) -> List[tuple]:

    bin_duration = int(duration_frames / bins)

    return [(i * bin_duration, (i + 1) * bin_duration) for i in range(int(bins))]


def divide_tracks(wav_fp: str, duration_seconds: float, verbose: bool = False) -> List[Any]:

    try:
        wav = wave.open(wav_fp, 'rb')
    except:
        y, sr = librosa.load(wav_fp)
        soundfile.write(wav_fp, y, sr)
        wav = wave.open(wav_fp, 'rb')

    frames = wav.getnframes()
    rate = wav.getframerate()

    duration = round(frames / rate, 2)

    needed_bin = duration / duration_seconds

    if verbose:
        print(f"Factor: {duration / needed_bin}")

    divider = intervals(bins=needed_bin, duration_frames=float(frames))

    return [list(divider), wav, wav_fp]


def sample_divisions(divisions: List[Any], wav: WAV, wav_fp: str, filenum: int, root: str, g_number: int) -> None:

    sci_wav = read(wav_fp)
    count = 0

    for div in divisions:

        fname = f"{root}/wav_{g_number}_{filenum}_{count}.wav"

        write(fname, wav.getframerate(), sci_wav[1][div[0]:div[1]])

        count += 1


def spilt_wav_by_seconds(wav_list: List[str], seconds: int, root: str, g_number: int) -> None:


    for idx, wav in enumerate(wav_list):

        data = divide_tracks(wav, seconds)

        sample_divisions(divisions=data[0],
                        wav=data[1],
                        wav_fp=data[2],
                        filenum=idx, 
                        root=root,
                        g_number=g_number)

    




     