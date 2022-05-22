import re
import requests

class Cyberdrop:
    REGEX_MEDIA = r"(?:https:\/\/)[^cdn\.][a-z0-9\-\/\.]+.cyberdrop.(?:to|me)\/[a-z0-9_\-A-Z \(\)\/]+.(?:mp4|mov|m4v|ts|mkv|avi|wmv|webm|vob|gifv|mpg|mpeg|mp3|flac|wav|png|jpeg|jpg|gif|bmp|webp|heif|heic|tiff|svf|svg|ico|psd|ai|pdf|txt|log|csv|xml|cbr|zip|rar|7z|tar|gz|xz|targz|tarxz|iso|torrent|kdbx)"

    def export(self, short_code: str):
        response = requests.get("https://cyberdrop.me/a/" + short_code)
        for url in re.findall(self.REGEX_MEDIA, response.text):
            if "/thumbs/" in url:
                continue
            if "/s/" in url:
                continue
            if url.index("cyberdrop") < 14 or url.index("cyberdrop") > 18:
                continue
            yield url
