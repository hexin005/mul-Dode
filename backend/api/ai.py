from flask import Blueprint, jsonify, request
from services.ai_client import MultiModelAPIClient

# 创建AI功能蓝图
ai_bp = Blueprint('ai', __name__, url_prefix='/api')

# 初始化AI客户端实例
ai_client = MultiModelAPIClient()

@ai_bp.route('/generate_image', methods=['POST'])
def generate_image():
    """生成图像接口"""
    try:
        # 获取请求参数
        data = request.get_json()
        prompt = data.get('prompt')
        model_name = data.get('model_name', 'model1')  # 默认使用model1
        size = data.get('size', '2K')  # 默认尺寸为2K
        
        # 验证参数
        if not prompt:
            return jsonify({'error': '缺少必要参数: prompt'}), 400
        
        # 调用AI生成图像
        result = ai_client.generate_image(prompt, model_name=model_name, size=size)
        
        if result['success']:
            return jsonify({
                'success': True,
                'image_url': result['image_url'],
                'model_used': result['model_used']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_bp.route('/chat', methods=['POST'])
def chat():
    """聊天接口"""
    try:
        # 获取请求参数
        data = request.get_json()
        message = data.get('message')
        model_name = data.get('model_name', 'model1')  # 默认使用model1
        temperature = data.get('temperature', 0.7)  # 默认温度
        max_tokens = data.get('max_tokens', 1000)  # 默认最大token数
        
        # 验证参数
        if not message:
            return jsonify({'error': '缺少必要参数: message'}), 400
        
        # 调用AI聊天接口
        result = ai_client.call_chat_api(
            message, 
            model_name=model_name, 
            temperature=temperature, 
            max_tokens=max_tokens
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'content': result['content'],
                'model_used': result['model_used']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_bp.route('/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    try:
        # 返回可用模型信息
        return jsonify({
            'success': True,
            'models': [
                {
                    'name': 'model1',
                    'description': 'AI模型1',
                    'default_model': 'doubao-seed-1-6-vision-250815'
                },
                {
                    'name': 'model2', 
                    'description': 'AI模型2',
                    'default_model': 'doubao-seed-1-6-vision-250815'
                }
            ]
        }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500