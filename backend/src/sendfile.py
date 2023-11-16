import requests
from time import sleep
from .constants import WEBHOOK, WEBHOOK_DICT

size = 0

def sendfile(buffer):
    session = requests.Session()

    while True:
        webhook = next(WEBHOOK)
        remaining = WEBHOOK_DICT[webhook]["x-ratelimit-remaining"]

        if int(remaining) <= 0:
            print("Rate limit exceeded. Trying the next webhook., 2")
            sleep(float(WEBHOOK_DICT[webhook]["x-ratelimit-reset-after"]))
            continue

        try:
            response = session.post(webhook, files={"file[0]": ("rip", buffer)})

            if response.status_code == 429:
                print("Rate limit exceeded. Trying the next webhook., 1")
                sleep(float(response.json()["retry_after"]) + float(WEBHOOK_DICT[webhook]["x-ratelimit-reset-after"]))
                continue

            if response.status_code == 404:
                print(f"sendfile| 404 Webhook {webhook} not found. Removing from list.")
                WEBHOOK_DICT.pop(webhook)
                continue

            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"sendfile| HTTP error occurred: {e}")
            sleep(float(WEBHOOK_DICT[webhook]["x-ratelimit-reset-after"]))
            continue

        [WEBHOOK_DICT[webhook].update({key: response.headers.get(key)}) for key in WEBHOOK_DICT[webhook].keys()]

        attachments = response.json().get("attachments", [])
        urls = []
        for attachment in attachments:
            url = attachment["url"].split("attachments/")[1].split("/")[:2]
            urls.append(f"{url[0]}/{url[1]}")

        global size
        size += len(buffer)
        print(f"Total size: {(size / 1024 / 1024 / 1024):.2f} GB")

        return urls
