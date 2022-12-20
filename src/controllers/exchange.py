# -*- coding: utf-8 -*-

__author__ = "Lucas Vidor Migotto"
__date__ = "$Dez 20, 2022 12:57:00 PM$"

import requests
from time import time
from datetime import datetime, timedelta
from flask import jsonify


class Exchange:

    def __init__(self, redis, config):
        self.__redis = redis
        self.__config = config
        self.__symbols = ('USD', 'BRL', 'EUR', 'BTC')
        self.__expected_paramentes = ('to', 'from', 'amount')

    def __update_rates(self):
        response = requests.get(
            f"{self.__config('EXCHANGE_API_URL')}/latest",
            params={
                'base': 'USD',
                'symbols': ','.join(self.__symbols)
            },
            headers={'apikey': self.__config('EXCHANGE_API_KEY')}
        )
        if response.status_code != 200:
            raise Exception('Request to 3rd party could not be successfully completed')
        for symbol in self.__symbols:
            self.__redis.set(f"exchange:{symbol}:rate", response_json['rates'][symbol])
        self.__redis.set('exchange:latest', int(time()))

    def __convert_value(self, from_currency, to_currency, amount):
        converted_value = float(amount)
        if from_currency != 'USD':
            converted_value = converted_value / float(self.__redis.get(f"exchange:{from_currency}:rate"))
        if to_currency != 'USD':
            return float(self.__redis.get(f"exchange:{to_currency}:rate")) * converted_value
        else:
            return converted_value

    def convert_money(self, args):
        try:
            if not all((key in args.keys() for key in self.__expected_paramentes)):
                return jsonify({
                    'message': f"Please inform the following args: {', '.join(self.__expected_paramentes)}"
                }), 409
            if args['from'] == args['to']:
                return jsonify({
                    'message': 'Please, choose the second currecy different that the first'
                }), 409
            if datetime.fromtimestamp(int(self.__redis.get('exchange:latest'))) < datetime.now() - timedelta(hours=1):
                self.__update_rates()
            converted_value = self.__convert_value(
                args['from'],
                args['to'],
                args['amount']
            )
            return jsonify({
                'message': 'Hello World',
                'data': converted_value
            }), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'Internal server error'}), 500
