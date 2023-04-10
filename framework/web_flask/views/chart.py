#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from flask import Blueprint, render_template, request, jsonify
from framework.web_flask.controllers.single_gene_handler import SingleGeneHandler

blueprint = Blueprint('chart', __name__)


@blueprint.route('/bubble-chart')
def bubble_chart():
    return render_template("charts/bubble-chart.html")
