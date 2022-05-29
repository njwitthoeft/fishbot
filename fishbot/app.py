
import os
import json
import requests
from flask import Flask
from flask import request
from slack_sdk.models.blocks import Block
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from fishbot.fishprofiles import profiles

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

import re
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/endpoint', methods = ['POST'])
def endpoint():
    if request.method == 'POST':
        request_data = request.get_json()
        #Verification for slack's sake.
        if a := request_data.get("challenge"):
            return a
        
        raw_text = request_data["event"]["text"]
        channel_id = request_data["event"]["channel"]

        if raw_text.lower() in profiles:
            response = requests.get(f"https://www.fishwatch.gov/api/species/{raw_text.lower().replace(' ','-')}")
            try:
                client.chat_postMessage(
                    channel = channel_id,
                    text = cleanhtml(json.loads(response.text)[0]["Habitat"])
                )
            except:
                SlackApiError()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port =8080)