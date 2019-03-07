import os
from flask import Flask, render_template, request, send_from_directory, url_for
import shutil

from face import classify

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # to correct open from outside

dir_uploads = 'static/uploads'
UPLOAD_FOLDER = os.path.join(dir_path, dir_uploads)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

shutil.rmtree(UPLOAD_FOLDER)


@app.route('/')
def index():
    #todo
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_test():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    if file:
            file.save(f)
            filename = url_for('static', filename='uploads/' + os.path.basename(f))
            k = 20
            try:
                ids, conf = classify(filename, k)
            except RuntimeError as e:
                return e.args[0]
            return render_template('index.html', image_files=filename, ids=ids, confidence=conf)

    return render_template('index.html')


@app.route('/clear', methods=['POST'])
def clear():
    #todo
    return render_template('index.html')


@app.route('/static/uploads/<filename>')
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    local = '127.0.0.1'  # to run on local machine
    internet = '0.0.0.0'  # to run on server and to be accessed outside

    app.run(host=local, port=8081, debug=False)
