from flask import Flask, redirect, request, session, url_for

from common.Role import *
from decorators import login_required
from models import init_db
from views import exam_bp, auth_bp, class_bp, paper_bp, question_bp, student_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')


# 全局拦截器

# 全局错误处理
@app.route('/')
def redirect_to_index():
    session['no'] = 'teacher1_en'
    session['role'] = MENTOR
    return redirect(url_for('class_bp.get_class'))


@app.route('/index', methods=['GET'])
@login_required('redirect')
def index():
    """
    负责根据用户身份在后端进行重定向，将不同身份用户定向到对应首页
    如果未登录则定向到登录页，异常身份则报404
    """
    if request.method == 'GET':
        role = session.get('role')
        if role == STUDENT or role == MENTOR:
            return app.send_static_file('html/class_list.html')
        elif role == ADMIN:
            return app.send_static_file('html/admin.html')


@app.errorhandler(404)
def page_not_found(err):
    """自定义404页面"""
    return app.send_static_file('html/error_404.html')


if __name__ == '__main__':
    # 为了避免循环引用，延时初始化数据库
    app.app_context().push()
    init_db(app)

    # 在此处注册蓝图
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(exam_bp, url_prefix='/exam')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(class_bp, url_prefix='/class')
    app.register_blueprint(paper_bp, url_prefix='/paper')
    app.register_blueprint(question_bp, url_prefix='/question')
    app.run(debug=True)
