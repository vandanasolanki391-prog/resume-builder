import sqlite3
import json
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ================= UPLOAD FOLDER =================
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= HOME =================
@app.route('/')
def home():
    return render_template('home.html')

# ================= CREATE =================
@app.route('/create')
def create():
    template = request.args.get('template', 'ats')
    return render_template('form.html', selected_template=template)

# ================= SITEMAP =================
@app.route('/sitemap.xml')
def sitemap():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://resume-builder-idja.onrender.com/</loc>
  </url>
</urlset>''', 200, {'Content-Type': 'application/xml'}

# ================= PAGES =================
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

# ================= PREVIEW =================
@app.route('/preview', methods=['POST'])
def preview():
    data = request.form.to_dict()
    photo = request.files.get('photo')

    # Save photo
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

# ================= SAVE RESUME =================
@app.route('/save', methods=['POST'])
def save_resume():
    data = request.form.to_dict()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute(
        'INSERT INTO resumes (data) VALUES (?)',
        (json.dumps(data),)
    )

    conn.commit()
    conn.close()

    return '''
    <h2>Resume Saved Successfully!</h2>
    <a href="/my-resumes">Go to My Resumes</a>
    '''

# ================= MY RESUMES =================
@app.route('/my-resumes')
def my_resumes():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('SELECT id, data FROM resumes ORDER BY id DESC')
    rows = c.fetchall()

    conn.close()

    resumes = []

    for row in rows:
        resumes.append({
            'id': row[0],
            'data': json.loads(row[1])
        })

    return render_template('my_resumes.html', resumes=resumes)

# ================= EDIT RESUME =================
@app.route('/edit/<int:resume_id>')
def edit_resume(resume_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('SELECT data FROM resumes WHERE id=?', (resume_id,))
    row = c.fetchone()

    conn.close()

    if row:
        data = json.loads(row[0])
        return render_template('form.html', data=data)

    return 'Resume not found'

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
