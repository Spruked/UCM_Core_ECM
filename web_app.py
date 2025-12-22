from flask import Flask, request, jsonify, render_template
import os
import json
from werkzeug.utils import secure_filename
from main import UCMReasoningCore

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'json', 'md', 'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize UCM Core
core = UCMReasoningCore()

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400

        query = data['query'].strip()
        if not query:
            return jsonify({'error': 'Empty query'}), 400

        # Process the query through UCM Core ECM
        result = core.reason(query)

        return jsonify({
            'query': query,
            'verdict': result.get('verdict', 'UNKNOWN'),
            'confidence': result.get('confidence', 0.0),
            'shadow_count': result.get('shadow_count', 0),
            'timestamp': result.get('timestamp', '')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            continue
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append({
                'filename': filename,
                'size': os.path.getsize(filepath),
                'type': file.content_type
            })

    return jsonify({
        'message': f'Successfully uploaded {len(uploaded_files)} files',
        'files': uploaded_files
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'UCM Core ECM Web Interface'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)