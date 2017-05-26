# -*- coding: utf-8 -*-
'''
Created on 2017年3月7日

@author: guxiwen
'''

from app import *
from sqlalchemy.sql import func

class req_base(db.Model):
    
    __table__name = 'req_base'
    req_id = db.Column(db.Integer,primary_key=True)
    req_name = db.Column(db.String(50))
    content = db.Column(db.String(100))
    img_url = db.Column(db.String(50))
    create_time = db.Column(db.DateTime,default=func.datetime('now','localtime'))
    raise_test_date = db.Column(db.Date)
    raise_audit_date = db.Column(db.Date)
    upline_date = db.Column(db.Date)
    create_man = db.Column(db.String(20))
    status = db.Column(db.Integer)
    version= db.Column(db.String(10))
    remarks = db.Column(db.String(200))
    is_force = db.Column(db.Integer)
    pre_upline_date = db.Column(db.Date)
    last_change_time = db.Column(db.DateTime)
    last_change_man = db.Column(db.String(20))
    back1 = db.Column(db.String(1))
    back2 = db.Column(db.String(1))
    back3 = db.Column(db.String(1))

class req_detail(db.Model):
    
    __table__name = 'req_detail'
    detail_id = db.Column(db.Integer,primary_key=True)
    req_id = db.Column(db.Integer)
    content = db.Column(db.String(100))
    req_type = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    is_confirm = db.Column(db.Integer)
    operate_man = db.Column(db.String(20))
    operate_id = db.Column(db.Integer)
    operate_time = db.Column(db.Time)
    remarks = db.Column(db.String(200))
    charge_man = db.Column(db.String(20))
    
    