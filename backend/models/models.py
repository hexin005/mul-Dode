from core.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class School(db.Model):
    """影系模型"""
    __tablename__ = 'schools'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # 关系
    provinces = db.relationship('Province', backref='school', lazy=True)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Province(db.Model):
    """省份模型"""
    __tablename__ = 'provinces'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    region = db.Column(db.String(100))
    shape_features = db.Column(db.Text)
    color_features = db.Column(db.Text)
    singing_features = db.Column(db.Text)
    representative_plays = db.Column(db.Text)
    image1 = db.Column(db.String(255))
    image2 = db.Column(db.String(255))
    image3 = db.Column(db.String(255))
    image4 = db.Column(db.String(255))
    image5 = db.Column(db.String(255))
    image6 = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # 外键
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'region': self.region,
            'shape_features': self.shape_features,
            'color_features': self.color_features,
            'singing_features': self.singing_features,
            'representative_plays': self.representative_plays,
            'image1': self.image1,
            'image2': self.image2,
            'image3': self.image3,
            'image4': self.image4,
            'image5': self.image5,
            'image6': self.image6,
            'school_id': self.school_id
        }