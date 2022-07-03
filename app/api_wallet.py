import os
import requests

def create_wallet (uid : str):
    result = requests.post("https://spotifiuby-payments-service.herokuapp.com/wallet",
        params={'user_id': uid},
        headers={'X-API-Key': os.environ['WALLET_API_KEY']})
