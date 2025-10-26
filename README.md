# 医疗病历分析系统

基于PaddlePaddle开发的医疗病历分析系统，能够读取病历文件，提取文本内容，并通过LLM模型提供健康建议。

## 功能特点

- 📁 支持上传图片格式的病历文件（PNG、JPG、GIF）
- 🔍 使用PaddleOCR进行文本提取
- 🧠 支持本地和服务器两种推理模式
- 💡 提供病历总结、健康分析和建议
- 📱 响应式设计，支持各种设备访问
- ⚠️ 自动添加免责声明，确保合规性

## 系统架构

```
用户 --> 前端页面 --> 后端API --> OCR处理 --> LLM推理 --> 结果返回 --> 前端展示
```

## 安装依赖

1. 克隆或下载项目代码
2. 安装所需依赖：

```bash
pip install -r requirements.txt
```

## 环境配置

系统使用`.env`文件进行配置，主要配置项包括：

- `INFERENCE_MODE`: 推理模式，可选值为`local`（本地）或`server`（服务器）
- `LOCAL_MODEL_PATH`: 本地模型路径
- `SERVER_API_URL`: 服务器推理API地址
- `UPLOAD_FOLDER`: 文件上传目录
- `MAX_CONTENT_LENGTH`: 最大文件大小（字节）
- `SECRET_KEY`: Flask应用密钥

## 运行系统

1. 确保已安装所有依赖
2. 进入backend目录
3. 运行Flask应用：

```bash
cd backend
python app.py
```

4. 打开浏览器访问：`http://localhost:5000`

## 使用方法

1. 在页面上上传病历图片
2. 选择推理模式（本地或服务器）
3. 等待系统处理完成
4. 查看提取的文本和AI生成的建议

## 注意事项

1. 本系统仅作为辅助工具，不能替代专业医生的诊断
2. 请确保上传的病历图片清晰可读，以获得更好的提取效果
3. 本地推理模式需要足够的计算资源支持
4. 服务器推理模式需要配置正确的API地址

## 技术栈

- **前端**: HTML, CSS, JavaScript
- **后端**: Python, Flask
- **OCR**: PaddleOCR
- **AI框架**: PaddlePaddle
- **其他**: Flask-CORS, python-dotenv

## 项目结构

```
AI_for_health/
├── backend/                  # 后端代码
│   ├── app.py               # 主应用程序
│   ├── models/              # 模型模块
│   │   ├── ocr_processor.py # OCR文本提取
│   │   └── llm_inferrer.py  # LLM推理器
│   ├── static/              # 静态资源
│   │   ├── styles.css       # CSS样式
│   │   └── scripts.js       # JavaScript脚本
│   └── templates/           # HTML模板
│       └── index.html       # 主页面
├── requirements.txt         # 依赖项
├── .env                     # 环境变量配置
└── README.md                # 项目说明
```

## 免责声明

本系统生成的所有建议仅供参考，不构成医疗诊断。如有健康问题，请务必咨询专业医生获取准确的医疗建议。