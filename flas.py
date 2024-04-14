from flask import Flask, send_from_directory, render_template, request
import os
import requests
from backend_funcs.read_pdf import read_pdf_plain, read_pdf
from backend_funcs.generate_script import generate_script
from backend_funcs.generate_audio import generate_audio
from backend_funcs.splice_audio import splice_audio
from backend_funcs.generate_audio_answer import generate_audio_answer
import threading
import json
import time

global status

status = {
    "status": "Idle",
    "updates": [],
}
app = Flask(__name__, static_folder='frontend')

@app.route('/restartstat')
def restat():
    global status
    status = {
        "status": "Idle",
        "updates": [],
    }
    return 'done'

@app.route('/question/<question>')
def resta(question):
    answer = generate_audio_answer("./uploads/tmp.pdf", question)
    return "done"

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

@app.route('/releaseq')
def servq():
    # Serve any file from the frontend folder
    return send_from_directory("./","answer.mp3")

@app.route('/status')
def statusz():
    global status
    return json.dumps(status)

@app.route('/submit', methods=['POST'])
def submit():
    global status
    if request.method == 'POST':
        print(request.files)
        f = request.files['file']
        f.save('uploads/' + "tmp.pdf")
        download_thread = threading.Thread(target=submit_pdf, name="Downloader")
        download_thread.start()
        status["status"] = "Processing"
        return 'File uploaded successfully!'

def submit_pdf():
    global status
    # get only file in uploads folder
    print("processingpdf")
    tmp_location = os.path.join('uploads', os.listdir('uploads')[0])
    status["updates"].append({"message": "Reading PDF", "time": time.time()})
    contents_plain = read_pdf_plain(tmp_location)
    print("read PDF")
    # contents = read_pdf(tmp_location)
    status["updates"].append({"message": "Generating Script", "time": time.time()})
    data_list = generate_script(contents_plain)
    print(data_list)
    status["updates"].append({"message": "Generating Audio", "time": time.time()})

    generate_audio(data_list["podcast"]["transcript"])
    status["updates"].append({"message": "Stitching Files", "time": time.time()})

    splice_audio("audio_files", "final_audio_with_pauses.wav", data_list)
    
    status["updates"].append({"message": "Cleaning...", "time": time.time()})

    for file_name in os.listdir("audio_files"):
        if file_name.endswith(".mp3"):
            os.remove(os.path.join("audio_files", file_name))
    status = {
        "status": "Complete",
        "updates": [],
    }
    return 'PDF processed successfully!'




if __name__ == '__main__':
    app.run(port=8080)
