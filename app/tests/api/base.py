from app.core.settings import API_KEY_NAME, API_KEY


def get_valid_api_key():
    return {API_KEY_NAME: API_KEY}


def get_invalid_api_key():
    return {API_KEY_NAME: "fake-api-key"}
