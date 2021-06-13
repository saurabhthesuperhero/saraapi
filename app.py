import requests
from wit import Wit
from googletrans import Translator
import json
from flask import Flask, jsonify
import os
import logging
from unidecode import unidecode
import random
import wikipedia
# Load data preprocessing libs
import pandas as pd
import numpy as np

# Load vectorizer and similarity measure
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#Initializations

app=Flask(__name__)
WIT_API_HOST = os.getenv('WIT_URL', 'https://api.wit.ai')
WIT_API_VERSION = os.getenv('WIT_API_VERSION', '20200513')
access_token = "ADRPSCFWVJEDDBCIYEP4ZFLY3EREFPYC"
client = Wit(access_token)

#Flask run
if __name__ == '__main__':
    app.run()

greet = ['Hello, I am Sara', 'Hi dear ', 'Hi, What can I do for you ?']

thankk = ['welcome.', 'Its my pleasure.']

shy = ['you make me shy', 'cause my creator is awesome']
love = ['I love eating lot', 'hehe , nice to hear']
creator = ['Saurabh is my creator', 'Saurabh is AI developer.']

#Homepage
@app.route('/')
def Index():
    return "Hello I am Sara!"



def check_intent(obj, key, name):
    if key not in obj[0]:
        return None
    if obj[0][key] == name:
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


def translate(text, language):
    try:
        translator = Translator()
        logging.debug(text+language)
        x = translator.translate(text, dest=language)
        return unidecode(" '{0}'  This is how you will say {1} in {2}. ".format(x.pronunciation, text, language))
    except Exception as e:
        print(e)
        return "I didnt get destination language."


def searchf(subj):
    try:
        result = wikipedia.summary(subj, sentences=2)
        return unidecode(result)
    except:
        return "Sorry ..Didnt get it...learning"


def handle_message(response):
    try:
        print(json.dumps(json.loads(json.dumps(response)), indent=2))
        greeting = first_value(response['traits'], 'wit$greetings')
        thamk = first_value(response['traits'], 'wit$thanks')
        typeof = first_value(response['entities'], 'type:type')
        bye = first_value(response['traits'], 'wit$bye')
        create = first_value(response['traits'], 'shy')
        shy_ = first_value(response['traits'], 'creator')
        love_ = first_value(response['traits'], 'love')
        checkcap = check_intent(response['intents'], 'name', 'capacity')
        checktranslate = check_intent(response['intents'], 'name', 'phrase_translate')
        checksearch = check_intent(response['intents'], 'name', 'question')
        # print(checktranslate)
        tbody = first_value(response['entities'], 'wit$phrase_to_translate:phrase_to_translate')
        tlanguage = first_value(response['entities'], 'wit$message_subject:message_subject')
        ssubject = first_value(response['entities'], 'wit$message_subject:message_subject')
        snotable = first_value(response['entities'], 'wit$wikipedia_search_query:wikipedia_search_query')
        swiki = first_entityvalue(response['entities'], 'wit$notable_person:notable_person')

        if checkcap:
            return "Hello,I can chat with you, & translate to any language, like:translate hello in tamil, I can also give you information on topics."
        elif checksearch:
            if (snotable != None):
                return searchf(snotable)
            elif (ssubject != None):
                return searchf(ssubject)
            elif (swiki != None):
                return searchf(swiki)
            else:
                return "Didnt got it,will learn and tell you."
        elif checktranslate:
            return translate(tbody, tlanguage)
        elif typeof != None:
            if typeof.lower() == "movie":
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
    except Exception as e:
        return "Soryy Im learning dear, will be awesome soon"






@app.route('/call=<lstring>')
def mainapp(lstring):
    data = []
    params = lstring
    data.append({"message": handle_message(client.message(params))})
    return jsonify(data=data, status=200)

@app.route('/call2=<lstring>')
def mainapp2(lstring):
    data=[]
    df = pd.read_csv("DFs1s2.csv")
    df.dropna(inplace=True)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.p1, df.p2)))
    Question_vectors = vectorizer.transform(df.p1)    
    # Locate the closest question
    input_question_vector = vectorizer.transform([lstring])

    # Compute similarities
    similarities = cosine_similarity(input_question_vector, Question_vectors)

    # Find the closest question
    closest = np.argmax(similarities, axis=1)

    # Print the correct answer
    message=(df.p2.iloc[closest].values[0])
    data.append({"message": message})
    return jsonify(data=data, status=200)    