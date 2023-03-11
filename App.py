from flask import Flask, request,jsonify ,redirect, url_for, render_template
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
@app.route('/login')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def login(): #名字最好与访问路径同名
    phonenumber1 = str(request.args.get('phonenumber'))     #获取uni.request所提交的data
    password1 = str(request.args.get('password')) #获取uni.request所提交的data
    n = database_operate.OpDB()
    mydata = ''
    mydata1= ''
    userid=''
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
        mydata = dict(zip(("id", "password", "phonenumber", "gender", "school", "name", "autograph"), data))
        mydata1 = dict(zip(("payword", "no_secret"), data1))

    return {'contrast': contrast,
            'userinfo': mydata,
            'pay': mydata1
            }        #以json格式返回数据

# 创建新用户
@app.route('/userinfoset')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def userinfoset():
    name = str(request.args.get('name'))
    phonenumber = str(request.args.get('phonenumber'))
    password = str(request.args.get('password'))
    gender = str(request.args.get('gender'))
    school = str(request.args.get('school'))
    pay_password = str(request.args.get('pay_password'))
    m = database_operate.OpDB()
    m.create_user(phonenumber, password, school, gender, name, int(pay_password))
    return {
        'f':'true'
    }

# 获取学校名
@app.route('/schoolinfo')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def schoolinfo():
    m = database_operate.OpDB()
    data = m.get_school()
    return {'schoolname': data}

@app.route('/submitinfo')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def submitinfo():
    name = str(request.args.get('name'))
    # phonenumber = str(request.args.get('phonenumber'))
    # password = str(request.args.get('password'))
    gender = str(request.args.get('gender'))
    school = str(request.args.get('school'))
    userid = str(request.args.get('id'))
    autograph = str(request.args.get('autograph'))
    m = database_operate.OpDB()
    # m.change_info1('password', password, userid)
    # m.change_info1('phone', phonenumber, userid)
    m.change_info1('schoolName', school, userid)
    m.change_info1('gender', gender, userid)
    m.change_info2('name', name, userid)
    m.change_info2('geXin', autograph, userid)
    return {
        'f': 'true'
    }

app.route('/nopayset')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def nopayset():
    no_secret = str(request.args.get('no_secret'))
    userid = str(request.args.get('id'))
    m = database_operate.OpDB()
    m.change_payment('nopayCode', no_secret, userid)
    return {
        'f': 'true'
    }


# 发送验证码
@app.route('/captcha')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def captcha():
    m = code.code()
    cd = str({"code": m})
    number = str(request.args.get('phonenumber'))
    # send.senMessage(number, cd)
    print(m)
    return {'captcha': m}

@app.route('/exist')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def exist():
    number = str(request.args.get('phonenumber'))
    is_newuser = database_operate.OpDB()
    exist1 = str(is_newuser.exist_phonenumber(number))
    exist1 = '123456'
    print(exist1)
    return {'exist123': exist1}

@app.route('/register')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def register():
    m = database_operate.OpDB()
    number = str(request.args.get('phonenumber'))
    userid = str(m.get_userid(number))

    n = database_operate.OpDB()
    data = n.get_userinfo(userid)

    l = database_operate.OpDB()
    data1 = l.get_payinfo(userid)
    mydata = dict(zip(("id","password","phonenumber","gender","school", "name","autograph"),data))
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
    return name


if __name__ == "__main__":
    # 启动Flask服务，指定主机IP和端口
    app.run(host='127.0.0.1', port=8080)


    