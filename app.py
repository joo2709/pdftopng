from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'outputs'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# 디렉토리 없으면 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf_to_png():
    if 'pdf' not in request.files:
        return jsonify(success=False, message="PDF 파일이 없습니다.")

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify(success=False, message="파일명이 비어있습니다.")

    filename = secure_filename(pdf_file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(input_path)

    # 여기에서 PDF를 PNG로 변환하는 로직을 넣어야 함 (아직 미구현)
    # 예시로는 변환된 파일이 fixed_output.png 라고 가정
    output_filename = filename.rsplit('.', 1)[0] + '.png'
    output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)

    # PDF → PNG 변환 기능은 나중에 구현 (지금은 더미 파일로 대체)
    with open(output_path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')  # PNG 헤더 (실제 변환 로직은 추후에 추가할게)

    return jsonify(success=True, download_url=f'/download/{output_filename}')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')  # 안전한 로컬 전용 IP
