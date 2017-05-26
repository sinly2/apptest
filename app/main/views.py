# -*- coding: utf-8 -*-
'''
Created on 2017年3月7日

@author: guxiwen
'''

from flask import *
from app.main import main
from app.main.ReqControllers import ReqController
from app.models.user import *
from app.models.requirements import *
from flask_login import login_required, current_user
from app.common.util import ResultFormat, InfoUtil
from app.user.controllers import UserControllers
from app.common.util import DateUtil
import datetime
import random,redis

@main.route('/api/add_req',methods=['post'])
def add_req_handler():
    '''
    parameters:
    req_name 需求名称
    content 需求内容
    version 版本号
    details [{"content":content,"req_type":req_type,"group_id":group_id,remarks":remarks},]
        content:子需求内容, req_type:0, android+ios, 1 android, 2 ios, remarks:备注
    remarks 备注
    
    '''
    req_name = request.form['req_name']
    version = request.form['version']
    preUplineDate = request.form['preUplineDate']
    is_force = request.form['is_force']
#     details = [{'content':u'微商icon去除','req_type':0,'group_id':1,'remarks':'12345'},\
#                {'content':u'首页改版abc','req_type':1,'group_id':1,'remarks':'54321'}]
    remarks = request.form['remarks']
    data = {'req_name':req_name,'is_force':is_force,'version':version,'preUplineDate':preUplineDate,'remarks':remarks,\
            'user_id':current_user.get_id()}
    req_id = ReqController.add_req(data)
    if req_id:
        detail_flag = ReqController.add_default_detail(req_id)
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'true',InfoUtil.CODE_FAIL).getData()
        return jsonify(result)
    if detail_flag:
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
        return jsonify(result)
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'true',InfoUtil.CODE_FAIL).getData()
        return jsonify(result)

@main.route('/test')
def test():
    details = [{'content':u'微商icon去除','req_type':0,'group_id':1,'remarks':'12345'},\
               {'content':u'首页改版abc','req_type':1,'group_id':1,'remarks':'54321'}]
    data = {'req_name':'abcdefg','content':'haha','version':'V3.3.2','details':details,'remarks':'bbs','user_id':'1001'}
    if ReqController.add_req(data):
        return 'ok'
    else:
        return 'no ok'

@main.route('/RequirementsList.html')
def get_list_handler():
    pass

@main.route('/api/getRequirements',methods=['post','get'])
def get_req_list_handler():
    if request.method == 'GET':
        version = request.args.get('version')
    else:
        version = request.form['version']
    #version = request.args.get('version')
    try:
        cuResult = ReqController.get_req_list(version)
        if cuResult is None:
            result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
        else:
            tmp = []
            for req in cuResult:
                pre_upline_date = datetime.datetime.strftime(req.pre_upline_date,'%Y-%m-%d')
                tmp.append({'req_name':req.req_name,'raise_man':req.raise_man,'version':req.version,'status':req.status,'remarks':req.remarks\
                            ,'raise_time':req.raise_time,'is_force':req.is_force,'pre_upline_date':pre_upline_date,'req_id':req.req_id,\
                            'upline_time':req.upline_time if req.upline_time is not None else '',})
            result = ResultFormat(tmp,InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    except Exception,e:
        print e
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@main.route('/Requirements')
def req_index():
    result = []
    cuResult = ReqController.get_req_list('')
    for req in cuResult:
        #pre_upline_date = datetime.datetime.strftime(req.pre_upline_date,'%Y-%m-%d')
        result.append({'req_name':req.req_name,'create_man':req.create_man,'version':req.version,'status':req.status,'remarks':req.remarks\
                            ,'raise_test_date':req.raise_test_date,'is_force':req.is_force,'pre_upline_date':req.pre_upline_date,'req_id':req.req_id,\
                            'upline_date':req.upline_date if req.upline_date is not None else '','raise_audit_date':req.raise_audit_date if req.raise_audit_date is not None else '',\
                            'raise_test_date':req.raise_test_date if req.raise_test_date is not None else ''})
    return render_template('requirements.html',reqs=result)

@main.route('/Requirements/edit')
def req_edit_handler():
    req_id = request.args.get('req_id')
    cuResult = ReqController.get_req_by_id(req_id)
    req =  cuResult[0]
    result = {'req_name':req.req_name,'version':req.version,'is_force':req.is_force,'pre_upline_date':req.pre_upline_date,'remarks':req.remarks}
    return render_template('requirement_edit.html',req=result)

@main.route('/Requirements/<req_id>')
def req_detail_handler(req_id):
    cuResult = ReqController.get_req_detail(req_id)
    req_name = ReqController.get_req_name_by_id(req_id)[0].req_name
    result = []
    if cuResult.count() == 0:
        return render_template('reqdetail.html',req_name=req_name,result=result)
    else:
        pre_upline_date = ReqController.get_req_by_id(req_id)[0].pre_upline_date
        for cu in cuResult:
            detail = cu.req_detail
            result.append({'detail_id':detail.detail_id,'content':detail.content,'req_type':detail.req_type,'group_id':detail.group_id,\
                        'is_confirm':detail.is_confirm,'remarks':detail.remarks,'req_type':detail.req_type,'charge_man':detail.charge_man,\
                          'pre_upline_date':pre_upline_date if pre_upline_date is not None else '','group_name':cu.group_name})    
        return render_template('reqdetail.html',req_name=req_name,result=result)
        
@main.route('/api/updateDetail',methods=['POST'])
def update_detail_handler():
    content = request.form['content']
    req_type = request.form['req_type']
    group_id = request.form['group_id']
    charge_man = request.form['charge_man']
    remarks = request.form['remarks']
    detail_id = request.form['detail_id']
    #req_id = request.form['req_id']
    operate_id = current_user.get_id()
    operate_man = UserControllers.get_username_by_id(operate_id) if operate_id is not None else None
    param_list = ['content','req_type','group_id','charge_man','remarks','detail_id']
    data = {}
    if detail_id is None or detail_id == '':
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
        return jsonify(result)
    for param in param_list:
        if param is None:
            continue
        else:
            data[param] = eval(param)
    if ReqController.update_detail(detail_id, data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@main.route('/api/addDetail',methods=['POST'])
def add_detail_handler():
    req_id = request.form['req_id']
    content = request.form['content']
    req_type = request.form['req_type']
    group_id = request.form['group_id']
    charge_man = request.form['charge_man']
    remarks = request.form['remarks']
    operate_id = current_user.get_id()
    operate_man = UserControllers.get_username_by_id(operate_id) if operate_id is not None else ''
    param_list = ['req_id','content','req_type','group_id','charge_man','remarks','operate_man','operate_id']
    data = {}
    for param in param_list:
        if param is None:
            continue
        else:
            data[param] = eval(param)
    if ReqController.add_detail(data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@main.route('/api/updateRequirement')
def update_requirement_handler():
    pass

@main.route('/api/uplineChildRequirement',methods=['POST'])
def upline_childrequirement_handler():
    detail_id = request.form['detail_id']
    action = request.form['action']
    is_confirm = 1 if action == 'upline' else 0
    operate_id = current_user.get_id()
    operate_man = UserControllers.get_username_by_id(operate_id) if operate_id is not None else ''
    data = {"operate_id":operate_id,"operate_man":operate_man,"is_confirm":is_confirm}
    if ReqController.update_detail(detail_id, data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@main.route('/api/uplineRequirement',methods=['POST'])
def upline_requirement_handler():
    req_id = request.form['req_id']
    action = request.form['action']
    check_status = ReqController.upline_check(req_id)
    data = {"req_id":req_id}
    now_date = DateUtil.get_now_date(1,"%Y-%m-%d")
    if check_status == 1:
        result = ResultFormat('','需求不存在！','false',InfoUtil.CODE_FAIL).getData()
        return jsonify(result)
    if action == 'overdevelopment':
        status = 1
        data["raise_test_date"] = now_date
    elif action == 'overtest':
        if check_status == 2:
            result = ResultFormat('','有子需求尚未测试完毕！','false',InfoUtil.CODE_FAIL).getData()
            return jsonify(result)
        status = 2
        data["raise_audit_date"] = now_date
    elif action == 'overaudit':
        status = 3
    elif action == 'auditback':
        status = 1
    elif action == 'upline':
        status = 4
        data["upline_date"] = now_date
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
        return jsonify(result)
    operate_id = current_user.get_id()
    operate_man = UserControllers.get_username_by_id(operate_id) if operate_id is not None else ''    
    data["status"] = status
    if ReqController.update_requirement(req_id, data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)
    
@main.route('/index')
def index():
    return render_template('add_req.html')

@main.route('/222')
def test222():
    return render_template('test.html')

@main.route('/getData',methods=['POST'])
def get_data():
    r = redis.Redis(host="192.168.130.35",port=6379,db=1)
    y = r.get('7.3')
    y = round(float(y),2)
    result = {"y":y}
    return jsonify(result)

@main.route('/configCenter')
def config_center_handler():
    return 'ok'