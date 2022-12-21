# -*- coding: utf-8 -*-

__author__ = "Lucas Vidor Migotto"
__date__ = "$Dez 20, 2022 12:57:00 PM$"

# Imports
import logging
import redis
from flask import Flask
from flask import request
from decouple import config
from controllers.exchange import Exchange

# Create Flask app instance
app = Flask(__name__)

# Create REDIS connection
redis = redis.Redis(
    host=config('REDIS_HOST', default='localhost'),
    port=config('REDIS_PORT', default=6379)
)

if redis.get('exchange:latest') is None:  # pragma: no cover
    redis.set('exchange:latest', 0)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    filemode='a',
    filename='ds-api.log'
)
logger = logging.getLogger('ds-api')


# Route the POST /convert endpoint
@app.route('/convert', methods=['POST'])
def movies():
    logger.info(f"Requested received from IP {request.remote_addr}")
    # Return instance class Exchange calling convert_money method
    return Exchange(redis, logger, config).convert_money(request.args)
