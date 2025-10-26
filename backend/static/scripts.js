// DOM元素
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const imagePreview = document.getElementById('image-preview');
const previewSection = document.getElementById('preview-section');
const processingSection = document.getElementById('processing-section');
const resultsSection = document.getElementById('results-section');
const processingStatus = document.getElementById('processing-status');
const textResult = document.getElementById('text-result');
const summary = document.getElementById('summary');
const analysis = document.getElementById('analysis');
const recommendations = document.getElementById('recommendations');
const lifestyleAdvice = document.getElementById('lifestyle-advice');
const disclaimerText = document.getElementById('disclaimer-text');
const inferenceMode = document.getElementById('inference-mode');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

// 文件拖放事件
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    dropArea.classList.add('drag-over');
}

function unhighlight() {
    dropArea.classList.remove('drag-over');
}

// 处理拖放的文件
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        handleFiles(files[0]);
    }
}

// 处理文件选择
fileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        handleFiles(this.files[0]);
    }
});

// 处理文件
function handleFiles(file) {
    // 检查文件类型
    const validTypes = ['image/png', 'image/jpeg', 'image/gif'];
    if (!validTypes.includes(file.type)) {
        alert('请上传有效的图片文件（PNG、JPG、GIF）');
        return;
    }
    
    // 显示预览
    previewSection.style.display = 'block';
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
    }
    reader.readAsDataURL(file);
    
    // 上传文件进行处理
    uploadFile(file);
}

// 上传文件到服务器
function uploadFile(file) {
    // 显示处理中状态
    processingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    processingStatus.textContent = '正在上传文件...';
    
    const formData = new FormData();
    formData.append('file', file);
    
    // 设置处理状态
    processingStatus.textContent = '正在提取病历信息...';
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('服务器响应错误');
        }
        return response.json();
    })
    .then(data => {
        processingStatus.textContent = '分析完成，正在生成建议...';
        
        // 处理响应数据
        if (data.success) {
            // 填充提取的文本
            textResult.textContent = data.result.text || '无法提取文本';
            
            // 填充建议内容
            const suggestions = data.result.suggestions;
            summary.textContent = suggestions.summary || '无法生成总结';
            analysis.textContent = suggestions.analysis || '无法生成分析';
            
            // 填充建议列表
            recommendations.innerHTML = '';
            if (suggestions.recommendations && suggestions.recommendations.length > 0) {
                suggestions.recommendations.forEach(rec => {
                    const li = document.createElement('li');
                    li.textContent = rec;
                    recommendations.appendChild(li);
                });
            } else {
                recommendations.innerHTML = '<li>暂无具体建议</li>';
            }
            
            lifestyleAdvice.textContent = suggestions.lifestyle_advice || '无法生成生活方式建议';
            
            // 显示免责声明
            disclaimerText.textContent = data.result.disclaimer || '本建议仅供参考，不构成医疗诊断，请咨询专业医生获取准确诊断';
            
            // 显示结果
            setTimeout(() => {
                processingSection.style.display = 'none';
                resultsSection.style.display = 'block';
                // 默认显示提取的文本标签页
                switchTab('extracted-text');
            }, 1000);
        } else {
            throw new Error(data.error || '处理失败');
        }
    })
    .catch(error => {
        console.error('错误:', error);
        processingSection.style.display = 'none';
        alert('处理文件时出错: ' + error.message);
    });
}

// 切换推理模式
inferenceMode.addEventListener('change', function() {
    const mode = this.value;
    
    fetch('/api/inference-mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mode: mode })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('推理模式已切换为:', mode);
        } else {
            console.error('切换模式失败:', data.error);
            // 恢复之前的选择
            const previousMode = data.mode || 'local';
            this.value = previousMode;
        }
    })
    .catch(error => {
        console.error('切换模式时出错:', error);
    });
});

// 页面加载时获取当前推理模式
window.addEventListener('DOMContentLoaded', function() {
    fetch('/api/inference-mode')
        .then(response => response.json())
        .then(data => {
            if (data.mode) {
                inferenceMode.value = data.mode;
            }
        })
        .catch(error => {
            console.error('获取推理模式时出错:', error);
        });
});

// 标签页切换
function switchTab(tabId) {
    // 隐藏所有标签页内容
    tabPanes.forEach(pane => {
        pane.classList.remove('active');
    });
    
    // 移除所有标签按钮的活动状态
    tabBtns.forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示选中的标签页内容
    document.getElementById(tabId).classList.add('active');
    
    // 设置选中标签按钮的活动状态
    tabBtns.forEach(btn => {
        if (btn.onclick.toString().includes(tabId)) {
            btn.classList.add('active');
        }
    });
}

// 平滑滚动到结果区域
function scrollToResults() {
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}