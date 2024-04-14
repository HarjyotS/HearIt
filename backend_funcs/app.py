import streamlit as st
from generate_audio import generate_audio
from read_pdf import *
import os
from generate_script import generate_script
from splice_audio import splice_audio
from generate_audio_answer import generate_audio_answer

def app():
    st.title("HearIt")
    st.subheader("Your Engaging Gateway to the Internet")
    uploaded_file = st.file_uploader("Upload a PDF file to read", type=["pdf"])
    if uploaded_file is not None:
        st.write("Reading PDF...")
        # Save pdf to temp location
        tmp_location = "tmp.pdf"
        with open(tmp_location, "wb") as f:
            f.write(uploaded_file.getbuffer())
        contents_plain = read_pdf_plain(tmp_location)
        contents = read_pdf(tmp_location)
        st.write("Generating script...")
        data_list = generate_script(contents_plain)
        print(data_list)
        st.write("Generating audio...")
        generate_audio(data_list["podcast"]["transcript"])
        st.write("Splicing audio...")
        splice_audio("audio_files", "final_audio_with_pauses.wav", data_list)
        st.write("Your podcast is ready!")
        st.audio("final_audio_with_pauses.wav")
        for file_name in os.listdir("audio_files"):
            if file_name.endswith(".mp3"):
                os.remove(os.path.join("audio_files", file_name))
        # Take questions
    question = st.text_input("Any questions about the text?")
    if question:
        st.write("Generating answer...")
        answer = generate_audio_answer("tmp.pdf", question)
        st.write("Answer:", answer)
        st.audio("answer.mp3")
    
app()