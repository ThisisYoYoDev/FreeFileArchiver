import requests
from time import sleep
from fastapi.exceptions import HTTPException
from .constants import WEBHOOK, WEBHOOK_DICT

def sendfile(buffer):
    session = requests.Session()

    while True:
        try:
            webhook = next(WEBHOOK)
            remaining = WEBHOOK_DICT[webhook]["x-ratelimit-remaining"]
            print(f"Remaining rate limit for {webhook.split('/')[-1]}: {remaining}")

            if remaining == None or int(remaining) > 0:
                response = session.post(webhook, files={"file[0]": ("rip", buffer)})
                [WEBHOOK_DICT[webhook].update({key: response.headers.get(key)}) for key in WEBHOOK_DICT[webhook].keys()]

                response.raise_for_status()
                attachments = response.json().get("attachments", [])
                urls = []
                for attachment in attachments:
                    url = attachment["url"].split("attachments/")[1].split("/")[:2]
                    urls.append(f"{url[0]}/{url[1]}")
                return urls
            else:
                print("Rate limit exceeded. Trying the next webhook.")
        except requests.exceptions.RequestException as error:
            print(error)
            return HTTPException(status_code=500, detail=f"Error: {error}")
