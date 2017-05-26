# -*- coding: utf-8 -*-
'''
Created on Oct 4, 2016

@author: guxiwen
'''
import datetime
import time

from sqlalchemy.sql.expression import or_

from app.models import *


class  reqController(object):
    @staticmethod
    def get_req_by_id(req_id):
        return requirements_base.query.filter(requirements_base.req_id == req_id).first()
    
    @staticmethod
    def get_reqs():
        return requirements_base.query.order_by(requirements_base.raise_date.desc()).all()
    
    @staticmethod
    def get_req_by_user_id(user_id):
        keyword = '%' + str(user_id) + '%'
        return requirements_base.query.filter(requirements_base.test_man_id.like(keyword)).\
            order_by(requirements_base.raise_date.desc()).all()
    
    @staticmethod
    def get_userinfo_by_id(user_id):
        return user_info.query.filter(user_info.user_id == user_id).first()
    
    @staticmethod
    def get_userinfo_by_username(username):
        return user_info.query.filter(user_info.user_name == username).first()
    
    @staticmethod
    def assign_req_sql(req_id,dic,assign):
        #更新requirements_base表
        try:
            db.session.add(assign)
            db.session.flush()
            dic["assign_id"] = assign.assign_id
            db.session.query(requirements_base).filter(requirements_base.req_id == req_id).update(dic)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def upline_sql(req_id,dic):
        try:
            db.session.query(requirements_base).filter(requirements_base.req_id == req_id).update(dic)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def claim_sql(req_id,dic):
        try:
            db.session.query(requirements_base).filter(requirements_base.req_id == req_id).update(dic)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def all_req_filter(status,raise_man,test_man,raise_date,upline_date):
        cu = requirements_base.query
        if status is not None and status <> '0':
            cu = cu.filter(requirements_base.status == int(status))
            
        if raise_man is not None and raise_man <> '':
            cu = cu.filter(requirements_base.raise_man == raise_man)
            
        if test_man is not None and test_man <> '':
            test_man_id = reqController.get_userinfo_by_username(test_man)
            if test_man_id is not None:
                cu = cu.filter(requirements_base.test_man_id.like("%"+str(test_man_id.user_id)+"%"))
                
        if raise_date is not None and raise_date <> '0':
            off_set,now_date = reqController.date_offset(raise_date)
            cu = cu.filter(requirements_base.raise_date.between(off_set,now_date))
            
        if upline_date is not None and upline_date <> '0':
            off_set,now_date = reqController.date_offset(upline_date)
            cu = cu.filter(requirements_base.upline_date.between(off_set,now_date))
        
        return cu.order_by(requirements_base.raise_date.desc()).all()
    
    @staticmethod
    def date_offset(d_type):
        #1一周内2一月内3一年内
        now_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        now_date = datetime.datetime.strptime(now_date,'%Y-%m-%d').date()
        if d_type == '1':
            off_set = now_date + datetime.timedelta(-7)
        elif d_type == '2':
            off_set = now_date + datetime.timedelta(-30)
        else:
            off_set = now_date + datetime.timedelta(-365)
        return off_set,now_date
    
    @staticmethod
    def data_transfer(dic):
        tmp_dic = dic
        for i in tmp_dic.keys():
            if tmp_dic[i] is None:
                tmp_dic[i] = ""
        return tmp_dic
    
    @staticmethod
    def dliver_page(reqs,pageSize,pageNum):
        count = len(reqs)
        tmp = []
        if count%pageSize == 0:
            totalNum = count/pageSize
        else:
            totalNum = count/pageSize + 1
        index_s = (pageNum - 1) * pageSize
        index_e = pageNum * pageSize
        index_e = count if index_e >= count else index_e
        for i in xrange(index_s,index_e):
            tmp.append(reqs[i])
        return tmp,totalNum
class  dataController(object):
    @staticmethod
    def week_count(m,s):
        return requirements_base.query.filter(requirements_base.status.in_((2,3))).\
            filter(or_(requirements_base.upline_date.between(m,s),requirements_base.status==2)).\
            order_by(requirements_base.raise_date.desc()).all()