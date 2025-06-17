from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from app.utils import extract_text_from_file

from app.analyzer import analyze_resume_against_jd


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__, template_folder='app/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('resume')
        jd = request.form.get('job_description')

        if not file or not jd:
            return 'Missing file or job description'

        if file.filename == '':
            return 'No file selected'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            resume_text = extract_text_from_file(filepath)
            analysis = analyze_resume_against_jd(resume_text, jd)
            return render_template('result.html', analysis=analysis)
    return render_template('index.html')




if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
