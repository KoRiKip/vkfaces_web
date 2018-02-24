import os
from flask import Flask, render_template, request, send_from_directory, url_for
from os import path
import glob
from reidentifier import Reidentifier

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_uploads = 'static/uploads'
UPLOAD_FOLDER = os.path.join(dir_path, dir_uploads)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class_names = ['1', '2']

for the_file in os.listdir(UPLOAD_FOLDER):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print(e)

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
    f = os.path.join(app.config['UPLOAD_FOLDER'], class_n, file.filename)
    file.save(f)
    filename = url_for('static', filename='uploads/' + class_n + '/' + os.path.basename(f))
    filenames[class_n].append(filename)

    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/upload_test', methods=['POST'])
def upload_test():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    filename = url_for('static', filename='uploads/' + os.path.basename(f))

    class_name_test = reidentifier.reindetify(testImagePath=f, train_image_dir=UPLOAD_FOLDER)

    return render_template('index.html', image_files=filenames, class_names=class_names,
                           test_image=filename, class_test=class_name_test, confidence=0.99)


@app.route('/clear', methods=['POST'])
def clear():
    class_n = request.form['class']
    filenames[class_n].clear()

    files = glob.glob(path.join(UPLOAD_FOLDER, class_n))
    for f in files:
        os.remove(f)
        
    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run()
