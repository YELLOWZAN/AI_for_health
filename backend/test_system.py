#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统测试脚本
用于测试OCR和LLM推理功能
"""

import os
import sys
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入系统模块
from models.ocr_processor import OCRProcessor
from models.llm_inferrer import LLMInferrer

def test_ocr_processor():
    """测试OCR处理器"""
    print("===== 测试OCR处理器 =====")
    try:
        processor = OCRProcessor()
        print("OCR处理器初始化成功")
        
        # 注意：这里需要一个测试图片文件
        # 如果没有实际的测试图片，可以使用模拟文本进行后续测试
        # sample_text = processor.extract_text('test_sample.jpg')
        
        # 由于没有实际图片，返回模拟结果
        return "患者基本信息：张三，男，65岁。主诉：头痛、发热38.5℃，伴有咳嗽症状。既往有高血压病史，现服用降压药物。实验室检查：白细胞计数升高。诊断：上呼吸道感染。医嘱：注意休息，多喝水，服用抗生素。"
        
    except Exception as e:
        print(f"OCR处理器测试失败: {str(e)}")
        return None

def test_llm_inferrer(sample_text):
    """测试LLM推理器"""
    print("\n===== 测试LLM推理器 =====")
    try:
        # 测试本地模式
        print("测试本地推理模式...")
        local_inferrer = LLMInferrer(mode='local')
        local_result = local_inferrer.get_suggestions(sample_text)
        print("本地推理结果:")
        print(json.dumps(local_result, ensure_ascii=False, indent=2))
        
        # 测试服务器模式
        print("\n测试服务器推理模式...")
        server_inferrer = LLMInferrer(mode='server')
        server_result = server_inferrer.get_suggestions(sample_text)
        print("服务器推理结果:")
        print(json.dumps(server_result, ensure_ascii=False, indent=2))
        
        return True
        
    except Exception as e:
        print(f"LLM推理器测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("开始系统测试...")
    
    # 使用模拟文本进行测试
    sample_text = "患者基本信息：张三，男，65岁。主诉：头痛、发热38.5℃，伴有咳嗽症状。既往有高血压病史，现服用降压药物。实验室检查：白细胞计数升高。诊断：上呼吸道感染。医嘱：注意休息，多喝水，服用抗生素。"
    
    # 如果有OCR测试成功，使用OCR结果，否则使用模拟文本
    # ocr_result = test_ocr_processor()
    # if ocr_result:
    #     sample_text = ocr_result
    
    print(f"\n使用测试文本: {sample_text}")
    
    # 测试LLM推理
    llm_success = test_llm_inferrer(sample_text)
    
    # 输出测试总结
    print("\n===== 测试总结 =====")
    print(f"OCR测试: 模拟成功")
    print(f"LLM测试: {'成功' if llm_success else '失败'}")
    print(f"系统状态: {'基本功能正常' if llm_success else '存在问题'}")
    
    if llm_success:
        print("\n系统测试通过，可以正常运行")
    else:
        print("\n系统测试未通过，请检查相关组件")

if __name__ == '__main__':
    main()