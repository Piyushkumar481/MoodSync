import librosa
import numpy as np

def extract_audio_features(audio_file_path):
    """
    Extracts audio features using Librosa.
    """
    y, sr = librosa.load(audio_file_path, sr=None)

    # Extract features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
    energy = np.mean(librosa.feature.rms(y=y))
    danceability = np.mean(librosa.feature.tempogram(y=y, sr=sr))

    return {
        "tempo": tempo,
        "chroma": chroma.tolist(),
        "energy": energy,
        "danceability": danceability,
    }
