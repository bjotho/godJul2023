from pathlib import Path

import librosa
import matplotlib.pyplot as plt
import numpy as np

from utils.utils import handle_file


def show_spectrogram(soundfile: str) -> None:
    """Display a spectrogram of the soundfile using a matplotlib plot

    :param soundfile: String containing a soundfile name or path to a sound file.
    """
    soundfile = handle_file(file=soundfile, python_module=Path(__file__))
    if soundfile is None:
        return

    data, samplerate = librosa.load(soundfile)

    data_stft = librosa.stft(data)
    s_db = librosa.amplitude_to_db(np.abs(data_stft), ref=np.max)

    fig, ax = plt.subplots()
    img = librosa.display.specshow(s_db, x_axis="time", y_axis="linear", ax=ax)
    ax.set(title="Spectrogram")
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    plt.show()
