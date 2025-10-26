import os
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

class OCRProcessor:
    """OCR文本提取处理器"""
    
    def __init__(self):
        # 初始化PaddleOCR，使用中文模型，尝试使用GPU加速
        # RTX5060支持CUDA，可以启用GPU加速
        self.ocr = PaddleOCR(
            use_angle_cls=True,  # 使用角度分类器
            lang='ch',          # 使用中文模型
            det_model_dir=None,  # 自动下载模型
            rec_model_dir=None,  # 自动下载模型
            cls_model_dir=None   # 自动下载模型
        )
    
    def extract_text(self, file_path):
        """
        从文件中提取文本
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 提取的文本
        """
        try:
            # 判断文件类型
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ['.png', '.jpg', '.jpeg', '.gif']:
                # 处理图片文件
                return self._extract_from_image(file_path)
            elif ext == '.pdf':
                # 处理PDF文件（这里简化处理，实际可能需要pdf2image等库）
                # 由于PaddleOCR不直接支持PDF，这里需要先转换为图片
                # 为了简化，我们先返回一个提示信息
                raise NotImplementedError("PDF处理需要额外配置，请使用图片格式")
            else:
                raise ValueError(f"不支持的文件类型: {ext}")
                
        except Exception as e:
            print(f"OCR提取错误: {str(e)}")
            raise
    
    def _extract_from_image(self, image_path):
        """
        从图片中提取文本
        
        Args:
            image_path: 图片路径
            
        Returns:
            str: 提取的文本
        """
        # 使用PaddleOCR进行文字识别（适配新版本API）
        result = self.ocr.ocr(image_path)
        
        # 提取文本内容
        extracted_text = []
        for idx, line in enumerate(result):
            # 检查结果格式
            if line is None:
                continue
                
            for item in line:
                if len(item) >= 2:
                    # item[1] 包含识别的文本和置信度
                    text = item[1][0]  # 文本内容
                    extracted_text.append(text)
        
        # 将所有文本合并为一个字符串
        return '\n'.join(extracted_text)
    
    def _preprocess_image(self, image_path):
        """
        图片预处理，提高OCR识别准确率
        
        Args:
            image_path: 图片路径
            
        Returns:
            numpy.ndarray: 预处理后的图片
        """
        img = Image.open(image_path)
        
        # 转换为灰度图
        img = img.convert('L')
        
        # 转换为numpy数组
        img_array = np.array(img)
        
        # 简单的二值化处理
        # 这里使用简单的阈值，实际应用中可能需要更复杂的自适应阈值
        threshold = 128
        img_array = (img_array > threshold) * 255
        
        return img_array

# 示例使用
if __name__ == '__main__':
    processor = OCRProcessor()
    try:
        text = processor.extract_text('sample.jpg')
        print("提取的文本:", text)
    except Exception as e:
        print(f"错误: {str(e)}")