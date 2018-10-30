import json
import requests
import time
import urllib
import urllib.parse
import re
import csv
import string
import os.path

TOKEN = open('key.txt', 'r').read().rstrip()
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
triggers = {}


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = False
    try:
        js = get_json_from_url(url)
    except Exception as e:
        print(e)
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
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            response = respond(text).encode("utf-8")
            send_message(response, chat)
        except Exception as e:
            print("Error in echo all: {}".format(e))


def respond(text):
    message = ""
    rem_punc = re.compile('[%s]' % re.escape(string.punctuation))
    command = text.split(' ', 1)[0]

    if command == '/start' or command == '/start@RU_Dad_bot':
        return "Hoi, ik ben Dad en je hebt me nu getriggerd. Je kan nieuwe trigger toevoegen met /add."

    if command == '/add' or command == '/add@RU_Dad_bot':
        try:
            value = text.split(' ', 1)[1]
            trigger, response = value.split(':', 1)
        except Exception as e:
            print("no keyword given\n{}".format(e))
            return "Add a new trigger by typing your trigger and response after /add, seperated by a colon (:)!"
        trigger = rem_punc.sub('', trigger.strip())
        # if trigger in triggers.keys():
        #     return "Wollah deze key bestaat al!\n"
        response = response.strip()
        write_triggers(trigger, response)
        return "Trigger toegevoegd!\n"

    # Respond to deletion of trigger words
    if command == '/delete' or command == '/delete@RU_Dad_bot':
        value = text.split(' ', 1)[1]
        del triggers[value]
        write_triggers()
        return '{} is verwijderd uit de triggers.'.format(value)

    if command == '/triggers' or command == '/triggers@RU_Dad_bot':
        try:
            value = text.split(' ', 1)[1]
            if value == "all":
                for key in triggers.keys():
                    message += "{}: {}\n".format(key, triggers[key])
                return message
        except Exception as e:
            pass
            # print("No second argument for trigger command given: {}".format(e))
        for key in triggers.keys():
            message += key + '\n'
        return message

    # Respond to 'I am'
    if re.search(r'ik ben \w+', text, re.I):
        matches = re.search(r'ik ben (\w+)', text, re.IGNORECASE)
        message += "Hoi {}, ik ben Dad Bot\n".format(matches.group(1))

    # Respond to added triggers
    text = rem_punc.sub('', text)
    for word in triggers.keys():
        regex = r'\b' + word + r'\b|\A' + word + r'\b '
        if re.search(regex, text, re.I):
            message += triggers[word]
    return message


def write_triggers(trigger='', response=''):
    if trigger != '' and response != '':
        triggers[trigger] = response
    with open('triggers.csv', 'w') as f:
        [f.write('{0};{1}\n'.format(key, value)) for key, value in triggers.items()]


def read_triggers():
    if os.path.isfile('triggers.csv'):
        with open('triggers.csv', mode='r') as infile:
            reader = csv.reader(infile, delimiter=';')
            try:
                for row in reader:
                    triggers[row[0]] = row[1]
            except Exception as e:
                print("There was an error with reading the csv file.\n{}".format(e))


def main():
    read_triggers()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates:
            if "result" in updates.keys():
                if len(updates["result"]) > 0:
                    last_update_id = get_last_update_id(updates) + 1
                    echo_all(updates)
            else:
                print("Bot was not found\n{}".format(updates))
        time.sleep(0.5)


if __name__ == '__main__':
    main()
