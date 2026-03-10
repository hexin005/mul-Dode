from flask import Blueprint, jsonify, request
from models import Province, School
from core.database import db

# 创建蓝图
provinces_bp = Blueprint('provinces', __name__, url_prefix='/api/provinces')

@provinces_bp.route('/', methods=['GET'])
def get_provinces():
    """获取所有省份信息"""
    try:
        # 查询所有省份及其关联的影系信息
        provinces = Province.query.join(School).add_columns(
            Province.id,
            Province.name.label('province_name'),
            Province.region,
            Province.shape_features,
            Province.color_features,
            Province.singing_features,
            Province.representative_plays,
            Province.image1,
            Province.image2,
            Province.image3,
            Province.image4,
            Province.image5,
            Province.image6,
            School.name.label('school_name')
        ).all()
        
        # 转换为字典列表
        result = []
        for province in provinces:
            result.append({
                'id': province.id,
                'province_name': province.province_name,
                'region': province.region,
                'shape_features': province.shape_features,
                'color_features': province.color_features,
                'singing_features': province.singing_features,
                'representative_plays': province.representative_plays,
                'image1': province.image1,
                'image2': province.image2,
                'image3': province.image3,
                'image4': province.image4,
                'image5': province.image5,
                'image6': province.image6,
                'school_name': province.school_name
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@provinces_bp.route('/<int:province_id>', methods=['GET'])
def get_province_detail(province_id):
    """获取特定省份的详细信息"""
    try:
        # 查询特定省份及其关联的影系信息
        province = Province.query.join(School).add_columns(
            Province.id,
            Province.name.label('province_name'),
            Province.region,
            Province.shape_features,
            Province.color_features,
            Province.singing_features,
            Province.representative_plays,
            Province.image1,
            Province.image2,
            Province.image3,
            Province.image4,
            Province.image5,
            Province.image6,
            School.name.label('school_name'),
            School.id.label('school_id')
        ).filter(Province.id == province_id).first()
        
        if province:
            result = {
                'id': province.id,
                'province_name': province.province_name,
                'region': province.region,
                'shape_features': province.shape_features,
                'color_features': province.color_features,
                'singing_features': province.singing_features,
                'representative_plays': province.representative_plays,
                'image1': province.image1,
                'image2': province.image2,
                'image3': province.image3,
                'image4': province.image4,
                'image5': province.image5,
                'image6': province.image6,
                'school_name': province.school_name,
                'school_id': province.school_id
            }
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Province not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500