# -*- coding: utf-8 -*-

__author__ = "Lucas Vidor Migotto"
__date__ = "$Dez 21, 2022 11:03:00 AM$"


from time import time
from time import mktime
from datetime import datetime
from datetime import timedelta
from re import match
from json import loads
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from app import app as web_api


class TestWebApiApp(TestCase):
    def setUp(self):
        self.app = web_api.test_client()

    def test_validation_query_params_missing(self):
        response = self.app.post(
            '/convert',
            query_string={
                'from': 'BRL',
                'amount': 100.50
            }
        )
        assert 409 == response.status_code
        assert 'message' in loads(response.data)
        assert match(r'^Please inform the following args', loads(response.data)['message'])

    def test_validation_query_param_from_equal_to(self):
        response = self.app.post(
            '/convert',
            query_string={
                'to': 'BRL',
                'from': 'BRL',
                'amount': 100.50
            }
        )
        assert 409 == response.status_code
        assert 'message' in loads(response.data)
        assert 'Please, choose the second currecy different that the first' == loads(response.data)['message']

    @patch("app.redis")
    def test_convert_notupdate_brl_to_usd(self, redis_mock):
        redis_mock.get.return_value = str(int(time()))
        response = self.app.post(
            '/convert',
            query_string={
                'from': 'BRL',
                'to': 'USD',
                'amount': 100.50
            }
        )
        assert 200 == response.status_code
        assert 'data' in loads(response.data)
        assert 'message' in loads(response.data)
        assert match(r'^Successfully exchanged', loads(response.data)['message'])

    @patch("app.redis")
    def test_convert_notupdate_usd_to_brl(self, redis_mock):
        redis_mock.get.return_value = str(int(time()))
        response = self.app.post(
            '/convert',
            query_string={
                'from': 'USD',
                'to': 'BRL',
                'amount': 100.50
            }
        )
        assert 200 == response.status_code
        assert 'data' in loads(response.data)
        assert 'message' in loads(response.data)
        assert match(r'^Successfully exchanged', loads(response.data)['message'])

    @patch("app.redis")
    @patch("controllers.exchange.requests")
    def test_convert_update_usd_to_brl(self, redis_mock, request_mock):
        redis_mock.get.return_value = str(int(mktime((datetime.now() - timedelta(hours=2)).timetuple())))
        redis_mock.set.return_value = 'OK'
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = {
            'success': True,
            'timestamp': 1671651783,
            'base': 'USD',
            'date': '2022-12-21',
            'rates': {
                'USD': 1,
                'BRL': 5.199896,
                'EUR': 0.94212,
                'BTC': 5.9627876e-05
            }
        }
        redis_mock.get.return_value = response_mock
        response = self.app.post(
            '/convert',
            query_string={
                'from': 'USD',
                'to': 'BRL',
                'amount': 100.50
            }
        )
        assert 200 == response.status_code
        assert 'data' in loads(response.data)
        assert 'message' in loads(response.data)
        assert match(r'^Successfully exchanged', loads(response.data)['message'])
