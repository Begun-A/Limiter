import tornado.web
import tornado.ioloop

from handlers import TimeoutHandler

application = tornado.web.Application(
    handlers=[
        (r"/timeout", TimeoutHandler),
    ]
)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
