import time
import hmac
import hashlib

import requests
import json

class APIClient():    
    def __init__(self, api_key, shop_id):
        self.api_key = api_key
        self.shop_id = shop_id

    def _send_http_request(self, api_method, data):
        data = {
            "shop_id": self.shop_id,
            **data
        }

        # По умолчанию питон json.dumps добавляет пробелы в JSON
        # Но php метод json_encode их не добавляет.
        jsoned_data = json.dumps(data, separators=(',', ':'))

        sign = hmac.digest(
            self.api_key.encode(),
            jsoned_data.encode(),
            'sha256'
        ).hex()

        resp = requests.post(f"https://tegro.money/api/{api_method}/",
            data=jsoned_data,
            headers={
                "Authorization": f'Bearer {sign}',
            }
        )
        return resp.json()

    def api_call(self, api_method, params={}, nonce=None):
        if nonce == None:
            nonce = int(time.time())
        return self._send_http_request(api_method, {"nonce": nonce, **params})
