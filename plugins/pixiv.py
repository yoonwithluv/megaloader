import requests

class Pixiv:

    def __init__(self, creator_id: str, PHPSESSID: str = None):
        self.creator_id = creator_id
        self.__headers = {
            "Accept": "application/json",
        }
        if PHPSESSID is not None:
            self.__headers["Cookie"] = "PHPSESSID=" + PHPSESSID

    def get_user_home(self, top_only: bool = False):
        return requests.get("https://www.pixiv.net/ajax/user/" + self.creator_id + "/profile/" + ("top" if top_only else "all") + "?lang=en", headers=self.__headers).json()

    def get_user_home_illusts(self):
        return tuple(self.get_user_home(False)["body"]["illusts"].keys())

    def build_artwork_urls(self, artwork_id: str):
        return tuple([illust["urls"]["original"] for illust in requests.get("https://www.pixiv.net/ajax/illust/" + artwork_id + "/pages?lang=en", headers=self.__headers).json()["body"]])
