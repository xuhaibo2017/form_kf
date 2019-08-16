__author__ = 'Administrator'
# -*- coding: utf-8 -*-
#import MySQLdb
import pymysql
class db_operate:
    def mysql_command(self,conn,sql_cmd):  # 执行sql
       # try:
            ret = []
            conn=pymysql.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
            conn.commit()
            cursor.close()
            conn.close()
        #except pymysql.Error.e:
          #  ret.append(e)
            return ret

    def select_table(self,conn,sql_cmd,parmas):  # 执行带参数的sql
        #try:
            ret = []
            conn=pymysql.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd,parmas)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
            conn.commit()
            cursor.close()
            conn.close()
        #except pymysql.Error e:
         #   ret.append(e)
            return ret

    def select_table2(self,conn,sql_cmd):  # 执行bu带参数的sql
        #try:
            ret = []
            conn=pymysql.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
            conn.commit()
            cursor.close()
            conn.close()
        #except pymysql.Error e:
         #   ret.append(e)
            return ret