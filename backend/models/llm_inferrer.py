import os
import requests
import json

class LLMInferrer:
    """LLM推理器，支持本地和服务器两种推理模式"""
    
    def __init__(self, mode='local', local_model_path='./models/', server_api_url='http://localhost:8866/predict'):
        """
        初始化LLM推理器
        
        Args:
            mode: 推理模式，'local'或'server'
            local_model_path: 本地模型路径
            server_api_url: 服务器推理API地址
        """
        self.mode = mode
        self.local_model_path = local_model_path
        self.server_api_url = server_api_url
        self.model = None
        
        # 如果是本地模式，初始化模型
        if mode == 'local':
            self._init_local_model()
    
    def _init_local_model(self):
        """初始化本地模型"""
        try:
            # 这里使用PaddlePaddle的模型
            # 注意：实际应用中需要使用适合的医疗领域模型
            print("初始化本地模型...")
            # 由于没有实际的医疗模型，这里使用一个模拟的模型
            # 在实际项目中，应该加载真实的医疗领域LLM
            self.model = True  # 模拟模型已加载
            print("本地模型初始化完成")
        except Exception as e:
            print(f"本地模型初始化失败: {str(e)}")
            # 失败时切换到服务器模式
            self.mode = 'server'
            print("已切换到服务器模式")
    
    def get_suggestions(self, medical_text):
        """
        根据病历文本获取医疗建议
        
        Args:
            medical_text: 从病历中提取的文本
            
        Returns:
            dict: 医疗建议结果
        """
        # 构建提示词
        prompt = self._build_prompt(medical_text)
        
        # 根据模式选择推理方式
        if self.mode == 'local':
            return self._infer_local(prompt)
        else:
            return self._infer_server(prompt)
    
    def _build_prompt(self, medical_text):
        """
        构建提示词
        
        Args:
            medical_text: 医疗文本
            
        Returns:
            str: 完整的提示词
        """
        prompt = f"""
你是一位专业的医疗顾问，请根据以下病历内容提供专业、准确的医疗建议。

病历内容：
{medical_text}

请提供以下内容：
1. 对病历内容的简要总结
2. 可能的健康问题分析
3. 建议的下一步行动
4. 生活方式调整建议（如适用）

注意：你的回答仅供参考，不构成医疗诊断，请在实际应用中提醒用户咨询专业医生。
"""
        return prompt
    
    def _infer_local(self, prompt):
        """
        本地推理
        
        Args:
            prompt: 提示词
            
        Returns:
            dict: 推理结果
        """
        try:
            # 这里是模拟本地推理
            # 实际应用中应该使用真实的模型进行推理
            print(f"本地推理中，提示词长度: {len(prompt)}")
            
            # 由于没有实际模型，返回模拟结果
            # 注意：在实际项目中，这里应该调用真实的模型进行推理
            return {
                "summary": "这是病历内容的简要总结（模拟）",
                "analysis": "基于病历内容的健康问题分析（模拟）",
                "recommendations": [
                    "建议1：继续观察症状变化",
                    "建议2：保持良好的生活习惯",
                    "建议3：如症状加重，及时就医"
                ],
                "lifestyle_advice": "健康的生活方式建议（模拟）",
                "mode": "local"
            }
        except Exception as e:
            print(f"本地推理失败: {str(e)}")
            # 失败时切换到服务器模式并重新尝试
            self.mode = 'server'
            return self._infer_server(prompt)
    
    def _infer_server(self, prompt):
        """
        服务器推理
        
        Args:
            prompt: 提示词
            
        Returns:
            dict: 推理结果
        """
        try:
            print(f"服务器推理中，请求API: {self.server_api_url}")
            
            # 准备请求数据
            data = {
                "prompt": prompt,
                "max_length": 2048,
                "temperature": 0.7
            }
            
            # 发送请求
            response = requests.post(
                self.server_api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=30  # 设置超时
            )
            
            # 检查响应
            if response.status_code == 200:
                result = response.json()
                # 格式化结果
                return {
                    "summary": result.get("summary", ""),
                    "analysis": result.get("analysis", ""),
                    "recommendations": result.get("recommendations", []),
                    "lifestyle_advice": result.get("lifestyle_advice", ""),
                    "mode": "server"
                }
            else:
                print(f"服务器返回错误状态码: {response.status_code}")
                # 返回模拟结果作为备选
                return self._get_fallback_suggestions()
                
        except Exception as e:
            print(f"服务器推理失败: {str(e)}")
            # 返回模拟结果作为备选
            return self._get_fallback_suggestions()
    
    def _get_fallback_suggestions(self):
        """
        当推理失败时返回的备选建议
        
        Returns:
            dict: 备选建议
        """
        return {
            "summary": "无法获取病历分析，请检查输入或重试",
            "analysis": "系统暂时无法提供详细分析",
            "recommendations": ["建议您咨询专业医生获取准确诊断"],
            "lifestyle_advice": "保持健康的生活方式对恢复健康非常重要",
            "mode": "fallback"
        }

# 示例使用
if __name__ == '__main__':
    inferrer = LLMInferrer(mode='server')
    sample_text = "患者主诉头痛、发热38.5℃，伴有咳嗽症状。既往有高血压病史，现服用降压药物。"
    suggestions = inferrer.get_suggestions(sample_text)
    print(json.dumps(suggestions, ensure_ascii=False, indent=2))