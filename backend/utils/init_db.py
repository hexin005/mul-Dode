from app import app, db
# 必须导入所有模型类，SQLAlchemy 才能识别并建表
from models.models import User, School, Province 

with app.app_context():
    print("正在连接数据库并创建名册表...")
    db.create_all()
    print("数据库搭建成功！")