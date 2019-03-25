import time
from datetime import datetime
import json 
import requests
import urllib
import os

TELEGRAM_TOKEN = os.environ['AAC']
WEATHER_TOKEN = os.environ['AAC2']

fieldLat = "41.86"
fieldLon = "12.47"

TELEGRAM_URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)
WEATHER_URL = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}".format(fieldLat,fieldLon,WEATHER_TOKEN)

#Used emoji
winkingFace = u'\U0001F609'


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
	url = TELEGRAM_URL + "getUpdates?timeout=100"
	if offset:
		url += "&offset={}".format(offset)
	js = get_json_from_url(url)
	return js
	
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
	text = urllib.parse.quote_plus(text)
	#text = urllib.pathname2url(text)
	url = TELEGRAM_URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	get_url(url)
	
def echo_all(updates):
	send = False
	for update in updates["result"]:
		try:
			text = update["message"]["text"]
			chat = update["message"]["chat"]["id"]
			print(text)
			
			'''
			
				
			if text == "/weather":
				send = True
				text = "Il tempo al campo nei prossimi 5 dovrebbe essere: \n"
				wjs = get_json_from_url(WEATHER_URL)
				for i in range(0,40):
					text += wjs["list"][i]["dt_txt"] + " " + wjs["list"][i]["weather"][0]["description"] +"\n"
			'''
			
			if text == "/clock":
				send = True
				text = "sono le ore " + datetime.now().strftime("%H:%M:%S") + " " + winkingFace
			
			if text == "(":
				send = True
				text = ")"
				
			if text.lower() == "pasquale":
				send = True
				text = "ricchioncello!"
			
				
			if send:		
				send_message(text, chat)
		except Exception as e:
			print(e)
    
	
def main():
	last_update_id = None
	
	while True:
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			echo_all(updates)
		time.sleep(0.5)
	    

if __name__ == '__main__':
    main()
