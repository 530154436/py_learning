#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/08/28
@function:
"""
import traceback
import qa_processor
from flask_sockets import Sockets
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
sockets = Sockets(app)

# ------------------------------------------------------------------------
# 后端接口
# http://127.0.0.1:5200/answer?question=章子怡和周润发共同演了什么电影？
# ------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/answer')
def answer():
    try:
        text = request.args.get('question')
        answer = qa_processor.run(text)
        return jsonify({"code": 0,  "data": answer, "msg": '成功'})
    except Exception as err:
        extract_list = traceback.extract_tb(err.__traceback__, limit=5)
        for item in traceback.format_list(extract_list):
            print(item.strip())
        print(err)
        return jsonify({"code": -1, "msg": '未知错误'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5200)
    print('Server start: HTTP[5200]')