from flask import Flask, request, redirect, url_for, render_template
from flask_cors import CORS
import json
# 创建Flask服务
app = Flask(__name__)
CORS(app)
# 访问URL：http://127.0.0.1:8080/home/hello
# 返回结果：{"data":"welcome to use flask.","msg":"hello"}
@app.route('/login')
def home():
    phonenumber1 = str(request.args.get('phonenumber'))
    password1 = str(request.args.get('password'))
    phonenumber = 123456 
    password = 123456
    if(phonenumber == int(phonenumber1) and password == int(password1)):
        contrast = True
    else:
        contrast = False
    return {'contrast':contrast}

if __name__ == "__main__":
    # 启动Flask服务，指定主机IP和端口
    app.run(host='127.0.0.1', port=8080)


    