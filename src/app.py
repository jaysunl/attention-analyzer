from flask import Flask, render_template, redirect, url_for, session, request, jsonify
import uuid
from datetime import datetime
import users
import os
import boto3

app = Flask(__name__)
app.secret_key = "key123"

UPLOAD_FOLDER = '../input_images/'
ALLOWED_EXTENSIONS = {'jpg'}
REGION='us-west-1'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table_name = 'attention-data'
user_table = dynamodb.Table(table_name)

@app.route('/')
def index():
    if 'sessions' not in session or not session['sessions']:
        session['sessions'] = []
    try:
        response = user_table.scan()
        items = response.get('Items', [])
        session['sessions'] = []
        for item in items:
            session_data = {}
            for key, val in item.items():
                session_data[str(key)] = val
            session['sessions'].append(session_data)
    except Exception as e:
        print(f"Error scanning table: {e}")

    session['sessions'].sort(key=lambda x: x['datetime'], reverse=True)
    return render_template('index.html', sessions=session['sessions'])

@app.route('/new_session', methods=['POST'])
def new_session():
    session_name = request.form.get('session_name')
    session_id, session_datetime = users.add_session(session_name)
    session_data = {'id': session_id, 'name': session_name, 'datetime': session_datetime}
    session['sessions'].append(session_data)
    session.modified = True

    return redirect(url_for('index'))

@app.route('/session/<session_id>')
def view_session(session_id):
    session_data = next((s for s in session['sessions'] if int(s['id']) == int(session_id)), None)
    if session_data:
        return render_template('session.html', session=session_data)
    return "Session not found", 404

@app.route('/delete_session/<session_id>')
def delete_session(session_id):
    session['sessions'] = [s for s in session['sessions'] if int(s['id']) != int(session_id)]
    session.modified = True
    users.delete_session(session_id)
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify(success=False, message="No file part")

    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message="No selected file")

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify(success=True, filepath=filepath)

    return jsonify(success=False, message="Invalid file type")

if __name__ == '__main__':
    app.run(debug=True)
