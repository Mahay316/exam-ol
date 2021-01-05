from flask import Flask, redirect, request, session, url_for
from common.Role import *
from decorators import login_required
from models import init_db
from views import exam_bp, auth_bp, class_bp, paper_bp, question_bp, student_bp, mentor_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')


# 全局拦截器

# 全局错误处理
@app.route('/')
def redirect_to_index():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
@login_required('redirect')
def index():
    """
    负责根据用户身份在后端进行重定向，装饰器定义了未登录的操作
    函数体返回给用户对应页面
    """
    role = session.get('role')
    if role == STUDENT or role == MENTOR:
        return app.send_static_file('html/class_list.html')
    elif role == ADMIN:
        return redirect('/mentor/manage')


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
    app.register_blueprint(mentor_bp, url_prefix='/mentor')
    app.register_blueprint(exam_bp, url_prefix='/exam')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(class_bp, url_prefix='/class')
    app.register_blueprint(paper_bp, url_prefix='/paper')
    app.register_blueprint(question_bp, url_prefix='/question')
    app.run(debug=True)
