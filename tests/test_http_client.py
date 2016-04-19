import sys, os
import json
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.escape import json_decode

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(APP_ROOT))

import app

ACCURACY = 1


class TestHandlerBase(AsyncHTTPTestCase):
    def setUp(self):
        super(TestHandlerBase, self).setUp()

    def get_app(self):
        return app.application


class HttpClientTest(TestHandlerBase):
    def setUp(self):
        super(HttpClientTest, self).setUp()
        from handlers import DOMENS
        DOMENS.clear()

    @gen_test
    def test_tree_requests_at_the_same_time(self):
        url1 = r'/timeout?domen=domen1&time=0.5'
        url2 = r'/timeout?domen=domen2&time=0.5'

        request1 = HTTPRequest(url=self.get_url(url1), method='GET')
        request2 = HTTPRequest(url=self.get_url(url2), method='GET')
        for i in range(3):
            response = yield self.http_client.fetch(request1)
            timeout = round(json_decode(response.body)['timeout'], ACCURACY)
            self.assertEqual(timeout, i * 2)
            response = yield self.http_client.fetch(request2)
            timeout = round(json_decode(response.body)['timeout'], ACCURACY)
            self.assertEqual(timeout, i * 2)
