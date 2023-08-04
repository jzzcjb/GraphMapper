# db.py
import pymysql

pymysql.connections.DEBUG = True
# conn = pymysql.connect("数据库地址", "用户名", "密码", "数据库名称")
conn = pymysql.connect(host="localhost", user="root", port=3306, password="", database="CVE_scores", unix_socket="/var/run/mysqld/mysqlx.sock")
# 原命令 conn = pymysql.connect(host="localhost", user="root", port=33062, password="", database="CVE_scores")
# 参考https://stackoverflow.com/questions/6885164/pymysql-cant-connect-to-mysql-on-localhost?rq=3 修改添加unix_socket
# 直接conn.cursor()返回的是一个二元元组，加入参数"pymysql.cursors.DictCursor"可以返回一个字典形式类似[{},{},{}]
cur = conn.cursor(pymysql.cursors.DictCursor)

def get_score(ID):
    sql = "select score from CVEs where ID = '{ID}';"
    cur.execute(sql)
    result = cur.fetchall()
    return result

print(get_score('CVE-2013-7491'))