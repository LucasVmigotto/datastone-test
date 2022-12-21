# -*- coding: utf-8 -*-

__author__ = "Lucas Vidor Migotto"
__date__ = "$Dez 21, 2022 11:03:00 AM$"


from re import match
from json import loads
from unittest import TestCase
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

    def test_convert_brl_to_usd(self):
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

    def test_convert_usd_to_brl(self):
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
