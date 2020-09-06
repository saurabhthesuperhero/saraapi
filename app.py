import requests
from wit import Wit
from googletrans import Translator
import json
from flask import Flask,jsonify
import os
import logging
from unidecode import unidecode
import random
import wikipedia

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



greet=['Hello, I am Sara','Hi dear ','Hi, What can I do for you ?']

thankk=['welcome.','Its my pleasure.']

shy=['you make me shy','cause my creator is awesome']
love=['I love eating lot','hehe , nice to hear']
creator=['Saurabh is my creator','Saurabh is AI developer.']






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
        return unidecode(" '{0}'  This is how you will say {1} in {2}. ".format(x.pronunciation,text,language))
    except Exception as e:
        return "I didnt get destination language."

def searchf(subj):
    result = wikipedia.summary(subj, sentences = 2)
    return unidecode(result) 

def handle_message(response):
    print(json.dumps(json.loads(json.dumps(response)),indent=2))
    greeting=first_value(response['traits'], 'wit$greetings')
    thamk=first_value(response['traits'],'wit$thanks')
    typeof=first_value(response['entities'], 'type:type')
    bye=first_value(response['traits'], 'wit$bye')
    create=first_value(response['traits'],'shy')
    shy_=first_value(response['traits'],'creator')
    love_=first_value(response['traits'],'love')
    checkcap=check_intent(response['intents'],'name','capacity')
    checktranslate=check_intent(response['intents'],'name','phrase_translate')
    checksearch=check_intent(response['intents'],'name','question')
	# print(checktranslate)
    tbody=first_value(response['entities'],'wit$phrase_to_translate:phrase_to_translate')
    tlanguage=first_value(response['entities'],'wit$message_subject:message_subject')
    ssubject=first_value(response['entities'],'wit$message_subject:message_subject')
    snotable=first_value(response['entities'],'wit$wikipedia_search_query:wikipedia_search_query')
    swiki=first_entityvalue(response['entities'],'wit$notable_person:notable_person')

    if checkcap:
        return "Hello,I can chat with you, & translate to any language, like:translate hello in tamil, I can also give you information on topics."
    elif checksearch:
        if(snotable!=None):
            return searchf(snotable)
        elif(ssubject!=None):
            return searchf(ssubject)
        elif(swiki!=None):
            return searchf(swiki)
        else:
            return "Didnt got it,will learn and tell you."
    elif checktranslate:
	    return translate(tbody,tlanguage)
    elif typeof!=None:
	    if typeof.lower()=="movie":
		    return "Movie you can watch"
    elif bye:
	    return "Bye see you later"
    elif greeting:
	    return random.choice(greet)
    elif thamk:
        return random.choice(thankk)
    elif create:
        return random.choice(creator)
    elif shy_:
        return random.choice(shy)
    elif love_:
        return random.choice(love)
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


