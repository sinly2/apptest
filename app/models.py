# -*- coding: utf-8 -*-
'''
Created on 2017年3月3日

@author: guxiwen
'''

from app import *
from flask_login import UserMixin

class requirements_base(db.Model):
    __tablename__ = 'requirements_base'
    req_id = db.Column(db.Integer,primary_key=True)
    group_id = db.Column(db.Integer,default=1)
    name = db.Column(db.String(200),unique=False)
    raise_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    upline_date = db.Column(db.Date)
    raise_man = db.Column(db.String(100))
    test_man_id = db.Column(db.String(100))
    #1已提测2已分配（正在测试）3已上线
    status = db.Column(db.Integer)
    assign_time = db.Column(db.Time)
    assign_id = db.Column(db.Integer)
    claim_time = db.Column(db.Time)
    claim_id = db.Column(db.Integer)
    leader_id = db.Column(db.Integer)
    
class req_assign(db.Model):
    __table__name = 'req_assign'
    assign_id = db.Column(db.Integer,primary_key=True)
    assign_time = db.Column(db.Time)
    assign_man_id = db.Column(db.String(100))
    assigned_man_id = db.Column(db.String(200))
    oper_ip = db.Column(db.String(50))
    context = db.Column(db.String(200))
    
class req_claim(db.Model):
    __table__name = 'req_claim'
    claim_id = db.Column(db.Integer,primary_key=True)
    claim_time = db.Column(db.Time)
    claim_man_id = db.Column(db.String(100))
    oper_ip = db.Column(db.String(50))
    context = db.Column(db.String(200))
    
class user_info(UserMixin,db.Model):
    __table__name = 'user_info'
    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(100),unique=True)
    user_type = db.Column(db.Integer)
    password = db.Column(db.String(100))
    user_mail = db.Column(db.String(100))
    def get_id(self):
        return unicode(self.user_id)
    
@login_manager.user_loader
def load_user(user_id):
    return user_info.query.get(int(user_id))