from openai import OpenAI
import json

with open("api_key.txt", "r") as f:
    keys = f.read().split(",")
    elevenlabs_api_key = keys[0]
    openai_api_key = keys[1][:-1]

print(repr(openai_api_key))

client = OpenAI(api_key=openai_api_key)

def generate_script(content):
  response = client.chat.completions.create(
    model="gpt-4-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will receive a document with information. Your Job is to create a script with a host and a guest speaker about the topic, do not talk about everything but discuss important sections or subtopics. If the topic is complex or hard to understand, you may simplify it a little bit.\n\nThe host is a female and the guest will be male."
    },
    {
      "role": "user",
      "content": content
    },

  ],
   temperature=1,
    max_tokens=2068,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  response2 = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {
      "role": "system",
      "content": "Podcast JSON Transformation Prompt\n\nPlease transform the following podcast transcription into a JSON format according to the structure outlined below:\n\nText: Transcribe the podcast content into text format, including dialogue and narrative. Ensure the transcription is accurate and maintains the context and flow of the podcast.\nSpeaker IDs: Attribute each portion of text to the correct speaker using speaker HOST and GUEST labels.\nFormat the JSON output as follows:\n\n{\n  \"podcast\": {\n    \"title\": \"Podcast Title\",\n    \"transcript\": [\n      {\n        \"speaker_id\": \"Speaker1\",\n        \"text\": \"Transcribed text for Speaker1\"\n      },\n      {\n        \"speaker_id\": \"Speaker2\",\n        \"text\": \"Transcribed text for Speaker2\"\n      },\n      ...\n    ]\n  }\n}\nTitle: Include the title of the podcast.\nTranscript: The podcast's transcript should be structured as an array of objects, where each object includes a unique speaker ID and the transcribed text for that speaker.\n\n Ensure all quotation marks are doublequoted"
    },
    {
      "role": "user",
      "content": response.choices[0].message.content
    }
  ],
  temperature=1,
  max_tokens=4095,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )
  # print(response2.choices[0].message.content)
  c = json.loads(str(response2.choices[0].message.content))
  # print(c)
  # print("--------------------\n\n\n-------------------")
  # print(c["podcast"]["transcript"])
  for i in range(len(c["podcast"]["transcript"])):
     print(c["podcast"]["transcript"][i]["speaker_id"], c["podcast"]["transcript"][i]["text"])
  return c
