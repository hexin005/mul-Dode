from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from core.config import config
from core.database import db
from api.provinces import provinces_bp
from api.schools import schools_bp
from api.ai import ai_bp
from api.user import user_bp 
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
# 如果你还没有使用 dotenv 加载环境变量，建议引入以下两行
# from dotenv import load_dotenv
# load_dotenv() 

# 声明 Mail 实例 (必须在工厂函数外)
mail = Mail()
migrate = Migrate()  # 创建 Migrate 实例

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # 加载基础配置
    app.config.from_object(config[config_name])
 
    # 邮件与安全配置（从环境变量/.env中读取，不再硬编码）
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'default-dev-fallback-key'), 
        MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.qq.com'),
        MAIL_PORT=int(os.getenv('MAIL_PORT', 465)),
        MAIL_USE_SSL=os.getenv('MAIL_USE_SSL', 'True') == 'True',
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),  
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')   
    )
    
    # 核心：CORS配置，明确允许跨域携带Cookie
    CORS(app, 
         supports_credentials=True,  
         resources={r"/api/*": {      
             "origins": "http://localhost:5173",  
             "allow_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
         }})

    # 初始化组件
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db) 
    
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(provinces_bp)
    app.register_blueprint(schools_bp)
    app.register_blueprint(ai_bp)
    
    # 图片路由
    @app.route('/images/<path:filename>')
    def get_image(filename):
        return send_from_directory('images', filename)
    
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

    return app

# 创建应用实例
app = create_app(os.getenv('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')