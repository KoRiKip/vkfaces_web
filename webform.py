import os
from flask import Flask, render_template, request, send_from_directory, url_for

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(dir_path, 'static/uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class_names = ['1', '2']
filenames = {'1': [], '2': []}  # [string, list[string]]


@app.route('/')
def hello_world():
    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/upload_train', methods=['POST'])
def upload_train():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    filename = url_for('static', filename='uploads/' + os.path.basename(f))
    class_n = request.form['class']
    filenames[class_n].append(filename)

    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/upload_test', methods=['POST'])
def upload_test():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    filename = url_for('static', filename='uploads/' + os.path.basename(f))

    return render_template('index.html', image_files=filenames, class_names=class_names,
                           test_image=filename, class_test='1', confidence=0.99)


@app.route('/clear', methods=['POST'])
def clear():
    class_n = request.form['class']
    filenames[class_n].clear()

    return render_template('index.html', image_files=filenames, class_names=class_names)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run()
