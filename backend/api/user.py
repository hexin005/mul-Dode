from flask import Blueprint, request, jsonify, session, current_app
from flask_mail import Message
from core.database import db
from models.models import User
import re
import random
import time
import os
import uuid
from datetime import timedelta

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
    # 3. 构造响应
    user_info = {
        "id": user.id, 
        "username": user.username, 
        "email": user.email,
        "avatar": user.avatar_url  # ⚠️ 关键：必须把刚才在模型里加的头像字段传给前端！
    }
    res = jsonify({"code": 200, "msg": "登录成功", "user": user_info})
    
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


# 👇 在文件最底部，新增上传头像接口
# 图片保存目录：指向你架构中的 backend/images/user_image/
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/user_image')

@user_bp.route('/avatar', methods=['POST'])
def upload_avatar():
    # 接收前端传来的用户名（因为咱们还没用JWT，暂时用用户名识别身份）
    username = request.form.get('username')
    if not username:
        return jsonify({"code": 400, "msg": "未提供用户信息"}), 400
        
    if 'avatar' not in request.files:
        return jsonify({"code": 400, "msg": "没有找到图片文件"}), 400
        
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({"code": 400, "msg": "未选择文件"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"}), 404

    # 🌟 新增：物理删除旧头像机制 🌟
    if user.avatar_url:
        # 提取出旧图片的文件名 (例如从 http://localhost:5000/images/user_image/avatar_123.jpg 提取出 avatar_123.jpg)
        old_filename = user.avatar_url.split('/')[-1]
        old_filepath = os.path.join(UPLOAD_FOLDER, old_filename)
        
        # 如果硬盘上确实存在这个旧文件，就把它删掉
        if os.path.exists(old_filepath):
            try:
                os.remove(old_filepath)
            except Exception as e:
                current_app.logger.warning(f"删除旧头像失败: {str(e)}")

    # 确保 images 文件夹存在
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # 生成安全且唯一的文件名 (防覆盖、防乱码)
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
    unique_filename = f"avatar_{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    # 保存到硬盘
    file.save(save_path)
    
    # 因为你的 app.py 里配了 @app.route('/images/<path:filename>')
    # 所以网络访问路径就是 http://localhost:5000/images/xxx.jpg
    avatar_url = f"http://localhost:5000/images/user_image/{unique_filename}"
    
    # 更新数据库
    user.avatar_url = avatar_url
    db.session.commit()
    
    return jsonify({
        "code": 200,
        "msg": "上传成功",
        "data": {"avatarUrl": avatar_url}
    })

# 在 user.py 中添加
@user_bp.route('/info', methods=['GET'])
def get_user_info():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"code": 401, "msg": "未登录"}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"}), 404
        
    return jsonify({
        "code": 200,
        "msg": "获取成功",
        "data": {
            "username": user.username,
            "avatar": user.avatar_url,
            "email": user.email
        }
    })

# user.py
@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  # 清除服务器端 Session 记录
    response = jsonify({"code": 200, "msg": "登出成功"})
    
    # 彻底抹除 Cookie：设置过期时间为 0
    # 注意：如果你的 Cookie 设置了 path，这里也要对应上
    response.set_cookie('session', '', expires=0, path='/')
    response.delete_cookie('remember_token', path='/')
    
    return response