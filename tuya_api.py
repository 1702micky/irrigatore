
import aiohttp
import time
import hmac
import hashlib
import json
import async_timeout

class TuyaApi:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret.encode('utf-8')
        self.access_token = None
        self.token_expire = 0
        self.base_url = "https://openapi.tuyaeu.com"

    async def get_timestamp(self):
        return str(int(time.time() * 1000))

    def sign(self, method, url, t, body=""):
        # String to sign
        payload = f"{self.client_id}{url}{t}{body}"
        sign = hmac.new(self.client_secret, payload.encode("utf-8"), hashlib.sha256).hexdigest().upper()
        return sign

    async def get_token(self):
        url = "/v1.0/token?grant_type=1"
        t = await self.get_timestamp()
        sign = self.sign("GET", url, t)
        headers = {
            "client_id": self.client_id,
            "sign": sign,
            "t": t,
            "sign_method": "HMAC-SHA256",
        }
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(self.base_url + url, headers=headers) as resp:
                    data = await resp.json()
                    if data["success"]:
                        self.access_token = data["result"]["access_token"]
                        self.token_expire = int(data["result"]["expire_time"]) + int(time.time())
                    else:
                        raise Exception(f"Token error: {data}")
        return self.access_token

    async def ensure_token(self):
        if self.access_token is None or time.time() > self.token_expire - 60:
            await self.get_token()

    async def get(self, endpoint):
        await self.ensure_token()
        t = await self.get_timestamp()
        url = f"/v1.0{endpoint}"
        sign = self.sign("GET", url, t)
        headers = {
            "client_id": self.client_id,
            "sign": sign,
            "t": t,
            "sign_method": "HMAC-SHA256",
            "access_token": self.access_token,
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(self.base_url + url, headers=headers) as resp:
                    return await resp.json()

    async def post(self, endpoint, payload):
        await self.ensure_token()
        body = json.dumps(payload)
        t = await self.get_timestamp()
        url = f"/v1.0{endpoint}"
        sign = self.sign("POST", url, t, body)
        headers = {
            "client_id": self.client_id,
            "sign": sign,
            "t": t,
            "sign_method": "HMAC-SHA256",
            "access_token": self.access_token,
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.post(self.base_url + url, data=body, headers=headers) as resp:
                    return await resp.json()
