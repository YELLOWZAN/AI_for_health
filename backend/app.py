import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# 导入自定义模块
from models.ocr_processor import OCRProcessor
from models.llm_inferrer import LLMInferrer

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化处理器
ocr_processor = OCRProcessor()
inferrer = LLMInferrer(
    mode=os.getenv('INFERENCE_MODE', 'local'),
    local_model_path=os.getenv('LOCAL_MODEL_PATH', './models/'),
    server_api_url=os.getenv('SERVER_API_URL', 'http://localhost:8866/predict')
)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """文件上传接口"""
    # 检查是否有文件部分
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    
    file = request.files['file']
    
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    # 检查文件类型
    if file and allowed_file(file.filename):
        # 安全保存文件
        filename = secure_filename(file.filename)
        # 添加时间戳避免文件名冲突
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # 1. OCR提取文本
            text = ocr_processor.extract_text(filepath)
            
            # 2. LLM处理获取建议
            suggestions = inferrer.get_suggestions(text)
            
            # 3. 后处理结果
            formatted_result = {
                'text': text,
                'suggestions': suggestions,
                'disclaimer': '本建议仅供参考，不构成医疗诊断，请咨询专业医生获取准确诊断',
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify({'success': True, 'result': formatted_result})
            
        except Exception as e:
            return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500
        finally:
            # 可选：处理完成后删除临时文件
            # os.remove(filepath)
            pass
    else:
        return jsonify({'error': '不支持的文件类型'}), 400

@app.route('/api/inference-mode', methods=['GET', 'POST'])
def set_inference_mode():
    """获取或设置推理模式"""
    if request.method == 'GET':
        return jsonify({'mode': inferrer.mode})
    elif request.method == 'POST':
        data = request.get_json()
        mode = data.get('mode')
        if mode in ['local', 'server']:
            inferrer.mode = mode
            # 更新环境变量文件
            with open('../.env', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open('../.env', 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.startswith('INFERENCE_MODE='):
                        f.write(f'INFERENCE_MODE={mode}\n')
                    else:
                        f.write(line)
            return jsonify({'success': True, 'mode': mode})
        else:
            return jsonify({'error': '无效的推理模式，必须是local或server'}), 400

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """提供上传文件的访问"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)