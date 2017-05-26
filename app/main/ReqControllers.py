# -*- coding: utf-8 -*-
'''
Created on 2017年3月7日

@author: guxiwen
'''

from app.models.requirements import *
from app.common.util import DateUtil
from app.user.controllers import UserControllers
from app.models.user import *
import datetime

class ReqController(object):
    
    @staticmethod
    def add_req(data):
        data['preUplineDate'] = datetime.datetime.strptime(data['preUplineDate'],'%Y-%m-%d').date()
        new_req = req_base(req_name=data['req_name'],version=data['version'],\
                           status=0,remarks=data['remarks'],create_man='guxiwen',is_force=data['is_force'],pre_upline_date=data['preUplineDate'])
        try:
            db.session.add(new_req)
            db.session.flush()
            req_id = new_req.req_id
#             for detail in data['details']:
#                 new_detail = req_detail(req_id=req_id,content=detail['content'],req_type=detail['req_type'],\
#                                         group_id=detail['group_id'],operate_id=data['user_id'],remarks=detail['remarks'])
#                 db.session.add(new_detail)
#                 db.session.flush()
            db.session.commit()
            return req_id
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def get_req_list(version):
        if version == '':
            cu = req_base.query
        else:
            cu = req_base.query.filter(req_base.version==version)
        cu = cu.order_by(req_base.req_id.desc())
        return cu
    
    @staticmethod
    def get_req_by_id(req_id):
        cu = req_base.query.filter(req_base.req_id==req_id)
        if cu.count() != 0:
            return cu
        else:
            return None
    
    @staticmethod
    def get_req_detail(req_id):
        #cu = req_detail.query.filter(req_detail.req_id == req_id)
        cu = db.session.query(req_detail,user_group.group_name).join(user_group,req_detail.group_id==user_group.group_id).filter(req_detail.req_id == req_id)
        return cu
    
    @staticmethod
    def update_detail(detail_id,data):
        try:
            db.session.query(req_detail).filter(req_detail.detail_id == detail_id).update(data)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def add_detail(data):
        new_detail = req_detail(req_id=data['req_id'],content=data['content'],req_type=data['req_type'],group_id=data['group_id'],\
                                operate_man=data['operate_man'],operate_id=data['operate_id'],remarks=data['remarks'],charge_man=data['charge_man'],\
                                is_confirm=0)
        try:
            db.session.add(new_detail)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
    @staticmethod
    def add_default_detail(req_id):
        cu = UserControllers.get_all_config_detail()
        g_cu = UserControllers.get_all_group()
        sys_id = 3
        flag = 1
        for detail in cu:
            tmp = detail.detail_config
            data = {"content":tmp.content,"req_type":tmp.req_type,"group_id":tmp.group_id,"remarks":tmp.remarks,"req_id":req_id,"charge_man":tmp.charge_man,\
                    "operate_man":"sys","operate_id":0}
            if tmp.group_id == sys_id:
                for g in g_cu:
                    if g.group_id == sys_id:
                        continue
                    else:
                        data["group_id"] = g.group_id 
                        data["charge_man"] = g.leader_name
                    if not ReqController.add_detail(data):
                        flag = 0
                        break
            else:
                if not ReqController.add_detail(data):
                    flag = 0
                    break    
        return flag
        
    @staticmethod
    def get_req_name_by_id(req_id):
        cu = req_base.query.filter(req_base.req_id == req_id)
        return cu
        
    @staticmethod
    def update_requirement(req_id,data):
        try:
            db.session.query(req_base).filter(req_base.req_id == req_id).update(data)
            db.session.commit()
            return True
        except Exception,e:
            print e
            db.session.rollback()
            return False
        
    @staticmethod
    def upline_check(req_id):
        '''需求上线前检查'''
        cu = req_base.query.filter(req_base.req_id == req_id)
        if cu.count() != 1:
            return 1
        cu = req_detail.query.filter(req_detail.req_id == req_id)
        if cu.count() == 0:
            return 3
        cu = req_detail.query.filter(req_detail.req_id == req_id).filter(req_detail.is_confirm != 1)
        if cu.count() == 0:
            return 2
        else:
            return 3
        