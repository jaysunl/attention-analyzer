from flask import Flask, render_template, redirect, url_for, session, request
import uuid
from datetime import datetime
# import users

app = Flask(__name__)
app.secret_key = "key123"

@app.route('/')
def index():
    if 'sessions' not in session:
        session['sessions'] = []
    return render_template('index.html', sessions=session['sessions'])

@app.route('/new_session', methods=['POST'])
def new_session():
    session_name = request.form.get('session_name')
    session_id = str(uuid.uuid4())
    session_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session_data = {'id': session_id, 'name': session_name, 'datetime': session_datetime}
    session['sessions'].append(session_data)
    session.modified = True
    return redirect(url_for('index'))

@app.route('/session/<session_id>')
def view_session(session_id):
    session_data = next((s for s in session['sessions'] if s['id'] == session_id), None)
    if session_data:
        return render_template('session.html', session=session_data)
    return "Session not found", 404

@app.route('/delete_session/<session_id>')
def delete_session(session_id):
    session['sessions'] = [s for s in session['sessions'] if s['id'] != session_id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
