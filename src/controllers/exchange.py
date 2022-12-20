# -*- coding: utf-8 -*-

__author__ = "Lucas Vidor Migotto"
__date__ = "$Dez 20, 2022 12:57:00 PM$"

import requests
from time import time
from datetime import datetime, timedelta
from flask import jsonify


class Exchange:

    def __init__(self, redis, config):
        """
        Contructor method

        Args:
            redis (_type_): Redis connection instance
            config (dict): Dictonary with env vars values
        """
        self.__redis = redis
        self.__config = config
        self.__symbols = ('USD', 'BRL', 'EUR', 'BTC')
        self.__expected_paramentes = ('to', 'from', 'amount')

    def __update_rates(self):
        """
        Update currencies exchange rates

        Request to the third party service in order to update the current values of currency exchange rates

        Raises:
            Exception: If the request does not return status 200, an exception is raised
        """
        # Request newest rates
        response = requests.get(
            f"{self.__config('EXCHANGE_API_URL')}/latest",
            params={
                'base': 'USD',
                'symbols': ','.join(self.__symbols)
            },
            headers={'apikey': self.__config('EXCHANGE_API_KEY')}
        )

        # If request fails, raise exception
        if response.status_code != 200:
            raise Exception('Request to 3rd party could not be successfully completed')
        response_json = response.json()

        # Update echange rate to every symbol
        for symbol in self.__symbols:
            self.__redis.set(f"exchange:{symbol}:rate", response_json['rates'][symbol])

        # Update key value to inform latest exchange rates update event
        self.__redis.set('exchange:latest', int(time()))

    def __convert_value(self, from_currency, to_currency, amount):
        """
        Convert values received in the request query parameters

        Args:
            from_currency (str): Code of the origin currency. Avaliable codes are the same as the self.__expected_paramentes prop
            to_currency (str): Code of the destiny currency. Avaliable codes are the same as the self.__expected_paramentes prop
            amount (str): Total amount to be exchange

        Returns:
            float: The total amount already converted
        """
        converted_value = float(amount)
        # If origin currency is different that the ballast, convert first to the base currency
        if from_currency != 'USD':
            converted_value = converted_value / float(self.__redis.get(f"exchange:{from_currency}:rate"))

        # If destiny currency is not already the ballast, convert to the chossen one
        if to_currency != 'USD':
            return float(self.__redis.get(f"exchange:{to_currency}:rate")) * converted_value

        # Or just return immediately
        else:
            return converted_value

    def convert_money(self, args):
        """
        Controller handler to convert currency amount

        Args:
            args (dict): The request query parameters. Must include 'from', 'to', 'amount'

        Returns:
            flask.Response: The request response
        """
        try:
            # Validate if all the query parameters was informed
            if not all((key in args.keys() for key in self.__expected_paramentes)):
                return jsonify({
                    'message': f"Please inform the following args: {', '.join(self.__expected_paramentes)}"
                }), 409

            # Validate of the origin and destiny currency are the same
            if args['from'] == args['to']:
                return jsonify({
                    'message': 'Please, choose the second currecy different that the first'
                }), 409

            # Check if the latest update was made more than an hour
            if datetime.fromtimestamp(int(self.__redis.get('exchange:latest'))) < datetime.now() - timedelta(hours=1):
                self.__update_rates()

            # Convert amount based in currencies informed
            converted_value = self.__convert_value(
                args['from'],
                args['to'],
                args['amount']
            )

            # Return response
            return jsonify({
                'message': 'Hello World',
                'data': converted_value
            }), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'Internal server error'}), 500
