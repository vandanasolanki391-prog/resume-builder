from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create')
def create():
    template = request.args.get("template", "ats")
    return render_template('form.html', selected_template=template)

@app.route('/preview', methods=['POST'])
def preview():
    data = request.form.to_dict()
    photo = request.files.get('photo')

    if photo and photo.filename != '':
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
        data['photo'] = f"uploads/{filename}"
    else:
        data['photo'] = None

    education = zip(
        request.form.getlist('degree'),
        request.form.getlist('institute'),
        request.form.getlist('year'),
        request.form.getlist('percentage')
    )

    experience = zip(
        request.form.getlist('company'),
        request.form.getlist('role'),
        request.form.getlist('duration'),
        request.form.getlist('description')
    )

    return render_template(
        'preview.html',
        data=data,
        education=education,
        experience=experience
    )

if __name__ == '__main__':
    app.run(debug=True)
