import os
import requests


def create_wallet(uid: str):
    requests.post(
        os.environ["PAYMENTS_SERVICE_URL"] + "/wallet",
        params={'user_id': uid},
        headers={'X-API-Key': os.environ['WALLET_API_KEY']})
