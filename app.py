from flask import Flask
from models import init_db
from views import exam_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

# 全局拦截器

# 全局错误处理


#使用pycharm运行flask环境时不能加__name__ == '__main__'的判断

# 为了避免循环引用，延时初始化数据库
app.app_context().push()
init_db(app)

# 在此处注册蓝图
# app.register_blueprint(auth)
app.register_blueprint(exam_bp, url_prefix='/exam')
