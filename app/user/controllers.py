# -*- coding: utf-8 -*-
'''
Created on 2017年3月3日

@author: guxiwen
'''

from app.models.user import *
from sqlalchemy import or_


class UserControllers(object):
    @staticmethod
    def get_id_by_username(username):
        cu = user_info.query.filter(user_info.username==username).first()
        if cu is None:
            return None
        return str(cu.user_id)

    @staticmethod
    def get_username_by_id(user_id):
        cu = user_info.query.filter(user_info.user_id==user_id).first()
        if cu is None:
            return None
        return str(cu.username)
    
    @staticmethod
    def get_user_info_id(user_id):
        return user_info.query.filter(user_info.user_id==user_id).first()
    
    @staticmethod
    def get_all_user_list():
        result = []
        cu = user_info.query.filter(user_info.enable == 1)
        for user in cu:
            result.append({"username":user.username,"user_id":user.user_id})
        return result
    
    
    @staticmethod
    def verify_password(username,password):
        cu = user_info.query.filter(user_info.username==username,user_info.password==password,user_info.enable==1).first()
        if cu is None:
            return False
        return cu
    
    @staticmethod
    def add_group(data):
        new_group = user_group(group_name=data['group_name'],leader_id=data['leader_id'],leader_name=data['leader_name'],is_enable=1)
        try:
            db.session.add(new_group)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def update_group(group_id,data):
        try:
            db.session.query(user_group).filter(user_group.group_id == group_id).update(data)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def get_all_group():
        return user_group.query.filter(user_group.is_enable == 1)
    
    @staticmethod
    def get_all_group_list():
        result = []
        cu = user_group.query.filter(user_group.is_enable == 1)
        for group in cu:
            result.append({"group_name":group.group_name,"group_id":group.group_id})
        return result
    
    @staticmethod
    def get_group_by_name(group_name):
        return user_group.query.filter(user_group.is_enable == 1,user_group.group_name == group_name)
    
    @staticmethod
    def get_group_by_id(group_id):
        return user_group.query.filter(user_group.is_enable == 1,user_group.group_id == group_id)
    
    @staticmethod
    def add_user(data):
        new_user = user_info(username=data['username'],password=data['password'],enable=data['enable'],leader_id=data['leader_id'],\
                              user_type=data['user_type'],user_mail=data['user_mail'])
        try:
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def get_all_user():
        return user_info.query.filter(user_info.enable == 1)
    
    @staticmethod
    def add_config_detail(data):
        new_detail = detail_config(content=data['content'],req_type=data['req_type'],group_id=data['group_id'],remarks=data['remarks'],\
                                   charge_man=data['charge_man'],is_enable=data['is_enable'])
        try:
            db.session.add(new_detail)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
    
    @staticmethod
    def update_config_detail(detail_id,data):
        try:
            db.session.query(detail_config).filter(detail_config.id == detail_id).update(data)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def get_all_config_detail():
        return db.session.query(detail_config,user_group.group_name).join(user_group,detail_config.group_id==user_group.group_id).filter(detail_config.is_enable == 1)
    
    @staticmethod
    def get_all_leaders():
        result = []
        cu = user_info.query.filter(user_info.enable == 1).filter(or_(user_info.user_type == 2,user_info.user_type == 4))
        for user in cu:
            result.append({"leader_name":user.username})
        return result  
        
        
if __name__ == "__main__":
    UserControllers.get_id_by_username('xixi')