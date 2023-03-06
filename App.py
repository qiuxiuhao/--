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


@app.route('/login')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def login(): #名字最好与访问路径同名
    phonenumber1 = str(request.args.get('phonenumber'))     #获取uni.request所提交的data
    password1 = str(request.args.get('password'))       #获取uni.request所提交的data
    phonenumber = 123456        
    password = 123456   #原数据，实际应从数据库中获取
    if(phonenumber == int(phonenumber1) and password == int(password1)):    #比对数据，确认返回值
        contrast = True
    else:
        contrast = False
    return {'contrast':contrast}        #以json格式返回数据

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
    #number = str(request.args.get('phonenumber'))
    number = "15717217249"
    userid = str(m.get_userid(number))
    print(userid)
    n = database_operate.OpDB()
    data = n.get_userinfo(userid)
    print(data)
    l = database_operate.OpDB()
    data1 = l.get_payinfo(userid)
    mydata = dict(zip(("phone","gender","schoolName", "name","geXin"),data))
    mydata1 = dict(zip(("pycode", "nopaycode"), data1))
    bbb = '1234'
    print(mydata)
    return {
            'mydata': mydata,
            'mydata1': mydata1
    }


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


    