# -*- coding: utf-8 -*-
'''
Created on 2017年3月8日

@author: guxiwen
'''
import time
import datetime

class DateUtil(object):
    
    @staticmethod
    def get_current_time(t,strFormat):
        if t == 1:
            tmp = time.strftime(strFormat,time.localtime())
            tmp = datetime.datetime.strptime(tmp,strFormat)
            print tmp
            print type(tmp)
            return tmp
        elif t == 2:
            return time.localtime() 
        else:
            return time.time()
        
    @staticmethod
    def get_now_date(t,strFormat):
        '''
        t=1 date类型， 其他 string类型
        '''
        if t == 1:
            now_date = time.strftime(strFormat,time.localtime())
            return datetime.datetime.strptime(now_date,strFormat).date()
        else:
            return time.strftime("%Y-%m-%d",time.localtime())
        
class ResultFormat(object):
    
    def __init__(self,data,message,success,code):
        self.data = data
        self.message = message
        self.success = success
        self.code = code
    
    def getData(self):
        return {'data':self.data,'message':self.message,'success':self.success,'code':self.code}
    
class InfoUtil(object):
    MESSAGE_SUCCESS = u'操作成功'
    MESSAGE_FAIL = u'操作失败'
    MESSAGE_TIMEOUT = u'操作超时'
    CODE_SUCCESS = 1000
    CODE_FAIL = 1005
    