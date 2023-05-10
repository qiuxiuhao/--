from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
import os
import send
import code
import time
import database_operate

# 创建Flask服务
app = Flask(__name__)
CORS(app)


# 访问URL：http://127.0.0.1:8080/home/hello
# 返回结果：{"data":"welcome to use flask.","msg":"hello"}

# 手机号登入
@app.route('/login')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def login():  # 名字最好与访问路径同名
    phonenumber1 = str(request.args.get('phonenumber'))  # 获取uni.request所提交的data
    password1 = str(request.args.get('password'))  # 获取uni.request所提交的data
    n = database_operate.OpDB()
    mydata = ''
    mydata1 = ''
    userid = ''
    contrast = False
    if n.exist_phonenumber(phonenumber1):
        userid = n.get_userid(phonenumber1)
        if password1 == n.get_password(userid):
            contrast = True
    if contrast:
        z = database_operate.OpDB()
        data = z.get_userinfo(userid)
        l = database_operate.OpDB()
        data1 = l.get_payinfo(userid)
        mydata = dict(zip(("id", "password", "phonenumber", "gender", "school", "name", "autograph", "avatar"), data))
        mydata1 = dict(zip(("payword", "no_secret"), data1))

    return {'contrast': contrast,
            'userinfo': mydata,
            'pay': mydata1
            }  # 以json格式返回数据


# 创建新用户
@app.route('/userinfoset')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def userinfoset():
    name = str(request.args.get('name'))
    phonenumber = str(request.args.get('phonenumber'))
    password = str(request.args.get('password'))
    gender = str(request.args.get('gender'))
    school = str(request.args.get('school'))
    pay_password = str(request.args.get('pay_password'))
    avatar = str(request.args.get('avatar'))
    m = database_operate.OpDB()
    userid = m.create_user(phonenumber, password, school, gender, name, int(pay_password), avatar)
    data = (userid, name, phonenumber, password, gender, school, pay_password, avatar)
    print(data)
    mydata = dict(zip(("id", "name", "phonenumber", "password", "gender", "school", "pay_password", "avatar"), data))
    return {
        'userinfo': mydata
    }


# 获取学校名
@app.route('/schoolinfo')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def schoolinfo():
    m = database_operate.OpDB()
    data = m.get_school()
    return {'schoolname': data}


# 获取余额
@app.route('/balanceinfo')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def balanceinfo():
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    data = m.get_payment(userid)
    return {'balance': data}


# 获取信息
@app.route('/lossinfo')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def lossinfo():
    school = str(request.args.get('school'))
    typename = str(request.args.get('type'))
    m = database_operate.OpDB()
    if typename == '二手':
        data = m.get_commodity(school)
    elif typename == '失物招领':
        data = m.get_loss(school)
    else:
        data = m.get_commission(school)
    mydata = [dict(zip(("id", "date", "name", "type", "avatar"), x)) for x in data]
    return jsonify(mydata)


# 根据id查找失物招领信息
@app.route('/loss_id')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def loss_id():
    lossid = str(request.args.get('id'))
    m = database_operate.OpDB()
    data = m.get_lossinfo(lossid)
    # print(data)
    mydata = dict(zip(("lossId", "userId", "date", "name", "school", "avatar", "detail", "state", "type", "time",
                       "address"), data))
    return mydata


# 根据id查找二手商品信息
@app.route('/commodity_id')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def commodity_id():
    commodityid = str(request.args.get('id'))
    m = database_operate.OpDB()
    data = m.get_commodityinfo(commodityid)
    mydata = dict(zip(("commodityId", "userId", "date", "commodityName", "school", "price", "avatar", "detail", "state",
                       "type"), data))
    return mydata


# 根据id查找代办商品信息
@app.route('/commission_id')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def commission_id():
    commissionid = str(request.args.get('id'))
    m = database_operate.OpDB()
    data = m.get_commissioninfo(commissionid)
    mydata = dict(zip(("commissionId", "userId", "date", "name", "school", "price", "avatar", "detail", "state", "type")
                      , data))
    return mydata


# 我的订单
@app.route('/myorder')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def myorder():
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    # userid = "10001020"
    data1 = m.get_commodity_order(userid)
    data2 = m.get_commission_order(userid)
    data3 = m.get_commission_order1(userid)
    data4 = m.get_commodity_order1(userid)
    for i in data2:
        data1 = data1 + ((i),)
    for i in data3:
        data1 = data1 + ((i),)
    for i in data4:
        data1 = data1 + ((i),)

    mydata = [dict(zip(("Id", "orderId", "date", "status", "name", "type", "avatar")
                       , x)) for x in data1]
    # print(mydata)
    return mydata


# 我的发布
@app.route('/myrelease')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def myrelease():
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    # userid = "10001020"
    data1 = m.get_loss_order(userid)
    data2 = m.get_commodity_(userid)
    data3 = m.get_commission_(userid)
    for i in data2:
        data1 = data1 + ((i),)
    for i in data3:
        data1 = data1 + ((i),)

    mydata = [dict(zip(("good_id", "date", "name", "type", "status", "avatar")
                       , x)) for x in data1]
    # print(mydata)
    return mydata


# 加入收藏
@app.route('/create_favorite')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def create_favorite():
    userid = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    goodid = str(request.args.get('goodid'))
    avatar = str(request.args.get('avatar'))
    m = database_operate.OpDB()
    m.create_favorite(userid, typename, goodid, avatar)
    return {
        'f': 'true'
    }


# 收藏判定
@app.route('/is_favorite')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def is_favorite():
    userid = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    # print(typename)
    goodid = str(request.args.get('goodid'))
    m = database_operate.OpDB()
    mm = False
    mm = m.is_favorite(userid, goodid, typename)
    if mm:
        return {
            'f': True
        }
    else:
        return {
            'f': False
        }


# 获取收藏信息
@app.route('/get_favorite')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def get_favorite():
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    data = m.get_favorite(userid)
    # print(data)
    mydata = [dict(zip(("id", "data", "name", "type", "avatar")
                       , x)) for x in data]
    return mydata


# 取消收藏
@app.route('/del_favorite')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def del_favorite():
    userid = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    goodid = str(request.args.get('goodid'))
    m = database_operate.OpDB()
    m.delete_favorite(userid, goodid, typename)
    return {
        'f': 'true'
    }


# 查询对应代办订单id的订单信息（含评价信息)
@app.route('/get_daiban')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def get_daiban():
    oderid = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    # print(oderid)
    m = database_operate.OpDB()
    data1 = (False, "NULL")
    data2 = (True,)
    if typename == '代办':
        data = m.get_daibaninfo(oderid)
        # print(type(data[5]))
        if data[5] is not None:
            data2 = data2 + m.get_commentinfo(data[5])
            data1 = data2
        # print(data1)
        mydata = dict(
            zip(("good_id", "userid_to", "status", "creatime", "finishtime", "cmmmentid", "userid_from", "name",
                 "price", "userphone_from", "user_from", "userphone_to", "user_to"), data))

        comment = dict(zip(("exist", "content"), data1))
    elif typename == "二手":
        data = m.get_shoppinginfo(oderid)
        if data[5] is not None:
            data2 = data2 + m.get_commentinfo(data[5])
            data1 = data2
        mydata = dict(
            zip(("good_id", "userid_to", "status", "creatime", "finishtime", "cmmmentid", "address", "userid_from",
                 "name", "price", "userphone_from", "user_from", "userphone_to", "user_to"), data))

        comment = dict(zip(("exist", "content"), data1))
    else:
        data = m.get_lossorder(oderid)
        mydata = dict(zip(("good_id", "userid", "creatime", "name", "status", "finishtime",
                           "userphone_from", "user_from"), data))
    return {
        "order": mydata,
        "evaluate": comment
    }


# 确认完成代办和购物订单
@app.route('/commit_daibanorder')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def commit_daibanorder():
    orderid = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    m = database_operate.OpDB()
    if typename == "代办":
        m.commit_daibanorder(orderid)
    else:
        m.commit_shoppingorder(orderid)
    return {
        'f': True
    }


# 取消代办和购物订单
@app.route('/cancel_daibanorder')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def cancel_daibanorder():
    orderid = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    m = database_operate.OpDB()
    if typename == "代办":
        m.cancel_daibanorder(orderid)
    else:
        m.cancel_shoppingorder(orderid)
    return {
        'f': True
    }


# 确认完成失物招领
@app.route('/commit_lossorder')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def commit_lossorder():
    orderid = str(request.args.get('id'))
    m = database_operate.OpDB()
    m.commit_lossorder(orderid)
    return {
        'f': 'true'
    }


# 确认取消失物招领
@app.route('/delete_loss')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def delete_loss():
    goodid = str(request.args.get('good_id'))
    m = database_operate.OpDB()
    m.delete_loss(goodid)
    return {
        'f': True
    }


# 确认取消商品
@app.route('/delete_commodity')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def delete_commodity():
    goodid = str(request.args.get('good_id'))
    m = database_operate.OpDB()
    m.delete_commodity(goodid)
    return {
        'f': 'true'
    }


# 确认取消代办
@app.route('/delete_commission')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def delete_commission():
    goodid = str(request.args.get('good_id'))
    m = database_operate.OpDB()
    m.delete_commission(goodid)
    return {
        'f': 'true'
    }


# 根据id查找交易信息
@app.route('/get_trade')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def get_trade():
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    data = m.get_trade(userid)
    mydata = [dict(zip(("type", "tradeMoney", "date", "remarks")
                       , x)) for x in data]
    return mydata


# 根据id查找聊天信息
@app.route('/get_user')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def get_user():
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    data = m.get_user(userid)
    mydata = dict(zip(("id", "name", "avatar")
                      , data))
    return mydata


# 返回最新发布
@app.route('/get_new_')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def get_new_():
    name = str(request.args.get('school'))
    print(name)
    m = database_operate.OpDB()
    data = m.get_new_(name)
    print(data)
    commission = dict(
        zip(("commissionId", "date", "name", "type", "state", "avatar", "userId", "price", "detail", "school")
            , data[0]))
    commodity = dict(
        zip(("ccommodityId", "date", "name", "type", "state", "avatar", "userId", "price", "detail", "school")
            , data[1]))
    loss = dict(
        zip(("commissionId", "date", "name", "type", "state", "avatar", "userId", "address", "detail", "school")
            , data[2]))
    return {
        "commission": commission,
        "commodity": commodity,
        "loss": loss
    }


# 发布评价
@app.route('/create_comment')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def create_comment():
    id = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    detail = str(request.args.get('detail'))
    m = database_operate.OpDB()
    m.create_comment(detail, typename, id)
    return {
        'f': 'true'
    }


# 发布失物招领
@app.route('/create_loss')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def create_loss():
    userid = str(request.args.get('id'))
    typename = str(request.args.get('type'))
    name = str(request.args.get('name'))
    address = str(request.args.get('address'))
    detail = str(request.args.get('detail'))
    school = str(request.args.get('school'))
    avatar = str(request.args.get('avatar'))
    m = database_operate.OpDB()
    n = m.create_lossinfo(userid, typename, name, address, detail, school, avatar)
    return {
        'f': n
    }


# 发布二手商品
@app.route('/create_commodity')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def create_commodity():
    userid = str(request.args.get('id'))
    name = str(request.args.get('name'))
    price = str(request.args.get('price'))
    detail = str(request.args.get('detail'))
    school = str(request.args.get('school'))
    avatar = str(request.args.get('avatar'))
    m = database_operate.OpDB()
    m.create_commodityinfo(userid, school, name, detail, price, avatar)
    return {
        'f': 'true'
    }


# 发布代办
@app.route('/create_commission')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def create_commission():
    userid = str(request.args.get('id'))
    name = str(request.args.get('name'))
    price = str(request.args.get('price'))
    detail = str(request.args.get('detail'))
    school = str(request.args.get('school'))
    m = database_operate.OpDB()
    balance = m.get_payment(userid)
    if float(price) > balance:
        return {
            'f': 'false'
        }
    else:
        m.create_commissioninfo(userid, school, name, detail, price)
        return {
            'f': 'true'
        }


# 生成购买订单
@app.route('/create_shopping')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def create_shopping():
    userid = str(request.args.get('user_id'))
    address = str(request.args.get('address'))
    commodity = str(request.args.get('good_id'))
    m = database_operate.OpDB()
    n = m.create_shopping(userid, address, commodity)
    print(n)
    return {
        'f': n
    }


# 生成代办订单
@app.route('/create_daiban')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def create_daiban():
    userid = str(request.args.get('id'))
    commission = str(request.args.get('good_id'))
    m = database_operate.OpDB()
    n = m.create_daiban(userid, commission)
    if n:
        return {
            'f': True
        }
    else:
        return {
            'f': False
        }


# 修改用户信息
@app.route('/submitinfo')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def submitinfo():
    name = str(request.args.get('name'))
    # phonenumber = str(request.args.get('phonenumber'))
    # password = str(request.args.get('password'))
    gender = str(request.args.get('gender'))
    school = str(request.args.get('school'))
    userid = str(request.args.get('id'))
    autograph = str(request.args.get('autograph'))
    avatar = str(request.args.get('avatar'))
    m = database_operate.OpDB()
    # m.change_info1('password', password, userid)
    # m.change_info1('phone', phonenumber, userid)
    m.change_info1('schoolName', school, userid)
    m.change_info1('gender', gender, userid)
    m.change_info2('name', name, userid)
    m.change_info2('autograph', autograph, userid)
    m.change_info2('avatar', avatar, userid)
    return {
        'f': 'true'
    }


# 修改免密支付
@app.route('/nopayset')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def nopayset():
    no_secret = str(request.args.get('no_secret'))
    userid = str(request.args.get('id'))
    if no_secret == "false":
        no_secret = "0"
    else:
        no_secret = "1"
    m = database_operate.OpDB()
    m.change_payment('nopayCode', no_secret, userid)
    return {
        'f': 'true'
    }


# 修改支付密码
@app.route('/payset')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def payset():
    payword_new1 = str(request.args.get('payword'))
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    m.change_payment('payCode', payword_new1, userid)
    return {
        'f': 'true'
    }


# 修改支付密码
@app.route('/passwordset')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def passwordset():
    password = str(request.args.get('password'))
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    m.change_info1('password', password, userid)
    return {
        'f': 'true'
    }


# 修改手机号
@app.route('/phonenumberset')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def phonenumberset():
    phonenumber = str(request.args.get('phonenumber'))
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    m.change_info1('phone', phonenumber, userid)
    return {
        'f': 'true'
    }


# 发送验证码
@app.route('/captcha')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def captcha():
    m = code.code()
    cd = str({"code": m})
    number = str(request.args.get('phonenumber'))
    send.senMessage(number, cd)
    print(m)
    return {'captcha': m}


@app.route('/exist')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def exist():
    number = str(request.args.get('phonenumber'))
    is_newuser = database_operate.OpDB()
    exist1 = str(is_newuser.exist_phonenumber(number))
    # exist1 = '123456'
    print(exist1)
    return {'exist': exist1}


@app.route('/register')  # 访问路径,需要与hbuilder对应页面的url的.com之后的一致
def register():
    m = database_operate.OpDB()
    number = str(request.args.get('phonenumber'))
    userid = str(m.get_userid(number))

    n = database_operate.OpDB()
    data = n.get_userinfo(userid)

    l = database_operate.OpDB()
    data1 = l.get_payinfo(userid)
    mydata = dict(zip(("id", "password", "phonenumber", "gender", "school", "name", "autograph", "avatar"), data))
    mydata1 = dict(zip(("payword", "no_secret"), data1))

    return {
        'userinfo': mydata,
        'pay': mydata1
    }


# 上传图片
@app.route('/upload', methods=['GET', 'POST'])
def uploads():
    img = request.files.get('image')
    name = request.form.get('names')
    name = str(name) + str(int(time.time())) + '.png'
    img.save(os.path.join('image', name))
    name = 'https://www.cloudproject.top/photo/' + name
    return name


if __name__ == "__main__":
    # 启动Flask服务，指定主机IP和端口
    app.run(host='127.0.0.1', port=8080)
