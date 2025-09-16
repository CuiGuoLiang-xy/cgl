import web
import time
import pymysql
import pymysql.cursors
import redis
from dbutils.pooled_db import PooledDB
# gdb = web.database(
#     dbn='mysql',
#     host='ip',``
#     port ='3306',
#     user = 'root',
#     pw = '123456',
#     db = 'dbname'   
# ) 

# host             # 主机名
# port             # 端口号
# user             # 用户名
# password         # 密码
# charset          # 字符编码方式
# database         # 数据库名
# cursorclass      # cursor类型，指定返回类型，不指定则返回元组
# init_command     # 连接建立时运行的初始语句
# connect_timeout  # 连接超时时间
# autocommit       # 是否自动提交事务

# dbconn = pymysql.connect(
#     host = 'localhost',
#     port = 3306,
#     user = 'root',
#     password = '123456',
#     charset = 'utf8',
#     database = 'gamedb',
#     cursorclass=pymysql.cursors.DictCursor
# )

# cursor = dbconn.cursor()
# sqlStr = "select * from user"
# res = cursor.execute(sqlStr)
# print(res)
# dbconn.commit()
# time.sleep(10)

# sqlStr = "select * from user"
# cursor.execute(sqlStr)
# res = cursor.fetchall()
# print(res)
#获取结果
# cursor.fetchall() #获取所有记录
# cursor.fetchone()#获取一个记录
# cursor.fetchmany(2)#获取指定个数记录

#批量操作
# 示例
# 模拟数据
# data = []
# for i in range(1,101):
#     data.append((i,'123456'))

# start = time.time()

# 使用循环依次执行：0.02866387367248535
# for d in data:
#     sqlStr = "insert into test values(%s, %s)"
#     Config.gdb.execute(sqlStr, d)

# 使用executemany()提升效率：0.00733184814453125
# sqlStr = "insert into test values(%s, %s)"
# Config.gdb.executemany(sqlStr, data)
# Config.mysql.commit()

# end = time.time()
# print(end - start)
#分批处理
# 示例
# 模拟数据
# data = []
# for i in range(1,101):
#     data.append((i,'123456'))

# 分批
# stepSize = 10
# for i in range(0, len(data), stepSize):
#     stepData = data[i:i+stepSize]
#     sqlStr = "insert into test values(%s, %s)"
#     Config.gdb.executemany(sqlStr, stepData)
#     Config.mysql.commit()

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = '123456'
DB_NAME = 'gamedb'

# dbconn = pymysql.connect(
#     host = DB_HOST,#localhost
#     port = DB_PORT,
#     user = DB_USER,
#     password = DB_PWD,
#     database = DB_NAME,
#     cursorclass=pymysql.cursors.DictCursor
# )


#数据库连接池
pool = PooledDB(
    creator = pymysql,      #数据库驱动，使用pymysql连接mysql数据库
    maxconnections = 10,    #连接池中允许的最大连接数
    mincached = 2,          #初始化时创建的空闲连接数
    maxcached = 5,          #连接池中空闲连接的最大数量
    maxshared = 3,          #连接池中共享链连接的最大数目
    blocking = True,        #如果没有可用连接时,是否允许阻塞等待
    host=DB_HOST,         #localhost
    port=DB_PORT,
    user=DB_USER,
    password=DB_PWD,
    db=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor,
)
# conn:pymysql.Connection = pool.connection()
# cursor:pymysql.cursors.Cursor = conn.cursor()

# try:
#     cursor.execute("select * from user")
#     res = cursor.fetchall()
#     for r in res:
#         print(r)
# finally:
#     cursor.close()
#     conn.close()
#账号初始信息配置
DEFAULT_SECPASSWORD = 000000


USER_STATUS_NORMAL = 0
USER_STATUS_FREEZE = 1

grds = redis.Redis(
    host = '127.0.0.1',
    port = 6379,
    password = '123456'
)
KEY_PACKAGE = "KEY_PACKAGE_{userid}"
KEY_PACKAGE_EXPIRE_TIME = 7*24*60*60

SESSION_EXPIRETIME = 10 * 60

MAIL_HOST = "127.0.0.1"
MAIL_POST = "1234"


