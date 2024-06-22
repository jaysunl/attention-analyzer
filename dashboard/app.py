from flask import Flask, render_template, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = "key123"

@app.route('/')
def index():
    if 'sessions' not in session:
        session['sessions'] = []
    return render_template('index.html', sessions=session['sessions'])

@app.route('/new_session')
def new_session():
    session_id = str(uuid.uuid4())
    session['sessions'].append(session_id)
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
