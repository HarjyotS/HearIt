import os
import random
import soundfile as sf
import numpy as np

def splice_audio(audio_folder, output_file, data_list):
    audio_segments = []
    sample_rate = 44100  # Default sample rate
    counter = 0
    for file_name in os.listdir(audio_folder):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(audio_folder, str(counter) + ".mp3")
            audio, sr = sf.read(file_path)
            audio_segments.append(audio * (4.5 if data_list["podcast"]["transcript"][counter]["speaker_id"] == "HOST" else 0.8))  # Multiply volume by 4 for every other audio file
            sample_rate = sr  # Assign the sample rate
        counter += 1

    final_audio = np.array([])
    for audio in audio_segments:
        pause_duration = random.choice([0.5, 1]) * sample_rate
        pause = np.zeros(int(pause_duration))
        final_audio = np.concatenate((final_audio, audio, pause))

    sf.write(output_file, final_audio, sample_rate)

# Example usage
# splice_audio("audio_files", "final_audio_with_pauses.wav", data_list)