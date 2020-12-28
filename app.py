from flask import Flask, render_template, session, redirect, jsonify, url_for, request
from models import init_db
from views import exam_bp, auth_bp, class_bp, paper_bp
from common.Role import *

app = Flask(__name__)
app.config.from_pyfile('config.py')


# 全局拦截器

# 全局错误处理
@app.route('/')
def redirect_to_index():
    # return render_template('add_question.html')
    # return render_template('paper_preview.html')
    # return render_template('new_paper.html')
    # return render_template('exam_detail.html')
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
def index():
    """
    负责根据用户身份在后端进行重定向，将不同身份用户定向到对应首页
    如果未登录则定向到登录页，异常身份则报404
    """
    if 'role' not in session:
        return redirect(url_for('auth_bp.login'))

    if request.method == 'GET':
        role = session.get('role')
        if role == STUDENT:
            # TODO 跳转学生主页
            pass
        elif role == MENTOR:
            return render_template('teacher_adm.html')
        elif role == ADMIN:
            # TODO 跳转管理员主页
            pass
        else:
            return jsonify({'code': 403})


@app.route('/class')
def get_class():
    return render_template('class_manage.html')


@app.errorhandler(404)
def page_not_found(err):
    """自定义404页面"""
    return render_template('error-404.html')


if __name__ == '__main__':
    # 为了避免循环引用，延时初始化数据库
    app.app_context().push()
    init_db(app)

    # 在此处注册蓝图
    app.register_blueprint(paper_bp, url_prefix='/paper')
    app.register_blueprint(class_bp, url_prefix='/class')
    app.register_blueprint(exam_bp, url_prefix='/exam')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.run(debug=True)
