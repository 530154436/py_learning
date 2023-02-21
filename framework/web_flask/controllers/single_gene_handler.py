#!/usr/bin/env python3
# -*- coding:utf-8 -*--
import pandas as pd
from flask import Request
from werkzeug.utils import secure_filename

from framework.web_flask import BASE_DIR


class SingleGeneHandler(object):

    def __init__(self, **kwargs):
        self.input_gene_list = kwargs.get("input_gene_list")
        self.input_ppi = 0
        self.bnl_random_num = kwargs.get("bnl_random_num")
        self.ppi_db = kwargs.get("ppi_db")

    def json(self):
        return vars(self)

    def parse_form(self, request: Request):
        """
        解析表单数据
        """
        # 输入基因列表
        has_input_gene_list = request.form.get("has_input_gene_list") == "1"
        if has_input_gene_list:
            self.input_gene_list = list(filter(lambda x: x != "", request.form.getlist("input_gene_list")))
        else:
            input_file = request.files['input_file']
            file = BASE_DIR.joinpath("data", "upload", secure_filename(input_file.filename))
            input_file.save(file)
            if file.suffix == 'xlsx':
                df: pd.DataFrame = pd.read_excel(file, header=None)
                self.input_gene_list = df[0].tolist()

        # PPI分值
        self.input_ppi = request.form.get("input_ppi")

        # 伯努利检验
        bnl_select = request.form.get("bnl_select") == "yes"
        if bnl_select:
            self.bnl_random_num = int(request.form.get("bnl_random_num"))

        # 数据库相关
        self.ppi_db = request.form.getlist("ppi_db")
