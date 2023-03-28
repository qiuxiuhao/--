import database_operate
from flask import Flask,jsonify,request, redirect, url_for, render_template
from flask_cors import CORS
import json
# 创建Flask服务
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app)
# 访问URL：http://127.0.0.1:8080/home/hello
# 返回结果：{"data":"welcome to use flask.","msg":"hello"}

@app.route('/login')  #访问路径,需要与hbuilder对应页面的url的.com之后的一致
def login(): #名字最好与访问路径同名
    data =database_operate.get()
    mydata = [dict(zip(("id",'name','langage','price','data'),x)) for x in data]
    return jsonify(mydata)        #以json格式返回数据

if __name__ == "__main__":
    # 启动Flask服务，指定主机IP和端口
    app.run(host='127.0.0.1', port=8080)