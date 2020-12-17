from flask import Flask, render_template
from models import init_db
from views import exam_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')


# 全局拦截器

# 全局错误处理
@app.route('/')
def index():
    return render_template('exam_online.html')


if __name__ == '__main__':
    # 为了避免循环引用，延时初始化数据库
    app.app_context().push()
    init_db(app)

    # 在此处注册蓝图
    app.register_blueprint(exam_bp, url_prefix='/exam')
    app.run(debug=True)
