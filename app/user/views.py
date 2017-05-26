# -*- coding: utf-8 -*-
'''
Created on 2017年3月3日

@author: guxiwen
'''

from flask import *
from app.user import user
from forms import loginForm
from flask_login import login_user, logout_user,login_required
from controllers import UserControllers
from app.common.util import ResultFormat, InfoUtil

@user.route('/test')
def test():
#     cu = UserControllers.verify_password('xixi', '112233')
#     if cu is True:
#         return 'ok'
#     return 'no ok'
    print UserControllers.get_all_group_list()
    return 'ok'

@user.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = UserControllers.verify_password(username, password)
    if user:
        #print load_user(user_id).user_name
        login_user(user,remember=False)
        return redirect(url_for('main.index'))
    else:
        flash('Invalid username or password')
    return 'login failed!'

@user.route('/login',methods=['GET'])
def login_form():
    form = loginForm()
    return render_template('login.html',form=form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out...')
    return redirect(url_for('main.index'))

@user.route('/config-group')
def config_group_handler():
    cuResults = UserControllers.get_all_group()
    data = []
    for group in cuResults:
        tmp = {'group_id':group.group_id,'group_name':group.group_name,'charge_man':group.leader_name,'charge_id':group.leader_id}
        data.append(tmp)
    print data
    return render_template('config-group.html',groups=data)

@user.route('/api/add_group',methods=['Post'])
def add_group_handler():
    group_name = request.form['group_name']
    charge_man = request.form['charge_man']
    leader_id = UserControllers.get_id_by_username(charge_man)
    if leader_id is None:
        result = ResultFormat('','查询不到组长信息','false',InfoUtil.CODE_FAIL).getData() 
        return jsonify(result)
    data = {"leader_id":leader_id,"group_name":group_name,"leader_name":charge_man}
    if UserControllers.add_group( data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@user.route('/api/delete_group',methods=['Post'])
def delete_group_handler():
    group_id = request.form['group_id']
    data = {"is_enable":0}
    if UserControllers.update_group(group_id, data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@user.route('/config-user')
def config_user_handler():
    cuResults = UserControllers.get_all_user()
    leaders = UserControllers.get_all_leaders()
    data = []
    for user in cuResults:
        leader_man = UserControllers.get_username_by_id(user.leader_id)
        tmp = {'username':user.username,'user_type':user.user_type,'user_mail':user.user_mail,'user_id':user.user_id,\
               'create_time':user.create_time,'last_login_time':user.last_login_time,'leader_man':leader_man}
        data.append(tmp)
    return render_template('config-user.html',users=data,leaders=leaders)

@user.route('/api/add_user',methods=['Post'])
def add_user_handler():
    username = request.form['username']
    password = request.form['password']
    leader_man = request.form['leader_man']
    user_mail = request.form['user_mail']
    user_type = request.form['user_type']
    enable = request.form['enable']
    leader_id = UserControllers.get_id_by_username(leader_man)
    if leader_id is None:
        result = ResultFormat('','组长信息不存在','false',InfoUtil.CODE_FAIL).getData()
        return jsonify(result)
    data = {'username':username,'password':password,'leader_id':leader_id,'user_mail':user_mail,'user_type':user_type,\
            'enable':enable}
    if UserControllers.add_user(data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@user.route('/config-req')
def config_req_handler():
    cuResults = UserControllers.get_all_config_detail()
    data = []
    group_list = UserControllers.get_all_group_list()
    user_list = UserControllers.get_all_user_list()
    for req in cuResults:
        tmp_req = req.detail_config
        tmp = {'content':tmp_req.content,'req_type':tmp_req.req_type,'group_id':tmp_req.group_id,'remarks':tmp_req.remarks,'charge_man':tmp_req.charge_man,\
               'is_enable':tmp_req.is_enable,'group_name':req.group_name,'id':tmp_req.id}
        data.append(tmp)
    return render_template('config-req.html',details=data,groups=group_list,users=user_list)

@user.route('/api/add_default_req',methods=['Post'])
def add_default_req_handler():
    content = request.form['content']
    req_type = request.form['req_type']
    group_name = request.form['group_name']
    charge_man = request.form['charge_man']
    remarks =  request.form['remarks']
    is_enable = 1
    group_id = UserControllers.get_group_by_name(group_name)
    if group_id.count() == 0:
        result = ResultFormat('','项目组信息不存在','false',InfoUtil.CODE_FAIL).getData()
        return jsonify(result)
    data = {'content':content,'req_type':req_type,'group_id':group_id.first().group_id,'charge_man':charge_man,'remarks':remarks,'is_enable':is_enable}
    print data
    if UserControllers.add_config_detail(data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)

@user.route('/api/delete_default_req',methods=['Post'])
def delete_default_req_handler():
    detail_id = request.form['id']
    data = {"is_enable":0}
    if UserControllers.update_config_detail(detail_id, data):
        result = ResultFormat('',InfoUtil.MESSAGE_SUCCESS,'true',InfoUtil.CODE_SUCCESS).getData()
    else:
        result = ResultFormat('',InfoUtil.MESSAGE_FAIL,'false',InfoUtil.CODE_FAIL).getData()
    return jsonify(result)





