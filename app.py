from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create')
def create():
    return render_template('form.html')

@app.route('/preview', methods=['POST'])
def preview():
    data = request.form

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
