from datetime import datetime, timedelta
import tornado.web
import tornado.escape
import tornado.ioloop

DOMENS = {}
SECONDS = 10.0
REQUESTS = 5.0
RATE_LIMIT = SECONDS / REQUESTS


class TimeOutHandler(tornado.web.RequestHandler):
    def post(self):
        """
        Calculate and return timeout for crawler
        """
        json = tornado.escape.json_decode(self.request.body)
        domen, gen_time = json['domen'], json['time']
        time_out = count_timeout(domen, gen_time, RATE_LIMIT)
        response = {'time_out': time_out}
        return self.write(response)


def count_timeout(domen, gen_time, rate_limit):
    """ The function count timeout for crawler.
    Timeout depends on greater value, page generation time or rate limit.
    Also depends on last request time.
    """
    if domen in DOMENS:                                                         # check domen in DOMENS dict
        last_request = DOMENS.get(domen)
        time_interval = datetime.now() - last_request                           # interval between now and last request time which display how many time left befor last request(-)
                                                                                # or how many time elapsed after last request (+)
        time_interval = time_interval.total_seconds()
        if gen_time >= rate_limit and (                                         #condition: generation time greater than rate limit and
                        time_interval <= 0 or gen_time > time_interval > 0):    # last request wasn't made (time_interval(-))
                                                                                # or  last request made but can't make request now (time_interval(+))

            time_out = gen_time - time_interval                                 # timeout equel generation time without time_interval(+) time or with time_interval(-)
            DOMENS[domen] = last_request + timedelta(seconds=gen_time)          # set last request time
            return time_out
        if rate_limit > gen_time and (
                        time_interval <= 0 or rate_limit > time_interval > 0):  # generation time less than rate limit,
                                                                                # last request wasn't made (time_interval(-))
                                                                                # or  last call made but can't make request now (time_interval(+))

            time_out = rate_limit - time_interval                               # timeout equal rate limit without time_interval(+) or with time_interval(-)
            DOMENS[domen] = last_request + timedelta(seconds=rate_limit)        # set last request time
            return time_out

        DOMENS[domen] = datetime.now()                                          # set last request time
        return 0                                                                # crawler can make request now
    else:
        DOMENS[domen] = datetime.now()                                          # set last request time to the new domen
        return 0                                                                # crawler can make request now
