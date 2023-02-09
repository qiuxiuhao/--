from flask import Flask, request, redirect, url_for, render_template
from flask_cors import CORS
import json
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
    return {}

if __name__ == "__main__":
    # 启动Flask服务，指定主机IP和端口
    app.run(host='127.0.0.1', port=8080)


    