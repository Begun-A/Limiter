Rate Limit API.
Python 2.7.6
Service built using Tornado.

pip install -r requirements.txt
To configure max number requests per seconds
use variables REQUESTS and SECONDS in handler.py
python app.py in terminal.
To get timeout for 'domen_name' with page genertion time 5 seconds:
localhost:8888/timeout?domen=domen_name&time=5 in your browser.
