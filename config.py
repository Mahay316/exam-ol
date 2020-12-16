import os

SECRET_KEY = os.urandom(24)

# SQLAlchemy configuration
# 数据库连接URI，如 mysql+mysqlconnector://root:password@localhost/exam
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 数据库连接配置
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'exam'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

# 数据库连接池初始化的容量
POOL_SIZE = 5

# 连接池最大溢出容量，该容量+初始容量=最大容量。超出会堵塞等待，等待时间为timeout参数值默认30
MAX_OVERFLOW = 10
