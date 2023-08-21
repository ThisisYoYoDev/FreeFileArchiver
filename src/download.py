from base64 import b85decode
import requests
from concurrent.futures import ThreadPoolExecutor


def download_chunk_data(file_id):
    try:
        file_id = b85decode(bytes.fromhex(file_id)).decode("utf-8")
    except Exception as e:
        print(e)
        return {"error": "Invalid file id."}

    response = requests.get(
        f"https://cdn.discordapp.com/attachments/{file_id}/data")
    response.raise_for_status()
    data = response.json()

    with ThreadPoolExecutor() as executor:
        futures = {}
        for i, url in enumerate(data["id"]):
            future = executor.submit(
                requests.get, f"https://cdn.discordapp.com/attachments/{url}/rip")
            futures[i] = future

    return (futures, data["name"])


def iterfile(futures):
    for _, future in futures.items():
        result = future.result()
        yield result.content
