#import yaml
import flask
from flask import request, jsonify, request, send_from_directory
import concurrent.futures
import yaml
import time
import logging

app = flask.Flask(__name__,
                  static_url_path='',
                  static_folder=''
                  )
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['JSON_KEYS_SORT'] = False

logging.basicConfig(level=logging.DEBUG,
                    filemode='a',
                    format='{asctime} - {levelname} - [{funcName}:{lineno}] - {message}',
                    style='{')

"""
http://127.0.0.1:5000/lazy-mounting/api/query
"""

"""
Refer to below link for better reading on decorators
https://realpython.com/primer-on-python-decorators/#simple-decorators
"""
def perf(f):
    def _perf(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logging.debug('--> START - Calling {}({})'.format(f.__name__, signature))
        start_time = time.perf_counter()
        retVal = f(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logging.debug('--> END   - {} - in {:.4f} secs'.format(f.__name__, run_time))
        #logging.debug(f'--> END   - {f.__name__!r} returned {retVal!r} - in {run_time:.4f} secs')
        return retVal
    return _perf

####################################################################################################################

@perf
class LazyMounting:
    def __init__(self, env, key, value):
        logging.debug("Inside LaztMounting constructor")
        self._env = env
        self._key = key
        self._value = value

        self._svc_order_id = ""
        self._service_id = ""
        self._trail_id = 0
        self._db_conn = {}
        self._db_keys = {}
        self._db_keys[self._key] = self._value

        self._results = {'env':self._env,
                         'key':self._key,
                         'value':self._value
                         }

    @perf
    def processAPI(self):
        self._handle_db_connections()

        with open(r'tables.yaml') as file:
            documents = yaml.full_load(file)

            if 'domains' in documents:
                for itrDomains in documents['domains']:
                    domain_name = itrDomains['name'] if 'name' in itrDomains else None
                    if 'tables' in itrDomains:
                        self._fetch_records_per_domain(domain_name, itrDomains['tables'])

        self._handle_db_connections()

####################################################################################################################

@perf
@app.route('/', methods=['GET'])
def root():
    logging.debug('Entering root')
    return app.send_static_file('web/index.html')

@perf
@app.route('/mount', methods=['GET'])
def mount():
    try:
        logging.debug('Hello')
    except Exception as e:
        logging.error('Error: {}'.format(e))
        raise jsonify('Error: {}'.format(e))
    else:
        logging.debug('There is NO exception')

    return 'Hello'

@perf
@app.route('/logs', methods=['GET'])
def logs():
    try:
        logging.debug('Hello')
        rsp_data = []

        with open(r'app-bin.log') as fp:
            for line in (fp.readlines() [-10:]):
                rsp_data.append(line)

    except Exception as e:
        logging.error('Error: {}'.format(e))
        raise jsonify('Error: {}'.format(e))
    else:
        logging.debug('There is NO exception')

    return jsonify(rsp_data)

@perf
@app.route('/fetch', methods=['GET'])
def fetch():
    try:
        logging.debug('Hello')
    except Exception as e:
        logging.error('Error: {}'.format(e))
        raise jsonify('Error: {}'.format(e))
    else:
        logging.debug('There is NO exception')

    return jsonify( [ [1,2,3,4,5,6], [1,2,3,4,5,6], [1,2,3,4,5,6], [1,2,3,4,5,6], [1,2,3,4,5,6]] )

# TODO - Try making this a json input rather than a query parameter
@perf
@app.route('/lazy-mounting/api/query', methods=['GET'])
def query():

    ####################################################################################################################
    logging.debug('Is json Request: {}'.format(request.is_json))
    try:
        if request.args:
            p_env = request.args['ENV'] if 'ENV' in request.args else 'None'
            p_key = request.args['KEY'] if 'KEY' in request.args else 'None'
            p_value = request.args['VALUE'] if 'VALUE' in request.args else 'None'

        logging.debug('ENV - type(p_env) = {} - value = {}'.format(type(p_env), p_env) )
        logging.debug('KEY - type(p_key) = {} - value = {}'.format(type(p_key), p_key))
        logging.debug('VALUE - type(p_value) = {} - value = {}'.format(type(p_value), p_value))

        if p_env == 'None' or p_key == 'None' or p_value == 'None' :
            ## TODO - see if we can comeup with an exception class and properly passon the message. currently, status code is missing
            ## https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
            raise Exception('Invalid Parameters')

    ####################################################################################################################

        objLazyMounting = LazyMounting(p_env, p_key, p_value)
        objLazyMounting.processAPI()
        logging.debug(f'Final Results are {objLazyMounting.results()}')

    ####################################################################################################################

    except Exception as e:
        logging.error('Error: {}'.format(e))
        raise jsonify('Error: {}'.format(e))
    else:
        logging.debug('There is NO exception')

    return jsonify(objLazyMounting.results())

def main():
    logging.debug("Hello!")
    app.config["DEBUG"] = True

if __name__ == "__main__": main()

app.run()
