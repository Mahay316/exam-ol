import os

SECRET_KEY = os.urandom(24)

# SQLAlchemy configuration
# 数据库连接URI，如 mysql+mysqlconnector://root:password@localhost/exam
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_TRACK_MODIFICATIONS = True
