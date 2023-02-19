#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from werkzeug.datastructures import ImmutableMultiDict


class SingleGeneHandler(object):

    def parse_form(self, form: ImmutableMultiDict) -> dict:
        """
        解析表单数据
        """
        has_input_gene_list = form.get("has_input_gene_list") == "1"
        input_gene_list = list(filter(lambda x: x != "", form.getlist("input_gene_list")))
        params = {
            "has_input_gene_list": has_input_gene_list,
            "input_gene_list": input_gene_list
        }
        return params

