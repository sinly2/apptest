# -*- coding: utf-8 -*-
'''
Created on 2017年3月3日

@author: guxiwen
'''
class Util(object):
    #svn需求路径
    svn_path = u"/root/project/TestRequests/app/task/xuqiu,/root/project/TestRequests/app/task/xuqiu_lamordue"
    #redis配置
    redis_host = "127.0.0.1"
    redis_port = 6379
    redis_db = 1
    #db
    db_task = "sqlite:///../data.db"
    
class Message(object):
    @staticmethod
    def message_handle(m):
        return m.encode('utf8')
    
    MESSAGE_EOR = "服务器错误"
    MESSAGE_SUC = "操作成功"
    