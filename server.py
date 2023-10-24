from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import prediction
import os

app = Flask(__name__)
Uploaded_images = "Uploaded_images"
app.config['UPLOAD_FOLDER'] = Uploaded_images

@app.route('/', methods=['GET', 'POST'])
def upload_and_display():
    image_path = None
    output = ""
    
    if request.method == 'POST':
        if 'myfile' not in request.files:
            return redirect(request.url)
        file = request.files['myfile']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_path = filename  # Store the filename for rendering
            output = prediction.prediction(file_path)

    return render_template('index.html', image_path=image_path, output=output)

@app.route('/Uploaded_images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(port=3000)
