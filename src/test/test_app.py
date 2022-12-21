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
