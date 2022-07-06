import re
import requests
import json
from megaloader.http import http_download

REGEX_BUILD_ID_PATT = 'buildId":".+",'

class Bunkr:
    def __init__(self, url: str) -> None:
        self.__url = url

    @property
    def url(self):
        return self.__url

    def getBuildId(self, resText):
        return re.findall(REGEX_BUILD_ID_PATT, resText)[0].split(":")[1].strip(",").strip('"')
    
    def getNextUrl(self, url, buildId, isAlbum = True):
        valToReplace = "/a/" if isAlbum else "/v/"
        url = url.replace(valToReplace,f"/_next/data/{buildId}{valToReplace}") + ".json"
        return url

    def export(self):
        response = requests.get(self.url)
        buildId = self.getBuildId(response.text)
        # is album
        if "/a/" in self.url:
            nextUrl = self.getNextUrl(self.url, buildId)
            files = json.loads(requests.get(nextUrl).text)["pageProps"]["files"]
            for url in files:
                yield url["cdn"].replace("cdn","media-files")+"/"+url["name"]
        # is specific resource
        else:
            nextUrl = self.getNextUrl(self.url, buildId, False)
            file = json.loads(requests.get(nextUrl).text)["pageProps"]["file"]
            domain = file["mediafiles"]
            name = file["name"]
            yield f"{domain}/{name}"

    def download_file(self, url: str, output: str):
        http_download(url, output, custom_headers=None, headers_required=False)
