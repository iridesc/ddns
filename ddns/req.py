from retry import retry
import requests


@retry(tries=5, delay=3)
def req(url, method="g", data: dict = None):
    data = data if data else dict()
    if method == "g":
        r = requests.get(url=url, params=data)
    elif method == "p":
        r = requests.post(url=url, json=data)
    r.raise_for_status()
    return r
