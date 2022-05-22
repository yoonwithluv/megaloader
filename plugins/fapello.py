import re
import requests
from megaloader.http import http_download

class Fapello:
    REGEX_VIDEO = r"^\s+<video.*src=\"(https:\/\/cdn.fapello.com\/content.+)\".*<\/video>$"
    REGEX_IMAGE = r"^\s+<img src=\"(https:\/\/fapello.com\/content\/.+)\" alt=\".+\">$"

    def __get_all_ajax_pages(self, model: str):
        i = 0
        while True:
            url = "https://fapello.com/ajax/model/{}/page-{}/".format(model, i)
            page = requests.get(url)
            if len(page.text) < len("DOCTYPE"):
                break
            i += 1
            yield page.text


    def __get_hyper_text_links(self, page: str, model: str):
        return re.findall(r"https://fapello.com/[a-zA-Z0-9\-_\.]+/\d+", page, re.M)


    def __get_medias_from_page(self, page_url: str):
        page = requests.get(page_url).text
        f = re.findall(self.REGEX_VIDEO, page, re.M)
        f.extend(re.findall(self.REGEX_IMAGE, page, re.M))
        return f

    def export(self, model: str):
        """ Yields a media URL for each iteration. """
        for page in self.__get_all_ajax_pages(model):
            external = [l for l in self.__get_hyper_text_links(page, model)]
            links = [l for e in external for l in self.__get_medias_from_page(e)]
            for l in links:
                yield l

    @staticmethod
    def download(url: str, output: str):
        http_download(url, output)
