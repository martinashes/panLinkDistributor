from flask import Flask, request, render_template, session, redirect, url_for
import random
import csv
import io

app = Flask(__name__)
# 定义一个空数组用于存储数据
links = []
mobile = []

# 随机发放版本
# @app.route('/')
# def index():
#     if links:
#         data = random.choice(links)
#         msg = data[1] + " 提取码：" + data[2]
#     else:
#         msg = 'No links available'
#     return render_template("index.html", data = msg)  # 加入变量传递


# 根据手机号发放版本
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mobile_number = request.form['mobile']
        if mobile_number in mobile:
            index = mobile.index(mobile_number)
            data = links[index]
            msg = data[1] + " 提取码：" + data[2]
        else:
            msg = '没有符合该手机号的信息'
    else:
        msg = '请输入手机号'
    return render_template("index.html", data = msg)  # 加入变量传递


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'martin' and password == '1muzhi':
            return redirect('/upload')  # 校验通过，跳转到upload页面
        else:
            return "用户名或密码错误！"
    return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if len(links) > 0:
        return render_template('upload.html', data=links)
    if request.method == 'POST':
        # 获取上传的文件
        file = request.files['csv_file']

        # 检查文件扩展名是否为csv
        if file and file.filename.endswith('.csv'):
            # 使用io模块将文件对象以文本模式读取
            io_stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader = csv.reader(io_stream)

            # 遍历每一行数据
            for row in reader:
                links.append([len(links), row[4], row[5], row[3]])  # 第1列是自增长的序号，第2列是links，第3列是keys
                mobile.append(row[3])
            # 在这里可以对links数组进行处理，如打印或保存到数据库
            data = links[1: ]
            return render_template('upload.html', data=links)
        return "请选择一个csv文件！"
    return render_template('upload.html')


if __name__=="__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)