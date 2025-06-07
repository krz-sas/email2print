import imaplib
import email
import os
import sys
import yaml
import requests
import json

from pathlib import Path

def upload_to_paperless(info, config):
    print(info)
    #login
    headers =  {"Authorization": f"Token {config['paperless_token']}", "accept": "application/json"}
    for f in info["files"]:
        data = {"document": (f, open(Path(config['dl_location']) / f, 'rb'))}
        #, "title": f"{info['from']} {info['subject']} {f}"}
        response = requests.post(config['paperless_host'] + '/api/documents/post_document/', headers=headers, files=data)
        print(response.json()) 

def read_config():
    with open("config.yaml") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        return None

config = read_config()

if config is None:
    print("Configuration not found")
    sys.exit(1)

server = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
server.login(config['user'], config['password'])
server.select('Print')

msg_ids=[]
resp, messages = server.search(None, 'UNSEEN')
if len(messages) > 0:
    print ("Found pending prints, proceeding to downloading attachment.")

for message in messages[0].split():
    typ, data = server.fetch(message, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    #looking for 'Content-Type: application/pdf
    paperlessInfo = {}
    paperlessInfo["from"] =  msg.get("From", "Unknown")
    paperlessInfo["subject"] = msg.get("Subject", "Unspecified")
    paperlessInfo["files"] = set()
    for part in msg.walk():
        file_path = part.get_filename()
        if not file_path is None:
            print(f"Attachment mimetype is: {part.get_content_type()}")
            with open(Path(config['dl_location']) / file_path, 'wb') as f:
                f.write(part.get_payload(decode=True))
                os.system(f'lp -d {config["printer"]} {config["printer_params"]} \"{Path(config["dl_location"]) / file_path}\"')

            if part.get_content_type() == "application/pdf":
                paperlessInfo["files"].add(file_path)

    if config['paperless_enable'] and len(paperlessInfo["files"]) > 0:
        upload_to_paperless(paperlessInfo, config)
