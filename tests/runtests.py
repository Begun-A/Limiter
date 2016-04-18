import tornado.testing
import unittest


TEST_MODULES = [
    'test_count_timeout',
    'test_http_client'
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


if __name__ == '__main__':
    tornado.testing.main()