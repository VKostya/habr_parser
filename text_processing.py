import json
import logging
import requests
import codecs


def get_key_definitions(url):
    pass


def main():
    with codecs.open("result.json", encoding="utf-8", mode="r") as f:
        json_data = json.load(f)

    json_data = json_data["articles"]
    urls = []
    print(json_data)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="debug/debug.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
    )
    main()
