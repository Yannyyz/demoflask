from flask import Flask, render_template, json, request, redirect

app = Flask(__name__)


#  json文件初始数据
name = 'Yann'
fake_name = "haha"
data = {
    'data': [
        {
            "name": "yann",
            "email": "123456789@qq.com",
            "message": "wonderful! wonderful! wonderful!"
        },
    ],
}


# 修改多个模板内的同个变量
@app.context_processor
def inject_user():  # 匿名函数可随意修改
    user = name
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


# 处理 URL 访问错误
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#  初始页
@app.route("/")
@app.route("/index")
def hello():
    return render_template('frontpage.html')


#  主页
@app.route("/home")
def home():
    return render_template('homepage.html')


#  留言板
@app.route('/question')
def question():
    with open("data.json", "rb")as f:
        load_data = json.loads(f.read().decode("utf-8"))
    return render_template('message.html', data=load_data['data'])


#  留言提交处理
@app.route('/handle', methods=['POST'])
def handle():
    tem = {}
    username = request.form.get('username')
    email = request.form.get('email')
    message = request.form.get('message')

    tem["name"] = username
    tem["email"] = email
    tem["message"] = message

    data['data'].append(tem)
    data_json = json.dumps(data)
    with open("data.json", 'wb')as f:
        f.write(data_json.encode("utf-8"))
    return redirect('/question')  # 重定向


# 入口函数
if __name__ == "__main__":
    app.run(debug=True)
