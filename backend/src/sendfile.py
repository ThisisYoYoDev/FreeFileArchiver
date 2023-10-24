import requests
from time import sleep
from fastapi.exceptions import HTTPException

from .constants import WEBHOOK, MAX_RETRIES, WAIT_TIME_INITIAL

def sendfile(buffer):
    retries = 0

    while retries < MAX_RETRIES:
        try:
            response = requests.post(next(WEBHOOK), files={
                                     "file[0]": ("rip", buffer)})
            if response.status_code == 429:  # Rate limit see: https://discord.com/developers/docs/topics/rate-limits
                retry_after = response.json().get("retry_after", WAIT_TIME_INITIAL)
                print(f"Rate limited. Retrying in {retry_after} seconds...")
                sleep(retry_after)
                retries += 1
            else:
                response.raise_for_status()
                attachments = response.json().get("attachments", [])
                urls = []
                for attachment in attachments:
                    url = attachment["url"].split(
                        "attachments/")[1].split("/")[:2]
                    urls.append(f"{url[0]}/{url[1]}")
                return urls
            print(f"Retrying... ({retries}/{MAX_RETRIES})")
        except requests.exceptions.RequestException as error:
            print(error)
            return HTTPException(status_code=response.status_code, detail="Failed to send file.")

    return HTTPException(status_code=500, detail=f"Max retries reached. ({retries}/{MAX_RETRIES})")
