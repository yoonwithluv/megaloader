import re
import requests
from megaloader.http import http_download
from megaloader.validator import validate_url, validate_short_code, validate_output


class Cyberdrop:
    @staticmethod
    def export(short_code: str) -> list:
        validate_short_code(short_code)

        response = requests.get("https://cyberdrop.me/a/" + short_code)
        html = response.text
        matchs = re.findall(
            r"(?:https:\/\/)[^cdn\.][a-z0-9\-\/\.]+.cyberdrop.(?:to|me)\/[a-z0-9_\-A-Z \(\)\/]+.(?:mp4|mov|m4v|ts|mkv|avi|wmv|webm|vob|gifv|mpg|mpeg|mp3|flac|wav|png|jpeg|jpg|gif|bmp|webp|heif|heic|tiff|svf|svg|ico|psd|ai|pdf|txt|log|csv|xml|cbr|zip|rar|7z|tar|gz|xz|targz|tarxz|iso|torrent|kdbx)", html)

        urls = []
        for url in matchs:
            if "/thumbs/" in url:
                continue
            if "/s/" in url:
                continue
            if url.index("cyberdrop") < 14 or url.index("cyberdrop") > 18:
                continue
            if url not in urls:
                urls.append(url)

        return urls

    @staticmethod
    def download_file(url: str, output: str):
        validate_url(url)
        validate_output(output)
        http_download(url, output)
