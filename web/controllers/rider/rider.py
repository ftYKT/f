# -*- coding: utf-8 -*-
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination,getCurrentDate
from common.libs.UrlManager import UrlManager
from common.models.rider.rider import Rider
from sqlalchemy import  or_
from application import app, db

# from flask import Blueprint,request,redirect,jsonify
# from common.libs.Helper import ops_render,iPagination,getCurrentDate,getDictFilterField,selectFilterObj
# from common.libs.UrlManager import UrlManager
# from common.models.rider.rider import Rider
# from sqlalchemy import  or_
# from common.models.member.MemberComments import MemberComments
# from common.models.food.Food import Food
# from common.models.pay.PayOrder import PayOrder
# from application import app,db

route_rider = Blueprint( 'rider_page', __name__ )

@route_rider.route("/index",methods = [ "GET","POST" ])
def index():
    resp_data = {}
    req = request.values
    page = int( req['p'] ) if ( 'p' in req and req['p'] ) else 1
    query = Rider.query

    if 'mix_kw' in req:
        rule = or_( Rider.nickname.ilike( "%{0}%".format( req['mix_kw'] ) ),Rider.mobile.ilike( "%{0}%".format( req['mix_kw'] ) ) )
        query = query.filter( rule )



    page_params = {
        'total': query.count(),
        'page_size':app.config['PAGE_SIZE'],
        'page': page,
        'display':app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace( "&p={}".format(page),"" )
    }

    pages = iPagination( page_params )
    offset = ( page - 1 ) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    id = int(req.get("id", 0))
    list = Rider.query.order_by( Rider.rid.desc() ).all()[ offset:limit ]
    # list = Rider.query.filter_by( uid = uid ).all()[ offset:limit ]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render( "rider/index.html",resp_data )


@route_rider.route( "/info" )
def info():
    resp_data = {}
    req = request.args
    rid = int( req.get('id',0 ))
    reback_url = UrlManager.buildUrl("/rider/index")
    if rid < 1:
        return redirect( reback_url )

    info = Rider.query.filter_by( rid = rid ).first()
    if not info:
        return redirect( reback_url )

    resp_data['info'] = info

    return ops_render( "rider/info.html",resp_data )


@route_rider.route( "/set",methods = [ "GET","POST" ] )
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int( req.get( "id",0 ) )
        info = None
        if uid :
            info = Rider.query.filter_by( uid = uid ).first()
        resp_data['info'] = info
        return ops_render( "rider/set.html",resp_data )

    resp = { 'code':200,'msg':'操作成功~~','data':{} }
    req = request.values

    rid = req['rid'] if 'rid' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    adarea = req['adarea'] if 'adarea' in req else ''

    if nickname is None or len( nickname ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify( resp )

    if mobile is None or len( mobile ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~"
        return jsonify( resp )

    has_in = Rider.query.filter( Rider.rid == rid ).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该rid已存在，请换一个试试~~"
        return jsonify(resp)

    rider_info = Rider.query.filter_by( rid = rid ).first()
    if rider_info:
        model_rider = rider_info
    else:
        model_rider = Rider()

    model_rider.rid = rid
    model_rider.nickname = nickname
    model_rider.mobile = mobile
    model_rider.adarea = adarea

    db.session.add( model_rider )
    db.session.commit()
    return jsonify(resp)


@route_rider.route("/ops",methods = [ "POST" ])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id :
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in [ 'remove','recover' ] :
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    user_info = Rider.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在~~"
        return jsonify(resp)

    if act == "remove":
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    if user_info and user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "该用户是演示账号，不准操作账号~~"
        return jsonify(resp)

    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)



