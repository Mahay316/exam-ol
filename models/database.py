from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """初始化数据库配置"""
    db.init_app(app)
