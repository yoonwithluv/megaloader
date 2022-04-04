import re
import json
import requests
from megaloader import unentitify
from megaloader.http import http_download
from megaloader.validator import validate_page, validate_tag, validate_url, validate_output, validate_html


class ThotslifeErrorPageNotFound(Exception):
    pass


class ThotslifeResource:
    REGEX_GALLERY = re.compile(
        r'<figure class=".+" id=".+" data-g1-gallery-title="" data-g1-gallery="(\[.*\])" data-g1-share-shortlink="https:\/\/thotslife\.com\/.+\/#.+">')
    REGEX_MEDIA_VIDEO = re.compile(
        r'^<source src="(https:\/\/.+thotslife\.com\/.+)" label="" type="video\/mp4" \/>$', re.M)
    REGEX_MEDIA_IMAGE = re.compile(
        r"^<a href='(https:\/\/thotslife\.com\/wp-content\/uploads\/.+)'>", re.M)

    def __init__(self, html: str) -> None:
        validate_html(html)
        self.__html = html

    @property
    def gallery(self):
        posts = []
        for gallery in self.REGEX_GALLERY.findall(self.__html):
            gallery = json.loads(unentitify(gallery))
            for item in gallery:
                if "full" in item.keys():
                    posts.append(item["full"])

        return posts

    @property
    def media(self):
        media = []
        media.extend(self.REGEX_MEDIA_VIDEO.findall(self.__html))
        media.extend(self.REGEX_MEDIA_IMAGE.findall(self.__html))
        return media


class Thotslife:
    BASE_URL = "https://thotslife.com/tag/"
    REGEX_RESOURCES = re.compile(
        r'<a title=".+" class="g1-frame" href="(https:\/\/thotslife\.com\/.+\/)">')

    def __init__(self, tag: str) -> None:
        validate_tag(tag)
        self.BASE_URL += tag

    def __get_page(self, page: int) -> str:
        validate_page(page)

        url = self.BASE_URL
        if page > 1:
            url += "/page/" + str(page) + "/"

        response = requests.get(url)
        body = response.text

        if "Ooops, sorry! We couldn't find it" in body or \
                response.code == 404:
            raise ThotslifeErrorPageNotFound()

        return body

    def __get_pages(self) -> list:
        i = 1
        pages = []
        while True:
            try:
                page = self.__get_page(i)
            except ThotslifeErrorPageNotFound:
                break
            else:
                pages.append(page)
                i += 1
        print(pages)
        return pages

    def get_resources(self) -> list:
        resources: list = []
        for page in self.__get_pages():
            resources.extend([ThotslifeResource(requests.get(url).text)
                             for url in self.REGEX_RESOURCES.findall(page)])
        return resources

    def export(self) -> list:
        resources = self.get_resources()
        data = []
        for resource in resources:
            gallery = resource.gallery
            media = resource.media

            downloads = [None] * (len(gallery) + len(media))
            total = 0

            for i in range(len(gallery)):
                downloads[i] = gallery[i]
                total += 1

            for i in range(len(media)):
                downloads[total + i] = media[i]

            data.extend(downloads)
        return data

    @staticmethod
    def download_file(url: str, output: str):
        validate_url(url)
        validate_output(output)

        http_download(url, output, custom_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": " (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
            "Referer": "",
            "Origin": "",
            "Connection": "",
            "Sec-Fetch-Dest": "",
            "Sec-Fetch-Mode": "",
            "Sec-Fetch-Site": "",
            "Pragma": "",
            "Cache-Control": ""
        })
