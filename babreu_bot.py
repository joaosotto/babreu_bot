import json
import requests
import time
import urllib
from owlready2 import *
    
path = "babreu_japones.owl"   # Add ontology file PATH

onto_path.append(path)
onto = get_ontology("babreu_japones.owl")
onto.load()

TOKEN = "7729071838:AAE2oZg_crMTL8ITvtZ9rydxgymBPYz37VE" # Insert your chatbot token here
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

estado = {}

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        # text = re.sub(r'[^\w\s]', '', text)
        print(chat, text)

        try:

          if ((text.lower() == onto.Q0.comment[0]) and (estado[chat] == 0)):
            question = onto.Q1.comment[0]
            send_message(question, chat)

            estado[chat] = 1
            print(estado)

            return

          # 1 pergunta
          if ((text.lower() == "sim") and (estado[chat] == 1)):
            response = onto.R1.comment[1]
            send_message(response, chat)
            send_sticker(onto.R1.comment[0], chat)

            estado[chat] = 0
            print(estado)

            return

          # 1 pergunta
          if ((text.lower() == "nao") and (estado[chat] == 1)):
            question = onto.Q2.comment[0]
            send_message(question, chat)

            estado[chat] = 2
            print(estado)

            return

          if ((text.lower() == "sim") and (estado[chat] == 2)):
            response = onto.R2.comment[1]
            send_message(response, chat)
            send_sticker(onto.R2.comment[0], chat)

            estado[chat] = 0
            print(estado)

            return

          if ((text.lower() == "nao") and (estado[chat] == 2)):
            question = onto.Q3.comment[0]
            send_message(question, chat)

            estado[chat] = 3
            print(estado)

            return

          if ((text.lower() == "sim") and (estado[chat] == 3)):
            response = onto.R3.comment[1]
            send_message(response, chat)
            send_sticker(onto.R3.comment[0], chat)

            estado[chat] = 0
            print(estado)

            return

          if ((text.lower() == "nao") and (estado[chat] == 3)):
            response = onto.Q4.comment[1]
            send_message(response, chat)

            estado[chat] = 4
            print(estado)

            return

          if ((text.lower() == "nao") and (estado[chat] == 4)):
            response = onto.R4.comment[1]
            send_message(response, chat)

            estado[chat] = 0
            print(estado)

            return

          else:
            send_message(onto.R0.comment[1], chat)
            send_sticker(onto.R0.comment[0], chat)

            #estado[chat] = 0
            print(estado)

            if (estado[chat] == 1):
              question = onto.Q1.comment[0]
              send_message(question, chat) 
            if (estado[chat] == 2):
              question = onto.Q2.comment[0]
              send_message(question, chat) 
            if (estado[chat] == 3):
              question = onto.Q3.comment[0]
              send_message(question, chat) 
            return

        except:
          estado[chat] = 0


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_sticker(sticker_id, chat_id):
    url = URL + "sendSticker?chat_id={}&sticker={}".format(chat_id, sticker_id)
    get_url(url)    

# ======================================================================================

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)

            for update in updates["result"]:
              chat = update["message"]["chat"]["id"]

        time.sleep(0.5)


if __name__ == '__main__':
    main()