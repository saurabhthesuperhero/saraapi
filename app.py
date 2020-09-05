import requests
from wit import Wit
from googletrans import Translator
import json
from flask import Flask,jsonify
import os
import logging
from unidecode import unidecode

app = Flask(__name__)

WIT_API_HOST = os.getenv('WIT_URL', 'https://api.wit.ai')
WIT_API_VERSION = os.getenv('WIT_API_VERSION', '20200513')
access_token="ADRPSCFWVJEDDBCIYEP4ZFLY3EREFPYC"
client = Wit(access_token)
@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()


def req(logger, access_token, meth, path, params, **kwargs):
    full_url = WIT_API_HOST + path
    logger.debug('%s %s %s', meth, full_url, params)
    headers = {
        'authorization': 'Bearer ' + access_token,
        'accept': 'application/vnd.wit.' + WIT_API_VERSION + '+json'
    }
    headers.update(kwargs.pop('headers', {}))
    rsp = requests.request(
        meth,
        full_url,
        headers=headers,
        params=params,
        **kwargs
    )
    if rsp.status_code > 200:
        return "400"
    json = rsp.json()
    if 'error' in json:
        return "400"

    logger.debug('%s %s %s', meth, full_url, json)
    return json
def message( msg, context=None, n=None, verbose=None):
    params = {}
    logger=logging.getLogger()
    if n is not None:
        params['n'] = n
    if msg:
        params['q'] = msg
    if context:
        params['context'] = json.dumps(context)
    if verbose:
        params['verbose'] = verbose
    resp = req(logger, access_token, 'GET', '/message', params)
    return resp



# res=client.message('suggest sad movies')
# # print('res is '+str(res))

def check_intent(obj,key,name):
	if key not in obj[0]:
		return None
	if obj[0][key]==name:
		return 1
	else:
		return 0


def first_value(obj, key):
    if key not in obj:
        return None
    val = obj[key][0]['value']
    if not val:
        return None
    return val

def first_entityvalue(obj, key):
    if key not in obj:
        return None
    val = obj[key][0]['body']
    if not val:
        return None
    return val

def translate(text,language):
    try:
        translator = Translator()
        x=translator.translate(text, dest=language)
        return unidecode(" '{0}' \n This is how you will say {1} in {2} \n & Pronounciation is '{3}'".format(x.text,text,language,x.pronunciation))
    except Exception as e:
        return "I didnt get destination language."
def handle_message(response):
	print(json.dumps(json.loads(json.dumps(response)),indent=2))
	greeting=first_value(response['traits'], 'wit$greetings')
	typeof=first_value(response['entities'], 'type:type')
	bye=first_value(response['traits'], 'wit$bye')

# translate wala
	checktranslate=check_intent(response['intents'],'name','phrase_translate')
	# print(checktranslate)
	tbody=first_value(response['entities'],'wit$phrase_to_translate:phrase_to_translate')
	tlanguage=first_value(response['entities'],'wit$message_subject:message_subject')
	
	if checktranslate:
		return translate(tbody,tlanguage)
	elif typeof!=None:
		 if typeof.lower()=="movie":
		 	return "Movie you can watch"
	elif bye:
		return "Bye see you later"
	elif greeting:
		return "Hi ask me to translate"
	else:
		return "........oooooo"
@app.route('/call=<lstring>')
def mainapp(lstring):
	data=[]
	params=lstring
	logger=logging.getLogger()
	resp = req(logger, access_token, 'GET', '/message', params)
	data.append({"message":handle_message(message(params))})
	return jsonify(data=data,status=200)


