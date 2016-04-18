import tornado.web
import tornado.ioloop

from handlers import TimeOutHandler

application = tornado.web.Application(
    handlers=[
        (r"/timeout", TimeOutHandler),
    ]
)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
