#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from flask import Blueprint, render_template, request
from Web.FlaskWeb.controllers.single_gene_handler import SingleGeneHandler

blueprint = Blueprint('form', __name__)

sg_handler = SingleGeneHandler()


@blueprint.route('/ajax-submit-form', methods=["POST"])
def ajax_submit_form():
    if request.method == 'POST':
        params: dict = sg_handler.parse_form(request.form)
        print(params)


@blueprint.route('/ajax-form')
def ajax_table_stype():
    return render_template("form/ajax-form.html")