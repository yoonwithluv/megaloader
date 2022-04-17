from plugins import GoFile

def main():
    output = "downloads"
    url = "https://gofile.io/d/CDruHU"
    password = "None"

    api = GoFile()
    for u in api.fetch_resources(url, password):
        api.download_file(u, output)

if __name__ == "__main__":
    main()
