import requests
from megaloader.http import http_download
from megaloader.validator import validate_output, validate_url, validate_creator_id


class Fanbox:
    BASE_API_URL = "https://api.fanbox.cc"

    def __init__(self, creator_id: str) -> None:
        validate_creator_id(creator_id)
        self.creator_id = creator_id

    def execute_api(self, endpoint: str, required_creator_id: bool = True):
        endpoint = endpoint.replace(self.BASE_API_URL, "")
        url = self.BASE_API_URL + endpoint

        if required_creator_id and "creatorId" not in url:
            url += ("&" if endpoint.startswith("?") else "?") + \
                "creatorId=" + self.creator_id

        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://" + self.creator_id + ".fanbox.cc/",
            "Origin": "https://" + self.creator_id + ".fanbox.cc"
        }).json()

        if "body" in response:
            return response["body"]

        if "items" in response:
            return response["items"]

        return response

    def export(self):
        return [self.creator, self.banner, next(self.plan_thumbnails), next(self.carousel), next(self.posts)]

    @staticmethod
    def download_file(url: str, output: str):
        if url is None:
            return
        validate_url(url)
        validate_output(output)
        http_download(url, output)

    @property
    def creator(self) -> dict:
        return self.execute_api("/creator.get")

    @property
    def paginate_creator(self) -> list:
        return self.execute_api("/post.paginateCreator")

    @property
    def banner(self) -> str:
        return self.creator["coverImageUrl"]

    @property
    def posts(self):
        for url in self.paginate_creator:
            response = self.execute_api(url)
            for post in response["items"]:
                response = self.execute_api(
                    "/post.info?postId=" + post["id"], False)
                if "body" in response.keys() and response["body"] is not None \
                    and "images" in response["body"].keys():
                        for image in response["body"]["images"]:
                            yield image["originalUrl"]
                else:
                    yield response["coverImageUrl"]

    @property
    def carousel(self):
        response = self.execute_api("/creator.get")
        for i in response["profileItems"]:
            yield i["imageUrl"]

    @property
    def plan_thumbnails(self):
        response = self.execute_api("/plan.listCreator")
        for p in response:
            if "coverImageUrl" in p and p["coverImageUrl"]:
                yield p["coverImageUrl"]
