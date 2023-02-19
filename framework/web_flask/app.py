#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from flask import Flask
from framework.web_flask.views import bootstrap_table
from framework.web_flask.views import form


app = Flask(__name__, template_folder="templates", static_folder="static")  # 创建应用

blueprints = [
    bootstrap_table.blueprint,
    form.blueprint,
]
for blueprint in blueprints:
    app.register_blueprint(blueprint)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
