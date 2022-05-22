import hashlib
import requests
from megaloader.http import http_download

class GoFile:

    def __init__(self):
        self.api_key = self.__get_api_key()

    def export(self, url: str, password: str = None):
        content_id = url[len("https://gofile.io/d/"):]
        url = "https://api.gofile.io/getContent?contentId=" + content_id + \
            "&token=" + self.api_key + "&websiteToken=12345&cache=true"
        if password is not None:
            password = hashlib.sha256(password.encode()).hexdigest()
            url += "&password=" + password
        resources = requests.get(url).json()

        if "contents" not in resources["data"].keys():
            if resources["stats"] == "error-notFound":
                print("Unable to reach " + url)

        contents = resources["data"]["contents"]
        for content in contents.values():
            yield content["link"]


    def download_file(self, url: str, output: str):
        http_download(url, output, custom_headers={
            "Cookie": "accountToken=" + self.api_key,
            "Accept-Encoding": "gzip, deflate, br"
        })

    @staticmethod
    def __get_api_key():
        # Gets a new account token
        data = requests.get("https://api.gofile.io/createAccount").json()
        api_token = data["data"]["token"]
        # Activate the new token
        data = requests.get(
            "https://api.gofile.io/getAccountDetails?token=" + api_token).json()
        if data["status"] != 'ok':
            raise Exception("The account was not successfully activated.")
        return api_token
