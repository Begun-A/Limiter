from datetime import datetime, timedelta
import tornado.web
import tornado.escape
import tornado.ioloop

DOMENS = {}
SECONDS_LIMIT = 10.0
DOMENS_LIMIT = 5.0


class TimeOutHandler(tornado.web.RequestHandler):
    def post(self):
        """
        Calculate and return timeout for crowler
        """
        json = tornado.escape.json_decode(self.request.body)
        domen, time = json['domen'], json['time']
        time_out = count_timeout(domen, SECONDS_LIMIT/DOMENS_LIMIT)
        response = {'time_out': time_out}
        return self.write(response)

def count_timeout(domen, step):
    step_timeout = step
    if domen in DOMENS:
        last_call = DOMENS.get(domen)
        elapsed = datetime.now() - last_call
        elapsed = elapsed.total_seconds()
        if elapsed < 0:
            time_out = step_timeout + abs(elapsed)
            DOMENS[domen] = last_call + timedelta(seconds=step_timeout)
            return time_out
        elif step_timeout > elapsed > 0:
            time_out = step_timeout - abs(elapsed)
            DOMENS[domen] = last_call + timedelta(seconds=step_timeout)
            return time_out
        else:
            DOMENS[domen] = datetime.now()
            return 0
    else:
        DOMENS[domen] = datetime.now()
        return 0