import threading
from elevenlabs import save
from elevenlabs.client import ElevenLabs

with open("api_key.txt", "r") as f:
    keys = f.read().split(",")
    elevenlabs_api_key = keys[0]
    openai_api_key = keys[1][:-1]

max_threads = 4
semaphore = threading.Semaphore(max_threads)

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=elevenlabs_api_key)

speaker_ids = {
    "HOST": "5PIw5p7U2UKtFRaB15Sg",
    "GUEST": "G17SuINrv2H9FC6nvetn"
}

def generate_audio(data_list):
    # Create a list of threads to generate audio for each item in the list
    threads = []
    for index, item in enumerate(data_list):
        # Create a thread for each item
        thread = threading.Thread(target=generate_files, args=(item, index))
        threads.append(thread)
        thread.start()
    
    # Join all threads to wait for their completion
    for thread in threads:
        thread.join()
    

def generate_files(item, index):
    # Acquire the semaphore to limit concurrent threads
    with semaphore:
        print(f"Generating audio for {item['speaker_id']}...")
        v = speaker_ids[item['speaker_id']]
        audio = client.generate(text=item['text'], voice=v)
        
        # Save the audio to a file named after the speaker ID
        filename = f"{index}.mp3"
        save(audio, f"./audio_files/{filename}")
        print(f"Audio saved for {item['speaker_id']} in {filename}")


generate_audio(data_list)