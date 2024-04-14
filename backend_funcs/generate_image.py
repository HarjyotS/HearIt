from openai import OpenAI

with open("api_key.txt", "r") as f:
    keys = f.read().split(",")
    elevenlabs_api_key = keys[0]
    openai_api_key = keys[1][:-1]

client = OpenAI(api_key=openai_api_key)

def generate_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url


import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def show_image(url):
    img = mpimg.imread(url)
    imgplot = plt.imshow(img)
    plt.show()

# Example usage
show_image(generate_image("A surrealistic painting of a cat with a fish tail."))
