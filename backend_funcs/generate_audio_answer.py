from read_pdf import read_pdf
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from openai import OpenAI

with open("api_key.txt", "r") as f:
    keys = f.read().split(",")
    elevenlabs_api_key = keys[0]
    openai_api_key = keys[1][:-1]

client = OpenAI(api_key=openai_api_key)
audio_client = ElevenLabs(api_key=elevenlabs_api_key)

speaker_ids = {
    "HOST": "5PIw5p7U2UKtFRaB15Sg",
    "GUEST": "G17SuINrv2H9FC6nvetn"
}

def find_context(file_path, query):
    pages = read_pdf(file_path)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(pages)
    db = Chroma.from_documents(documents, OpenAIEmbeddings(api_key=openai_api_key))
    docs = db.similarity_search(query)
    return docs[0].page_content

def generate_answer(file_path, query):
    context = find_context(file_path, query)
    response = client.chat.completions.create(
        model="gpt-4-turbo",
    messages=[
        {
        "role": "system",
        "content": "You will receive a question and some context that will possibly answer the question. Write an answer to the question, as succint as possible, coming across as cheerful and happy to help but not going too over the top. Use the context as much as possible."
        },
        {
        "role": "user",
        "content": "Query: " + query + "\nContext: " + context
        },

    ],
    temperature=1,
        max_tokens=2068,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )    

    return response.choices[0].message.content

def generate_audio_answer(file_path, query):
    answer = generate_answer(file_path, query)
    v = speaker_ids["HOST"]
    audio = audio_client.generate(text=answer, voice=v)

    # Save the audio to a file named after the speaker ID
    filename = "answer.mp3"
    save(audio, f"./{filename}")
    print(f"Audio saved for HOST in {filename}")
    return answer

# Example Usage
# generate_audio_answer("backend_funcs/test.pdf", "How is the recovery usually done?")
