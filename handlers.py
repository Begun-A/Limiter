from datetime import datetime, timedelta
import tornado.web
import tornado.escape
import tornado.ioloop

DOMENS = {}
SECONDS = 10.0
REQUESTS = 5.0
RATE_LIMIT = SECONDS/REQUESTS

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

def count_timeout(domen, gen_time, step_timeout):

    if domen in DOMENS: # check domen in DOMENS dict
        last_call = DOMENS.get(domen)
        elapsed = datetime.now() - last_call # interval between now and last call which has been executed (+) or will be executed(-)
        elapsed = elapsed.total_seconds()
        if elapsed < 0: # last call wasn't made
            if step_timeout < gen_time: # if page generation time greatest than step timeout then timeout use gen_time, else step_timeout
                time_out = gen_time - elapsed # timeout consists of generation time and the remaining time before last call
                DOMENS[domen] = last_call + timedelta(seconds=gen_time)# set last call time
                return time_out
            else:
                time_out = step_timeout - elapsed # timeout consists of step timeout  and the remaining time before last call
                DOMENS[domen] = last_call + timedelta(seconds=step_timeout)
                return time_out
        elif step_timeout > elapsed > 0 or gen_time > elapsed > 0: # last call made  and elapsed less time than step timeout or generation time
            if step_timeout < gen_time: #if page generation time greatest than step timeout then timeout use gen_time, else step_timeout
                time_out = gen_time - elapsed # timeout equel generation time without elapsed time
                DOMENS[domen] = last_call + timedelta(seconds=gen_time)
                return time_out
            else:
                time_out = step_timeout - elapsed # timeout equal step timeout without elapsed time
                DOMENS[domen] = last_call + timedelta(seconds=step_timeout)
                return time_out
        else:
            DOMENS[domen] = datetime.now()
            return 0
    else:
        DOMENS[domen] = datetime.now() #  set last call time to the new domen
        return 0