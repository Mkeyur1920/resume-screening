from flask import Flask, request, render_template
import os
import fitz  # PyMuPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_resume(file_path):
    text = ""
    document = fitz.open(file_path)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

REQUIRED_KEYWORDS = ['Python', 'Flask Developer', 'Machine Learning', 'Data Analyst',
                     'Front-end Developer','Flutter Developer','React-Native Developer','Mern-Stack Developer',
                     'Data Scientist','Cardiologist','Endocrinologist']

def match_keywords(resume_text):
    matched_keywords = [keyword for keyword in REQUIRED_KEYWORDS if keyword.lower() in resume_text.lower()]
    return matched_keywords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        resume_text = process_resume(file_path)
        matched_keywords = match_keywords(resume_text)
        return f"File uploaded and processed and also Matched keywords: {matched_keywords}"
    return "File upload failed"

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
