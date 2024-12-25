import numpy as np
import librosa
import cv2

def solution(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    mean_frequency = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    # Define a threshold to classify sound as "metal" or "cardboard"
    # I defined frequency value as threshold bcz it had significant difference in metal and cardboard. 
    # metal frequency is less than cardboard by almost 2000 Hz
    threshold = 3796
    if mean_frequency <= threshold:
      return "metal"
    else:
      return "cardboard"