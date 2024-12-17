from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import uuid
import sys
import traceback
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 存储上传的文件信息
uploaded_files = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def scan_qr_code(image_path):
    try:
        print(f"\nScanning image: {image_path}")
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"Error: File does not exist: {image_path}")
            return []

        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image: {image_path}")
            return []

        # 创建QRCode检测器
        qr_detector = cv2.QRCodeDetector()
        
        # 检测和解码QR码
        retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(image)
        
        results = []
        if retval:
            for data in decoded_info:
                if data:  # 确保数据不为空
                    print(f"Found QR code with data: {data}")
                    results.append({
                        'type': 'QR_CODE',
                        'data': data
                    })
        else:
            # 如果多重检测失败，尝试单个检测
            retval, decoded_info, points = qr_detector.detectAndDecode(image)
            if retval:
                print(f"Found single QR code with data: {decoded_info}")
                results.append({
                    'type': 'QR_CODE',
                    'data': decoded_info
                })

        # 如果没有找到QR码，尝试不同的图像预处理
        if not results:
            # 转换为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 应用自适应阈值
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            
            retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(thresh)
            if retval:
                for data in decoded_info:
                    if data:
                        print(f"Found QR code after preprocessing with data: {data}")
                        results.append({
                            'type': 'QR_CODE',
                            'data': data
                        })

        print(f"Total QR codes found: {len(results)}")
        return results

    except Exception as e:
        print(f"Error processing {image_path}:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        traceback.print_exc()
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files[]')
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # 保存文件信息到内存中
            file_info = {
                'original_name': filename,
                'saved_name': unique_filename,
                'path': filepath
            }
            uploaded_files.append(file_info)
            results.append(file_info)
    
    return jsonify(results)

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify(uploaded_files)

@app.route('/scan', methods=['POST'])
def scan_files():
    print("\n=== Starting scan process ===")
    print(f"Number of files to scan: {len(uploaded_files)}")
    results = []
    
    for file_info in uploaded_files:
        print(f"\nProcessing file: {file_info['original_name']}")
        print(f"File path: {file_info['path']}")
        
        if not os.path.exists(file_info['path']):
            print(f"File does not exist: {file_info['path']}")
            continue
            
        qr_results = scan_qr_code(file_info['path'])
        print(f"QR code results: {qr_results}")
        
        results.append({
            'filename': file_info['original_name'],
            'qr_codes': qr_results
        })
    
    print("\n=== Scan process completed ===")
    print(f"Final results: {results}")
    return jsonify(results)

@app.route('/clear', methods=['POST'])
def clear_files():
    # 删除所有上传的文件
    for file_info in uploaded_files:
        try:
            if os.path.exists(file_info['path']):
                os.remove(file_info['path'])
        except Exception as e:
            print(f"Error deleting file {file_info['path']}: {str(e)}")
    uploaded_files.clear()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print(f"Python version: {sys.version}")
    print("OpenCV version:", cv2.__version__)
    print("Starting Flask application...")
    app.run(debug=True) 