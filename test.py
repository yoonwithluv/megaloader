from plugins import Cyberdrop

def main():
    output = "downloads"
    short_code = "bAsFfpMA"

    api = Cyberdrop()
    for u in api.export(short_code):
        api.download_file(u, output)

if __name__ == "__main__":
    main()
