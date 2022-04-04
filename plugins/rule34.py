import math
import requests
import xml.etree.ElementTree as XML_ET
from megaloader.http import http_download
from megaloader.validator import validate_output, validate_tags, validate_url, validate_pid, validate_limit


class Rule34:
    def __init__(self, tags: list) -> None:
        validate_tags(tags)
        self.__tags = tags

    def api_url_builder(self, pid: int = 0, limit: int = 100) -> str:
        validate_pid(pid)
        validate_limit(limit)
        return "https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}&pid={}&limit={}".format(",".join(self.__tags), pid, limit)

    def export(self) -> list:
        pid = 0
        limit = 100
        urls = []
        while True:
            url = self.api_url_builder(pid=pid)
            data = requests.get(url).text
            data = XML_ET.fromstringlist([data])
            total_posts = int(data.get("count"))
            posts = data.iter("post")

            urls.extend([post.get("file_url") for post in posts])

            pid_limit = math.ceil(total_posts / limit)
            if pid_limit == pid:
                break

            pid += 1

        return urls

    @staticmethod
    def download_file(url: str, output: str):
        validate_url(url)
        validate_output(output)
        http_download(url, output)
