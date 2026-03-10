from flask import Blueprint, jsonify
from models import School

# 创建蓝图
schools_bp = Blueprint('schools', __name__, url_prefix='/api/schools')

@schools_bp.route('/', methods=['GET'])
def get_schools():
    """获取所有影系信息"""
    try:
        # 查询所有影系
        schools = School.query.all()
        
        # 转换为字典列表
        result = [school.to_dict() for school in schools]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500