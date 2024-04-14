import os
import random
import soundfile as sf
import numpy as np

def splice_audio(audio_folder, output_file):
    audio_segments = []
    sample_rate = 44100  # Default sample rate
    for file_name in os.listdir(audio_folder):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(audio_folder, file_name)
            audio, sr = sf.read(file_path)
            audio_segments.append(audio)
            sample_rate = sr  # Assign the sample rate

    final_audio = np.array([])
    for audio in audio_segments:
        pause_duration = random.choice([2, 3]) * sample_rate
        pause = np.zeros(pause_duration)
        final_audio = np.concatenate((final_audio, audio, pause))

    # Increase volume of the final audio
    final_audio = final_audio * 4

    sf.write(output_file, final_audio, sample_rate)

# Example usage
splice_audio("audio_files", "final_audio_with_pauses.wav")
