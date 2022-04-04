import requests
from megaloader.http import http_download
from megaloader.validator import validate_artwork_id, validate_creator_id, validate_output, validate_PHPSESSID, validate_url


class Pixiv:
    def __init__(self, creator_id: str, PHPSESSID: str = None):
        validate_creator_id(creator_id)
        self.creator_id = creator_id

        self.__headers = {
            "Accept": "application/json",
        }

        if PHPSESSID is not None:
            validate_PHPSESSID(PHPSESSID)
            self.__headers["Cookie"] = "PHPSESSID=" + PHPSESSID

    def get_user_home(self, top_only: bool = False) -> dict:
        return requests.get("https://www.pixiv.net/ajax/user/" + self.creator_id + "/profile/" + ("top" if top_only else "all") + "?lang=en", headers=self.__headers).json()

    def get_user_home_illusts(self) -> tuple:
        return tuple(self.get_user_home(False)["body"]["illusts"].keys())

    def build_artwork_urls(self, artwork_id: str) -> tuple:
        validate_artwork_id(artwork_id)
        return tuple([illust["urls"]["original"] for illust in requests.get("https://www.pixiv.net/ajax/illust/" + artwork_id + "/pages?lang=en", headers=self.__headers).json()["body"]])

    @staticmethod
    def download_file(url: str, output: str) -> bytes:
        validate_url(url)
        validate_output(output)
        http_download(url, output)
