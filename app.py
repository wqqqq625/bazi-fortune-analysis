"""
Flask 后端服务器
提供八字分析 API
"""
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import secrets
from bazi_calculator import calculate_bazi, get_day_master, analyze_with_deepseek, analyze_2026_yunshi

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = secrets.token_hex(32)  # 生成随机密钥用于session
CORS(app, supports_credentials=True)  # 允许跨域请求和携带凭证

# DeepSeek API Key
DEEPSEEK_API_KEY = "sk-ce5f3d16c611492ca98a3fda8e77dc17"

# 用户账户数据库（10个用户）
USERS = {
    'user001': 'pass001',
    'user002': 'pass002',
    'user003': 'pass003',
    'user004': 'pass004',
    'user005': 'pass005',
    'user006': 'pass006',
    'user007': 'pass007',
    'user008': 'pass008',
    'user009': 'pass009',
    'user010': 'pass010'
}

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """快速计算八字信息（不包含AI分析）"""
    try:
        data = request.get_json()
        
        # 获取用户输入
        nickname = data.get('nickname', '').strip()
        birth_date_str = data.get('birthDate', '')
        birth_time_str = data.get('birthTime', '')
        
        # Validate required fields
        if not nickname:
            return jsonify({'error': 'Please enter your name'}), 400
        if not birth_date_str:
            return jsonify({'error': 'Please select date of birth'}), 400
        
        # Parse date and time
        try:
            if birth_time_str:
                dt = datetime.strptime(f"{birth_date_str} {birth_time_str}", "%Y-%m-%d %H:%M")
            else:
                dt = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError as e:
            return jsonify({'error': 'Invalid date format'}), 400
        
        # 计算八字（这部分很快）
        bazi = calculate_bazi(dt)
        day_master = get_day_master(bazi['day'])
        
        # 立即返回八字信息
        return jsonify({
            'nickname': nickname,
            'bazi': bazi,
            'dayMaster': day_master
        })
        
    except Exception as e:
        print(f"Calculation error: {e}")
        return jsonify({'error': f'Calculation failed: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """AI分析（较慢，异步调用）"""
    try:
        data = request.get_json()
        
        # 获取用户输入
        nickname = data.get('nickname', '').strip()
        gender = data.get('gender', '')
        birth_date_str = data.get('birthDate', '')
        birth_time_str = data.get('birthTime', '')
        
        # Validate required fields
        if not nickname:
            return jsonify({'error': 'Please enter your name'}), 400
        if not gender:
            return jsonify({'error': 'Please select gender'}), 400
        if not birth_date_str:
            return jsonify({'error': 'Please select date of birth'}), 400
        
        # Parse date and time
        try:
            if birth_time_str:
                dt = datetime.strptime(f"{birth_date_str} {birth_time_str}", "%Y-%m-%d %H:%M")
            else:
                dt = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError as e:
            return jsonify({'error': 'Invalid date format'}), 400
        
        # 计算八字
        bazi = calculate_bazi(dt)
        day_master = get_day_master(bazi['day'])
        
        # 使用 DeepSeek AI 分析
        analysis_result = analyze_with_deepseek(
            bazi=bazi,
            day_master=day_master,
            nickname=nickname,
            gender=gender,
            api_key=DEEPSEEK_API_KEY
        )
        
        # 分析2026年丙午年运势
        yunshi_2026 = analyze_2026_yunshi(
            bazi=bazi,
            day_master=day_master,
            nickname=nickname,
            api_key=DEEPSEEK_API_KEY
        )
        
        # 返回AI分析结果
        result = {
            **analysis_result,
            'yunshi2026': yunshi_2026
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': '请输入用户名和密码'}), 400
        
        # 验证用户名和密码
        if username in USERS and USERS[username] == password:
            session['username'] = username
            session['logged_in'] = True
            return jsonify({
                'success': True,
                'message': '登录成功',
                'username': username
            })
        else:
            return jsonify({'error': '用户名或密码错误'}), 401
            
    except Exception as e:
        print(f"登录错误: {e}")
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({'success': True, 'message': '已登出'})

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    """检查登录状态"""
    if session.get('logged_in'):
        return jsonify({
            'logged_in': True,
            'username': session.get('username')
        })
    else:
        return jsonify({'logged_in': False})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    """首页"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """服务静态文件"""
    if os.path.exists(path) and os.path.isfile(path):
        return send_from_directory('.', path)
    # 如果是 HTML 文件但不存在于当前目录，返回 404
    if path.endswith('.html'):
        return "页面不存在", 404
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

