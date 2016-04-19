from datetime import datetime, timedelta
import tornado.web
import tornado.escape
import tornado.ioloop

DOMENS = {}
SECONDS = 10.0
REQUESTS = 5.0
RATE_LIMIT = SECONDS / REQUESTS


class TimeOutHandler(tornado.web.RequestHandler):
    def get(self):
        """
        Calculate and return timeout for crawler
        """
        domen =  self.get_argument('domen')
        gen_time = float(self.get_argument('time'))
        timeout = count_timeout(domen, gen_time, RATE_LIMIT)
        response = {'timeout': timeout}
        return self.write(response)


def count_timeout(domen, gen_time, rate_limit):
    """ The function count timeout for crawler.
    Timeout depends on greater value, page generation time or rate limit.
    Also depends on last request time.
    """
    if domen in DOMENS: # check domen in DOMENS dict
        last_request = DOMENS.get(domen)
        # Interval between now and last request time which display how many time left befor last request(-)
        # or how many time elapsed after last request (+)
        time_interval = datetime.now() - last_request
        time_interval = time_interval.total_seconds()

        # #Uncomented code below if you want limit crawlers timeout (> SECONDS-RATE_LIMIT*2).
        # if abs(time_interval) > SECONDS-RATE_LIMIT*2:
        #     return 'Too many requests per second or pages generation very slow'

        #Condition: generation time greater than rate limit and
        # last request wasn't made (time_interval(-))
        # or  last request made but can't make request now (time_interval(+))
        if gen_time >= rate_limit and (
                        time_interval <= 0 or gen_time > time_interval > 0):
            timeout = gen_time - time_interval    # Timeout equel generation time without time_interval(+) time or with time_interval(-)
            DOMENS[domen] = last_request + timedelta(seconds=gen_time)  # set last request time
            return timeout
        # Generation time less than rate limit,
        # last request wasn't made (time_interval(-))
        # or  last call made but can't make request now (time_interval(+))
        if rate_limit > gen_time and (
                        time_interval <= 0 or rate_limit > time_interval > 0):
            timeout = rate_limit - time_interval   # Timeout equal rate limit without time_interval(+) or with time_interval(-)
            DOMENS[domen] = last_request + timedelta(seconds=rate_limit)    # set last request time
            return timeout

        DOMENS[domen] = datetime.now()  # set last request time
        return 0    # crawler can make request now
    else:
        DOMENS[domen] = datetime.now()  # set last request time to the new domen
        return 0    # crawler can make request now
