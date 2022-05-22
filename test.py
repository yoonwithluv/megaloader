from plugins import GoFile


def main():
    output = "downloads"
    url = "https://gofile.io/d/BsB2uM"
    password = ""
    api = GoFile()
    for u in api.export(url, password):
        api.download_file(u, output)


if __name__ == "__main__":
    main()
