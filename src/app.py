# -*- coding: utf-8 -*-

__author__ = "Lucas Vidor Migotto"
__date__ = "$Dez 20, 2022 12:57:00 PM$"

# Imports
import redis
from flask import Flask
from flask import request
from decouple import config
from controllers.exchange import Exchange

# Create Flask app instance
app = Flask(__name__)

# Create REDIS connection
redis = redis.Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'))


# Route the POST /convert endpoint
@app.route('/convert', methods=['POST'])
def movies():
    # Return instance class Exchange calling convert_money method
    return Exchange(redis, config).convert_money(request.args)
