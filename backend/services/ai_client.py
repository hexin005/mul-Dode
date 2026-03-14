import os
import requests
import json
import traceback
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiModelAPIClient:
    """多模型API客户端，支持调用不同的AI模型"""
    
    def __init__(self):
        # 加载.env文件中的环境变量
        load_dotenv()
        logger.info("开始加载环境变量...")
        
        # 打印环境变量加载状态
        model1_key = os.getenv('MODEL1_API_KEY')
        model2_key = os.getenv('MODEL2_API_KEY')
        logger.info(f"MODEL1_API_KEY 已加载: {model1_key is not None}")
        logger.info(f"MODEL2_API_KEY 已加载: {model2_key is not None}")
        
        # 从环境变量初始化两个不同模型的API配置
        self.models = {
            "model1": {
                "api_key": model1_key,
                "endpoint": os.getenv('MODEL1_ENDPOINT', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'),
                "timeout": int(os.getenv('MODEL1_TIMEOUT', '60')),
                "default_model": os.getenv('MODEL1_DEFAULT_MODEL', 'doubao-seed-1-6-vision-250815')
            },
            "model2": {
                "api_key": model2_key,
                "endpoint": os.getenv('MODEL2_ENDPOINT', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'),
                "timeout": int(os.getenv('MODEL2_TIMEOUT', '60')),
                "default_model": os.getenv('MODEL2_DEFAULT_MODEL', 'doubao-seed-1-6-vision-250815')
            }
        }
        
        # 初始化图像生成端点
        self.image_endpoint = os.getenv('IMAGE_GENERATION_ENDPOINT', 'https://ark.cn-beijing.volces.com/api/v3/images/generations')
        logger.info(f"图像生成端点: {self.image_endpoint}")
        
        logger.info("环境变量加载完成")
    
    def _create_headers(self, api_key: str) -> Dict[str, str]:
        """创建请求头，包含API密钥"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def call_chat_api(self, message: str, model_name: str = "model1", 
                     custom_model: Optional[str] = None, 
                     temperature: float = 0.7, 
                     max_tokens: int = 4096) -> Dict[str, Any]:
        """
        调用聊天API，支持选择不同的模型
        
        Args:
            message (str): 用户消息内容
            model_name (str): 选择要使用的模型配置，支持'model1'或'model2'
            custom_model (str, optional): 自定义模型名称，优先级高于默认配置
            temperature (float): 生成温度参数
            max_tokens (int): 最大生成token数
            
        Returns:
            Dict: 包含成功状态和响应内容的字典
        """
        try:
            # 验证模型选择
            if model_name not in self.models:
                logger.error(f"不支持的模型: {model_name}")
                return {
                    "success": False,
                    "error": f"不支持的模型: {model_name}，请选择'model1'或'model2'"
                }
            
            model_config = self.models[model_name]
            headers = self._create_headers(model_config["api_key"])
            
           
           # ai_client.py - call_chat_api 函数内部

            # --- ✅ 适中优化版：既保留深度，又防止滥竽充数 ---
            system_instruction = (
                "你是皮影戏非遗传承智能助手。请用中文回答。"
                "回答原则：\n"
                "1. 【详略得当】：对于历史、工艺等核心内容，可以详细展开，展现文化底蕴。\n"
                "2. 【精选代表】：在介绍流派或剧目时，不要罗列清单。请挑选最具代表性的 5-8 个进行深入一点的点评，而非泛泛而谈几十个。\n"
                "3. 【结构清晰】：多使用分段和由点到面的方式回答，确保在 1000 字以内能把核心讲透。\n"
                "4. 【完整性】：必须确保回答有始有终，严禁在句子中间中断。"
            )
            # ----------------------------------------------------

            # 构建请求数据 (保持不变，确保 max_tokens 足够大)
            payload = {
                "model": custom_model or model_config["default_model"],
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,     # 稍微降低一点随机性，让回答更稳
                "max_tokens": 4096      # ✅ 保持这个最大值，给它足够的空间去“适中”
            }
            
            logger.info(f"正在使用 {model_name} 发送API请求...")
            response = requests.post(
                model_config["endpoint"],
                headers=headers,
                json=payload,
                timeout=model_config["timeout"]
            )
            
            # 处理响应
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and data["choices"]:
                    logger.info(f"API调用成功，使用模型: {model_name}")
                    return {
                        "success": True,
                        "content": data["choices"][0].get("message", {}).get("content", ""),
                        "model_used": model_name,
                        "full_response": data  # 保存完整响应供调试使用
                    }
                else:
                    logger.warning("API返回格式不正确")
                    return {
                        "success": False,
                        "error": "API返回格式不正确",
                        "response_data": data
                    }
            else:
                logger.error(f"API调用失败: 状态码 {response.status_code}")
                return {
                    "success": False,
                    "error": f"API调用失败: 状态码 {response.status_code}",
                    "response_text": response.text[:200] + "..." if len(response.text) > 200 else response.text  # 限制错误信息长度
                }
                
        except requests.Timeout:
            logger.error("请求超时")
            return {
                "success": False,
                "error": "请求超时，请稍后重试"
            }
        except requests.ConnectionError:
            logger.error("网络连接错误")
            return {
                "success": False,
                "error": "网络连接错误，请检查网络设置"
            }
        except Exception as e:
            logger.error(f"调用过程中发生错误: {str(e)}")
            logger.debug(traceback.format_exc())  # 只在调试级别记录详细堆栈
            return {
                "success": False,
                "error": f"调用过程中发生错误: {str(e)}"
            }
    
    def generate_image(self, prompt: str, model_name: str = "model1", 
                      size: str = "2K", 
                      response_format: str = "url") -> Dict[str, Any]:
        """
        使用指定模型生成图像
        
        Args:
            prompt (str): 图像生成提示词
            model_name (str): 选择要使用的模型配置
            size (str): 图像尺寸，支持'2K'、'1K'等
            response_format (str): 响应格式，支持'url'或其他格式
            
        Returns:
            Dict: 包含成功状态和图像URL的字典
        """
        try:
            # 验证模型选择
            if model_name not in self.models:
                logger.error(f"不支持的模型: {model_name}")
                return {
                    "success": False,
                    "error": f"不支持的模型: {model_name}，请选择'model1'或'model2'"
                }
            
            model_config = self.models[model_name]
            headers = self._create_headers(model_config["api_key"])
            
            payload = {
                "model": "doubao-seedream-4-0-250828",
                "prompt": prompt,
                "size": size,
                "response_format": response_format,
                "sequential_image_generation": "disabled",
                "stream": False,
                "watermark": True
            }
            
            logger.info(f"正在使用 {model_name} 生成图像...")
            # 确保使用正确的图像生成端点
            response = requests.post(
            self.image_endpoint,  # 现在这个属性已正确初始化
            headers=headers,
            json=payload,
            timeout=60  # 图像生成需要更长时间
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data'] and 'url' in data['data'][0]:
                    logger.info(f"图像生成成功，使用模型: {model_name}")
                    return {
                        "success": True,
                        "image_url": data['data'][0]['url'],
                        "model_used": model_name
                    }
                else:
                    logger.warning("图像生成失败: 返回格式不正确")
                    return {
                        "success": False,
                        "error": "图像生成失败: 返回格式不正确",
                        "response_data": data
                    }
            else:
                logger.error(f"图像API调用失败: 状态码 {response.status_code}")
                return {
                    "success": False,
                    "error": f"图像API调用失败: 状态码 {response.status_code}",
                    "response_text": response.text[:200] + "..." if len(response.text) > 200 else response.text
                }
                
        except requests.Timeout:
            logger.error("图像生成请求超时")
            return {"success": False, "error": "图像生成请求超时"}
        except requests.ConnectionError:
            logger.error("网络连接错误")
            return {"success": False, "error": "网络连接错误"}
        except Exception as e:
            logger.error(f"图像生成过程中发生错误: {str(e)}")
            logger.debug(traceback.format_exc())
            return {
                "success": False,
                "error": f"图像生成过程中发生错误: {str(e)}"
            }