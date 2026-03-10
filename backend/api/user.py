from flask import Blueprint, request, jsonify, session, current_app
from flask_mail import Message
from core.database import db
from models.models import User
import re
import random
import time

# 创建蓝图，前缀/api/user
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# 验证码发送频率限制：60秒内只能发一次
def check_send_frequency(email):
    last_send = session.get(f'last_send_{email}')
    if last_send and time.time() - last_send < 60:
        return False
    return True

# 发送验证码接口
@user_bp.route('/send-code', methods=['POST'])
def send_code():
    # 获取请求参数
    data = request.get_json() or {}
    email = data.get('email')
    
    # 1. 校验邮箱是否为空
    if not email:
        return jsonify({"code": 400, "msg": "请输入邮箱"}), 400
    
    # 2. 校验邮箱格式
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        return jsonify({"code": 400, "msg": "邮箱格式不正确"}), 400
    
    # 3. 校验发送频率
    if not check_send_frequency(email):
        return jsonify({"code": 400, "msg": "验证码发送过于频繁，请60秒后重试"}), 400
    
    # 4. 生成6位数字验证码
    code = str(random.randint(100000, 999999))
    expire_at = time.time() + 300  # 5分钟有效期
    
    # 5. 存储验证码：与邮箱绑定，防止串号
    session[f'verify_code_{email}'] = {
        'code': code,
        'expire_at': expire_at
    }
    # 记录最后发送时间
    session[f'last_send_{email}'] = time.time()

    # 6. 构造并发送邮件
    try:
        msg = Message(
            subject="【光影千年】注册验证码",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f"尊驾好！您的名册录入验证码为：{code}，请于5分钟内填写，切勿泄露给他人。"
        
        from app import mail
        mail.send(msg)
        return jsonify({"code": 200, "msg": "验证码发送成功"})
    
    except Exception as e:
        # 发送失败：清除无效的Session数据
        session.pop(f'verify_code_{email}', None)
        session.pop(f'last_send_{email}', None)
        current_app.logger.error(f"邮件发送失败：{str(e)}")
        return jsonify({"code": 500, "msg": f"验证码发送失败：{str(e)}"}), 500

# 注册接口
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    code = data.get('code')
    
    # 1. 基础参数校验
    if not all([username, password, email, code]):
        return jsonify({"code": 400, "msg": "请填写完整的注册信息"}), 400
    
    # 2. 校验验证码（与邮箱绑定）
    verify_key = f'verify_code_{email}'
    verify_info = session.get(verify_key)
    if not verify_info:
        return jsonify({"code": 400, "msg": "请先获取验证码"}), 400
    if verify_info['code'] != code:
        return jsonify({"code": 400, "msg": "验证码错误"}), 400
    if time.time() > verify_info['expire_at']:
        session.pop(verify_key, None)
        return jsonify({"code": 400, "msg": "验证码已过期，请重新获取"}), 400
    
    # 3. 校验用户名和密码规则
    if len(username) < 3:
        return jsonify({"code": 400, "msg": "用户名至少3个字符"}), 400
    if len(password) < 6:
        return jsonify({"code": 400, "msg": "密码至少6个字符"}), 400
    
    # 4. 校验用户名/邮箱是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "msg": "该用户名已被占用"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"code": 400, "msg": "该邮箱已被注册"}), 400
    
    # 5. 创建用户并写入数据库
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # 密码加密存储
        db.session.add(new_user)
        db.session.commit()
        
        # 清除验证码，防止重复使用
        session.pop(verify_key, None)
        session.pop(f'last_send_{email}', None)
        
        return jsonify({"code": 200, "msg": "注册成功"})
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"注册失败：{str(e)}")
        return jsonify({"code": 500, "msg": f"注册失败：{str(e)}"}), 500

# 登录接口
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    remember = data.get('remember', False)
    
    # 1. 校验参数
    if not all([username, password]):
        return jsonify({"code": 400, "msg": "请填写用户名和密码"}), 400
    
    # 2. 查询用户并校验密码
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"code": 401, "msg": "名号或秘钥错误"}), 401
    
    # 3. 构造响应
    user_info = {"id": user.id, "username": user.username, "email": user.email}
    res = jsonify({"code": 200, "msg": "欢迎归阁", "user": user_info})
    
    # 4. 记住我功能：设置cookie
    if remember:
        res.set_cookie(
            'remember_token',
            'secure_token_here',  # 生产环境替换为真实的用户token
            max_age=30*24*3600,   # 30天有效期
            httponly=True,        # 防止XSS攻击
            secure=False,         # 开发环境关闭，生产环境开启HTTPS后设为True
            samesite='Lax'        # 跨域Cookie策略
        )
    
    # 5. 存储用户ID到Session
    session['user_id'] = user.id
    
    return res