from flask import Flask, send_from_directory, render_template, request
import os
import requests
from backend_funcs.read_pdf import read_pdf_plain, read_pdf
from backend_funcs.generate_script import generate_script
from backend_funcs.generate_audio import generate_audio
from backend_funcs.splice_audio import splice_audio
import threading
global status


app = Flask(__name__, static_folder='frontend')

@app.route('/')
def index():
    # Serve the index.html file from the frontend folder
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_file_in_path(path):
    # Serve any file from the frontend folder
    return send_from_directory('frontend', path)

@app.route('/release')
def serv():
    # Serve any file from the frontend folder
    return send_from_directory("./","final_audio_with_pauses.wav")

@app.route('/status')
def status():
    return status

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        print(request.files)
        f = request.files['file']
        f.save('uploads/' + f.filename)
        download_thread = threading.Thread(target=submit_pdf, name="Downloader")
        download_thread.start()
        status = "Processing"
        return 'File uploaded successfully!'

def submit_pdf():

    # get only file in uploads folder
    print("processingpdf")
    tmp_location = os.path.join('uploads', os.listdir('uploads')[0])
    contents_plain = read_pdf_plain(tmp_location)
    print("read PDF")
    # contents = read_pdf(tmp_location)
    data_list = generate_script(contents_plain)
    print(data_list)
    generate_audio(data_list["podcast"]["transcript"])
    splice_audio("audio_files", "final_audio_with_pauses.wav", data_list)
    for file_name in os.listdir("audio_files"):
        if file_name.endswith(".mp3"):
            os.remove(os.path.join("audio_files", file_name))
    status = "Complete"
    return 'PDF processed successfully!'




if __name__ == '__main__':
    app.run(port=8080, debug=True)
