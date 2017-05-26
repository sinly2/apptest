# -*- coding: utf-8 -*-
'''
Created on 2017年3月7日

@author: guxiwen
'''
from app import *
from flask_login import UserMixin

class user_info(UserMixin,db.Model):
    
    __table__name = 'user_info'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(80))
    leader_id = db.Column(db.Integer)
    create_time = db.Column(db.Time)
    enable = db.Column(db.Integer)
    last_login_time = db.Column(db.Time)
    user_type = db.Column(db.Integer)
    user_mail = db.Column(db.String(50))
    
    def get_id(self):
        return unicode(self.user_id)

class user_group(db.Model):     
   
    __table__name = 'user_group'
    group_id = db.Column(db.Integer,primary_key=True)
    group_name = db.Column(db.String(20))
    leader_id = db.Column(db.Integer)
    leader_name = db.Column(db.String(20))
    is_enable = db.Column(db.Integer)

class detail_config(db.Model):
    
    __table__name = 'detail_config'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(100))
    req_type = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    remarks = db.Column(db.String(200))
    charge_man = db.Column(db.String(20))
    is_enable = db.Column(db.Integer)
    
@login_manager.user_loader
def load_user(user_id):
    return user_info.query.get(int(user_id))