import os
from flask import Flask, render_template, request, send_from_directory, url_for
from os import path
import glob
import shutil

from reidentifier import Reidentifier

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # to correct open from outside

dir_uploads = 'static/uploads'
UPLOAD_FOLDER = os.path.join(dir_path, dir_uploads)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class_names = ['1', '2']

shutil.rmtree(UPLOAD_FOLDER)
for class_name in class_names:
    os.makedirs(path.join(UPLOAD_FOLDER, class_name))


filenames = {'1': [], '2': []}  # [string, list[string]]

reidentifier = Reidentifier()


@app.route('/')
def index():
    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/upload_train', methods=['POST'])
def upload_train():
    class_n = request.form['class']
    file = request.files['image']
    if file:
        f = os.path.join(app.config['UPLOAD_FOLDER'], class_n, file.filename)
        file.save(f)
        filename = url_for('static', filename='uploads/' + class_n + '/' + os.path.basename(f))
        filenames[class_n].append(filename)

    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/upload_test', methods=['POST'])
def upload_test():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    if file:
        if len(filenames[class_names[0]]) > 0 and len(filenames[class_names[1]]) > 0:
            file.save(f)
            filename = url_for('static', filename='uploads/' + os.path.basename(f))

            class_name_test, score = reidentifier.reindetify(testImagePath=f, train_image_dir=UPLOAD_FOLDER)
            return render_template('index.html', image_files=filenames, class_names=class_names,
                                   test_image=filename, class_test=class_name_test, confidence=score)

    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/clear', methods=['POST'])
def clear():
    class_n = request.form['class']
    filenames[class_n] = []

    files = glob.glob(path.join(UPLOAD_FOLDER, class_n, '*'))
    for f in files:
        os.remove(f)

    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/static/uploads/<filename>')
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
