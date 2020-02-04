from .Api import newApi
from .Auth import auth

api = newApi
Auth = auth

def headers_client_id(client_id):
    headers = {
        'Client-ID': f'{client_id}',
    }
    return headers

def params_user_id(user_id):
    params = {
        'user_id': f'{user_id}'
    }
    return params