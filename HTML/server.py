# 要把原来的file_cache.py和他的app.py合并到一起，实现拖拽框
from flask import Flask, request, render_template, jsonify, send_file, redirect
import os
import PIL
from PIL import Image
import simplejson
import traceback
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 在这里进行用户名和密码的验证，验证通过则跳转到主界面
        return redirect('/main')
    return render_template('login.html')

@app.route('/main')
def main():
    return render_template('fronter.html')

@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

@app.route('/analyse', methods=['GET'])
def analyse():
    return render_template('analyse.html')

@app.route('/myupload', methods=['POST'])
def myupload():
    uploaded_file = request.files['file']
    if uploaded_file:
        file_name = uploaded_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        uploaded_file.save(file_path)
        # Call another function for further processing
        process_file(file_path)
        return jsonify({
            'message': 'File uploaded successfully.',
            'file_name': file_name
        })
    else:
        return 'No file was uploaded.'

@app.route('/pdf', methods=['POST'])
def serve_pdf():
    filename = request.form['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, mimetype='application/pdf')

@app.route('/get_image', methods=['POST'])
def get_image():
    image_filename = request.form.get('filename')
    if image_filename:
        image_dot_path = os.path.join('./upload', image_filename)
        image_png_path = os.path.join('./upload', 'graph.png')

        if os.path.exists(image_dot_path):
            # Execute the 'dot' command
            dot_command = f'dot -Tpng -Nfontname=Arial -Nfontcolor=#483FCC -Ncolor=#483FCC -Ecolor=#483FCC -Npenwidth=2 -Epenwidth=1.5 -o {image_png_path} {image_dot_path}'
            subprocess.run(dot_command, shell=True, check=True)

            return send_file(image_png_path, mimetype='image/png')

    return 'Image not found', 404

@app.route('/png', methods=['POST'])
def get_png():
    image_filename = request.form.get('filename')
    image_filepath = os.path.join('./src', image_filename)
    if os.path.exists(image_filepath):
        return send_file(image_filepath, mimetype='png')
    return 'Image not found', 404

def process_file(file_path):
    # Read the saved file and write to a directory
    with open(file_path, 'rb') as file:
        content = file.read()
    print(content)
    # Perform further processing or writing to the desired directory
    # destination_path = '/path/to/destination/folder'  # Set the desired destination folder path
    # # Write the file to the destination folder
    # with open(os.path.join(destination_path, os.path.basename(file_path)), 'w') as dest_file:
    #     dest_file.write(content)
if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = './upload'  # Set the desired upload folder path
    app.run()
    # file_path = os.path.join('./upload', 'test1234.txt')
    # process_file(file_path)
