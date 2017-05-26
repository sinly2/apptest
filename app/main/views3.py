# -*- coding: utf-8 -*-
'''
Created on Sep 29, 2016

@author: guxiwen
'''
import datetime
import time

from flask import *
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from app.user.controllers import UserControllers
from app.config import Util, Message
from app.main import main
from app.models import *
#from app.models.user import *
from controllers import reqController
from app.main.controllers import dataController


@main.route('/index')
def index():
    basic = {"user_name":u"游客"}
    if current_user.get_id() is not None:
        username = reqController.get_userinfo_by_id(current_user.get_id()).user_name
        basic["user_name"] = username
    return render_template('index.html',basic=basic)

@main.route('/addUser',methods=['get'])
@login_required
def add_user():
    username = request.args.get('username')
    user_type = request.args.get('t')
    password = request.args.get('password')
    mail = request.args.get('mail')
    utype = UserControllers.get_user_info_id(current_user.get_id())
    if utype is None or utype.user_type <> 1:
        #1管理员2普通人员，做的好应该把权限提取出来，通过配置维护
        return u"你没有权限"
    if mail is None:
        mail = username + "@qbao.com"
    if user_type is None:
        user_type = 2
    user = user_info(user_name=username,user_type=user_type,password=password,user_mail=mail)
    try:
        a = db.session.add(user)
        b = db.session.commit()
    except IntegrityError,e:
        print e
        return u"用户%s已存在！请重新输入不同的用户名" %(username)  
    
    return u"用户%s创建成功!" %(username)

@main.route('/getUser')
def get_user():
    return current_user.get_id()

@main.route('/test')
def test():
    if  reqController.get_req_by_id(15) is None:
        print request.args.viewkeys()
        return '2'
    else:
        return "1"

@main.route('/assignReq',methods=['post','get'])
# @login_required
def assign_req():
    req_id = '1'
    aim_id = '1'
    if req_id is None:
        return jsonify({"code":"1001","message":Message.MESSAGE_EOR,"data":None})
    req = reqController.get_req_by_id(req_id)
    if req is None:
        return jsonify({"code":"1001","message":"该需求不存在","data":None})
    elif req.status == 3:
        return jsonify({"code":"1001","message":"该需求已上线，无法再次分配","data":None})
    else:
        tmp = req.test_man_id
    #判断是否重复分配
    if tmp is not None:
        if tmp == aim_id:
            return jsonify({"code":"1001","message":"该用户已分配，无需再次分配","data":None})
        else:
            lis_tmp = tmp.split(",")
            for i in lis_tmp:
                if i == aim_id:
                    return jsonify({"code":"1001","message":"该用户已分配，无需再次分配","data":None})
        aim_id = tmp + ',' + aim_id 
    his_assign = req_assign(assign_man_id = current_user.get_id(),assigned_man_id = req_id)
    dic = {"test_man_id":aim_id,"status":2}
    if reqController.assign_req_sql(req_id, dic, his_assign):
        return jsonify({"code":"1000","message":Message.MESSAGE_SUC,"data":None})
    else:
        return jsonify({"code":"1001","message":"分配失败","data":None})
    
@main.route('/upline',methods=['POST'])
@login_required
def upline():
    req_id = request.form['req_id']
    now_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    now_date = datetime.datetime.strptime(now_date,'%Y-%m-%d').date()
    if req_id is None:
        return jsonify({"code":"1001","message":Message.MESSAGE_EOR,"data":None})
    req = reqController.get_req_by_id(req_id)
    if req is None:
        return jsonify({"code":"1001","message":"该需求不存在","data":None})
    elif req.status == 3:
        return jsonify({"code":"1001","message":"该需求已上线，无法再次上线","data":None})
    dic = {"status":3,"upline_date":now_date}
    if reqController.upline_sql(req_id, dic):
        return jsonify({"code":"1000","message":Message.MESSAGE_SUC,"data":None})
    else:
        return jsonify({"code":"1001","message":Message.MESSAGE_EOR,"data":None})

@main.route('/claim',methods=['POST'])
@login_required
def claim(): 
#     req_id = request.args.get('req_id')
    req_id = request.form['req_id']
    aim_id = current_user.get_id()
    now_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    now_date = datetime.datetime.strptime(now_date,'%Y-%m-%d').date()
    if req_id is None:
        return jsonify({"code":"1001","message":Message.MESSAGE_EOR,"data":None})
    req = reqController.get_req_by_id(req_id)
    if req is None:
        return jsonify({"code":"1001","message":"该需求不存在","data":None})
    elif req.status == 3:
        return jsonify({"code":"1001","message":"该需求已上线，无法认领","data":None})
    else:
        tmp = req.test_man_id
    #判断是否重复分配
    if tmp is not None:
        if tmp == aim_id:
            return jsonify({"code":"1001","message":"您已认领该任务，无需重复认领","data":None})
        else:
            lis_tmp = tmp.split(",")
            for i in lis_tmp:
                if i == aim_id:
                    return jsonify({"code":"1001","message":"您已认领该任务，无需再次认领","data":None})
        aim_id = tmp + ',' + aim_id
    #判断是否有人认领，首次认领需要 
    dic = {"test_man_id":aim_id,"status":2,"start_date":now_date}
    if reqController.claim_sql(req_id, dic):
        return jsonify({"code":"1000","message":Message.MESSAGE_SUC,"data":None})
    else:
        return jsonify({"code":"1001","message":Message.MESSAGE_EOR,"data":None})

@main.route('/getMyReq',methods=['GET'])
@login_required
def get_my_req():
    reqs = reqController.get_req_by_user_id(current_user.get_id())
    result = []
    pageSize = 10 if request.args.get("pageSize") is None else int(request.args.get("pageSize"))
    pageNum = 1 if request.args.get("pageNum") is None else int(request.args.get("pageNum"))
    basic = {"status":"","raise_man":"","test_man":"","raise_date":"","upline_date":"","count_upline":0,"count_testing":0,\
             "user_name":u"游客","start_date":""}
    if reqs is None:
        return None
    
    #分页算法    
    reqs,totalNum = reqController.dliver_page(reqs, pageSize, pageNum)
    basic["totalNum"] = totalNum
    basic["pageNum"] = pageNum
    for req in reqs:
        tmp = {}
        tmp["id"] =  req.req_id
        tmp["name"] = req.name
        tmp["raise_man"] = req.raise_man
        tmp["raise_date"] = req.raise_date
        tmp["start_date"] = req.start_date
        tmp["status"] = req.status
        tmp["test_man"] = ''
        tmp["upline_date"] = req.upline_date
        for user_id in req.test_man_id.split(","):
            if user_id is None or user_id == '':
                continue
            user_name = reqController.get_userinfo_by_id(user_id).user_name
            tmp["test_man"] = tmp["test_man"] + user_name + ","
        tmp = reqController.data_transfer(tmp)
        result.append(tmp)
    if current_user.get_id() is not None:
        username = reqController.get_userinfo_by_id(current_user.get_id()).user_name
        basic["user_name"] = username
    return render_template('myreq.html',basic=basic,result=result)

@main.route('/getAllReq')
def get_all_req():
    result = []
    pageSize = 10 if request.args.get("pageSize") is None else int(request.args.get("pageSize"))
    pageNum = 1 if request.args.get("pageNum") is None else int(request.args.get("pageNum"))
    basic = {"status":"","raise_man":"","test_man":"","raise_date":"","upline_date":"","count_upline":0,"count_testing":0,\
             "user_name":u"游客","start_date":"","is_claimed":""}
    if len(request.args.lists()) == 0:
        reqs = reqController.get_reqs()            
    else:
        basic["status"] = request.args.get("status")
        basic["raise_man"] = request.args.get("raise_man")
        basic["test_man"] = request.args.get("test_man")
        basic["raise_date"] = request.args.get("raise_date")
        basic["upline_date"] = request.args.get("upline_date")
        
        reqs = reqController.all_req_filter(basic["status"], basic["raise_man"], basic["test_man"],\
                                                   basic["raise_date"], basic["upline_date"])
    #分页算法    
    reqs,totalNum = reqController.dliver_page(reqs, pageSize, pageNum)
    basic["totalNum"] = totalNum
    basic["pageNum"] = pageNum
        
    for req in reqs:
        tmp = {}
        tmp["id"] =  req.req_id
        tmp["name"] = req.name
        tmp["raise_man"] = req.raise_man
        tmp["raise_date"] = req.raise_date
        tmp["start_date"] = req.start_date
        tmp["status"] = req.status
        tmp["test_man"] = ''
        tmp["upline_date"] = req.upline_date
        if req.test_man_id is not None and req.test_man_id <> '':
            for user_id in req.test_man_id.split(","):
                if user_id is None or user_id == '':
                    continue
                if user_id == current_user.get_id():
                    tmp["is_claimed"] = 1
                user_name = reqController.get_userinfo_by_id(user_id).user_name
                tmp["test_man"] = tmp["test_man"] + user_name + ","
        tmp = reqController.data_transfer(tmp)
        result.append(tmp)
    if current_user.get_id() is not None:
        username = reqController.get_userinfo_by_id(current_user.get_id()).user_name
        basic["user_name"] = username
    return render_template('allreq.html',basic=basic,result=result)

@main.route('/datalist')
def datalist():
    result = []
    basic = {"status":"","raise_man":"","test_man":"","raise_date":"","upline_date":"","count_upline":0,"count_testing":0,\
             "user_name":u"游客","start_date":""}
    today =  datetime.date.today()
    #统计上周
#     last_sunday = today + datetime.timedelta(-1 - today.weekday())
#     last_monday = today + datetime.timedelta(-7 - today.weekday())
    #统计本周
    last_sunday = today + datetime.timedelta(6 - today.weekday())
    last_monday = today + datetime.timedelta(0 - today.weekday())
    reqs = dataController.week_count(last_monday,last_sunday)
    for req in reqs:
        tmp = {}
        tmp["id"] =  req.req_id
        tmp["name"] = req.name
        tmp["raise_man"] = req.raise_man
        tmp["raise_date"] = req.raise_date
        tmp["start_date"] = req.start_date
        tmp["status"] = req.status
        if req.status == 2:
            basic["count_testing"] = basic["count_testing"] + 1
        elif req.status == 3:
            basic["count_upline"] = basic["count_upline"] + 1
        tmp["test_man"] = ''
        tmp["upline_date"] = req.upline_date
        if req.test_man_id is not None and req.test_man_id <> '':
            for user_id in req.test_man_id.split(","):
                if user_id is None or user_id == '':
                    continue
                user_name = reqController.get_userinfo_by_id(user_id).user_name
                tmp["test_man"] = tmp["test_man"] + user_name + ","
        tmp = reqController.data_transfer(tmp)
        result.append(tmp)
    if current_user.get_id() is not None:
        username = reqController.get_userinfo_by_id(current_user.get_id()).user_name
        basic["user_name"] = username
    return render_template('datalist.html',basic=basic,result=result)

@main.route('/test2')    
def test2():
    result = [{"name":u"需求2.9","raise_man":"wulei","raise_date":"2016-10-05","test_man":"guxiwen","status":"2"}\
              ,{"name":u"需求2.9","raise_man":"wulei","raise_date":"2016-10-05","test_man":"guxiwen","status":"1"}\
              ,{"name":u"需求2.9","raise_man":"wulei","raise_date":"2016-10-05","test_man":"guxiwen","status":"3"}]
    return render_template('user.html',name='123',result=result)

@main.route('/test3')
def test3():
    basic = {"status":"","raise_man":"","test_man":"","raise_date":"","upline_date":"","count_upline":0,"count_testing":0,\
             "user_name":u"游客","start_date":""}
    return render_template('reqdetail.html',basic=basic)