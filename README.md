# Megaloader

### Introduction
This project will make you smile. It allows you to use some download plugins for many websites such as :
- [Cyberdrop](http://www.cyberdrop.me/),
- [Fanbox](https://www.fanbox.cc),
- [GoFile](http://www.gofile.io/),
- [Pixiv](http://www.pixiv.net/),
- [Rule34](http://www.rule34.xxx/),
- [ThotsLife](http://www.thotslife.com/).
- [ThotHub](http://www.thothub.vip/).

The list may grow, but at the moment, it's all about NSFW. Cyberdrop, GoFile, Thotslife and ThotHub are knowned to host some leaks about nudity, while Rule34, Pixiv and Fanbox are hosting some hentai arts.

### Setup
In order to make the project working without error, you need to install the modules in ``requirements.txt``. You can achieve this using the following command :

```bash
python3 -m pip install -r requirements.txt
```

### Goal
The goal of this project is to create script to download all content from a specific website and make it as a plugin using the Megaloader HTTP request, made using native modules only, and a validator to check that you're not wrongly using plugins.

### Why ?
I'm interested in the download automation. Sometimes it's easy to make, sometimes it's not. But everytime I do a downloader that works, I put it on GitHub using a new repository. This time, I'm going to make a Monolith repository containing all my downloader adapted for a plugin form.

### Contribution
If you want to contribute, you can either make a pull request to patch an error in a Megaloader's plugin, or create yours which I just have to validate before merging.

If you're facing any error, please, open an issue.

### Thanks
Thanks for the support you're giving to me, it makes me happy to see a new star notification.

### Other way to support
If you want to support me in depth, you can [donate me here](https://www.paypal.me/quatrecentquatre). Thanks to futur donators.

# Snippets

### Introduction
Below, you will be able to see many snippets on existing plugins to see how it can be used. Sure, you're gonna need to see in depth the source code of each plugin because some don't work the same as other, since some websites asks for certain auth token, or else, and other don't.

### Cyberdrop

```python
from plugins import Cyberdrop

def main():
    output = "downloads"
    short_code = "CYBERDROP_FOLDER_ID"

    api = Cyberdrop()
    for u in api.export(short_code):
        api.download_file(u, output)

if __name__ == "__main__":
    main()
```

### GoFile

```python
from plugins import GoFile

def main():
    output = "downloads"
    url = "GOFILE_FOLDER_URL"
    password = "PASSWORD_IF_REQUIRED" or None

    api = GoFile()
    for u in api.fetch_resources(url, password):
        api.download_file(u, output)

if __name__ == "__main__":
    main()
```

### Rule34

```python
from plugins import Rule34

def main():
    output = "downloads"
    tags = ["girl", "hot"] # tags example

    api = Rule34(tags)
    for u in api.export():
        api.download_file(u, output)

if __name__ == "__main__":
    main()
```