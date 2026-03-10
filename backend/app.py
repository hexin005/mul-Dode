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

# 声明 Mail 实例 (必须在工厂函数外)
mail = Mail()
# db = SQLAlchemy()
migrate = Migrate()  # 创建 Migrate 实例


def create_app(config_name='default'):
    app = Flask(__name__)
    
    # 加载基础配置
    app.config.from_object(config[config_name])
 
    
    # 邮件与安全配置（开发环境临时配置，生产环境移到.env）
    app.config.update(
        SECRET_KEY='sfasfnbjasfnk',  # Session加密必需
        MAIL_SERVER='smtp.qq.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='3034206204@qq.com',  # 替换为你的QQ邮箱
        MAIL_PASSWORD='vdgvmhclltpgddid'    # 替换为你的QQ邮箱SMTP授权码（非登录密码）
    )
    
    # 核心：CORS配置，明确允许跨域携带Cookie
    CORS(app, 
         supports_credentials=True,  # 允许跨域携带 Cookie/Session
         resources={r"/api/*": {      # 只对 /api 开头的接口生效
             "origins": "http://localhost:5173",  # 你的前端地址
             "allow_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
         }})
    # 注：localhost:5173是Vue默认启动端口，若你的前端端口不同请修改
    


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
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')