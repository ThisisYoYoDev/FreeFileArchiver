import requests
from time import sleep
from fastapi.exceptions import HTTPException
from itertools import cycle
from .constants import WEBHOOK_DICT, MAX_RETRIES, WAIT_TIME_INITIAL, RATE_LIMITS

def sendfile(buffer):
    retries = 3
    session = requests.Session()

    webhook_cycle = cycle(WEBHOOK_DICT)

    while True:
        try:
            webhook = next(webhook_cycle)
            remaining = RATE_LIMITS[webhook]["x-ratelimit-remaining"]

            print(f"Remaining rate limit for {webhook}: {remaining}")

            if remaining == None or int(remaining) > 0:
                headers = WEBHOOK_DICT[webhook]
                response = session.post(webhook, files={"file[0]": ("rip", buffer)}, headers=headers)
                remaining = response.headers.get("x-ratelimit-remaining")

                RATE_LIMITS[webhook]["x-ratelimit-remaining"] = remaining

                if response.status_code == 429:
                    retry_after = response.json().get("retry_after", WAIT_TIME_INITIAL)
                    print(f"Rate limited. Retrying in {retry_after} seconds...")
                    sleep(retry_after)
                    retries += 1
                else:
                    response.raise_for_status()
                    attachments = response.json().get("attachments", [])
                    urls = []
                    for attachment in attachments:
                        url = attachment["url"].split("attachments/")[1].split("/")[:2]
                        urls.append(f"{url[0]}/{url[1]}")
                    return urls
            else:
                print("Rate limit exceeded. Trying the next webhook.")
                
            print(f"Retrying... ({retries}/{MAX_RETRIES})")
        except requests.exceptions.RequestException as error:
            print(error)
            return HTTPException(status_code=500, detail=f"Failed to send file. ({retries}/{MAX_RETRIES})")