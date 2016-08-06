# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests
import random

app = Flask(__name__)

access_token = 'EAAJCQpvWZB8IBAOe9coFvwZAd9LaCzFlhsS2kp0f81qkz2RleYzg78YbOx82HpgxYGoFOp1f1FoBsgtncGfDc9JGanbt8BPkErR0ExGCO0V2UAwBKxNZCCPZAecNtcoYZAqKX89AeZBkr4We1nbJ4reKTaLPliC6vigRsJSzl6BAZDZD'


@app.route("/", methods=["GET"])
def root():
    return "Hello World!"


# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET'])
def get_webhook():

    if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args:
        abort(400)

    return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = request.json

    if data["object"] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                if "message" in messaging_event:

                    sender_id = messaging_event['sender']['id']

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text'].lower()
                        '''
                        image = "http://cdn.shopify.com/s/files/1/0080/8372/products/tattly_jen_mussari_hello_script_web_design_01_grande.jpg"
                        element = create_generic_template_element("Hello", image, message_text)
                        reply_with_generic_template(sender_id, [element])
                        '''
                        do_rules(sender_id, message_text)

    return "ok", 200


def get_url(url):
    result = request.get(url)
    return json.loads(result.content)


def do_rules(recipient_id, message_text):
    rules = {
        "hi": "Hey! Give me a date (dd.mm.yyyy) ;)",
    }

    dates = {
        "01.01.1990": "https://www.youtube.com/watch?v=Qt2mbGP6vFI",
        "21.05.1983": "https://www.youtube.com/watch?v=N4d7Wp9kKjA",
        "05.08.1989": "https://www.youtube.com/watch?v=pfLFP7WncLI",
    }
    greetings = ["Enjoy!", "Have fun ;)", "Let's dance!", "Freak out on:", "Fancy!", "Live it up"]

    if message_text in rules:
        reply = rules[message_text]
    elif message_text in dates:
        reply = random.choice(greetings) + " " + dates[message_text]
    else:
        reply = "Sorry, I don't unterstand. Give me a date (dd.mm.yyyy)"

    reply_with_text(recipient_id, reply)

'''
def show_video(url):
    import urllib.request
    import urllib.parse
    import re

    query_string = urllib.parse.urlencode({"search_query" : input()})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("http://www.youtube.com/watch?v=" + search_results[0])
'''

def reply_with_text(recipient_id, message_text):
    message = {
        "text": message_text
    }
    reply_to_facebook(recipient_id, message)


def reply_with_generic_template(recipient_id, elements):
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
    reply_to_facebook(recipient_id, message)


def reply_to_facebook(recipient_id, message):
    params = {
        "access_token": access_token
    }

    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message
    })

    print data

    url = "https://graph.facebook.com/v2.6/me/messages?" + urllib.urlencode(params)
    r = requests.post(url=url, headers=headers, data=data)


def create_generic_template_element(title, image_url, subtitle):
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle
    }


if __name__ == '__main__':
    app.run(debug=True)