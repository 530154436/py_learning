#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from flask import Blueprint, render_template, jsonify, request

from Web.FlaskWeb import BASE_DIR
from Web.FlaskWeb.controllers.downloader import ExcelDownloader
from Web.FlaskWeb.data.table_data import boostrap_table_data

blueprint = Blueprint('bootstrap_table', __name__)


@blueprint.route('/table-data', methods=["POST"])
def ajax_table():
    return jsonify(boostrap_table_data)


@blueprint.route('/download_excel', methods=["POST", "GET"])
def download_excel():
    print(request)
    if request.method == "GET":
        params: dict = request.args.to_dict()
    else:
        params: dict = request.form.to_dict()
    print(params)
    downloader = ExcelDownloader(BASE_DIR.joinpath("data", "result", f"{params.get('id')}.xlsx"))
    return downloader()


@blueprint.route('/ajax-table-basic')
def ajax_table_basic():
    return render_template("table/ajax-table-basic.html")


@blueprint.route('/ajax-table-stype')
def ajax_table_stype():
    return render_template("table/ajax-table-stype.html")
