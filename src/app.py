# -*- coding: utf-8 -*-

__author__ = "Lucas Vidor Migotto"
__date__ = "$Dez 20, 2022 12:57:00 PM$"

import redis
from flask import Flask
from flask import request
from decouple import config
from controllers.exchange import Exchange

app = Flask(__name__)
redis = redis.Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'))


@app.route('/convert', methods=['POST'])
def movies():
    return Exchange(redis, config).convert_money(request.args)
