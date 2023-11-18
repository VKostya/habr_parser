import datetime
import json
import logging
import requests
import codecs
import asyncio
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import pymorphy2
import nltk


async def get_key_definitions(parsed_page: BeautifulSoup, def_dict: dict):
    all_tags = parsed_page.find_all("a", class_="tm-tags-list__link")
    for tag in all_tags:
        text = tag.text
        if text in def_dict.keys():
            def_dict[text] += 1
        else:
            def_dict[text] = 1


async def get_content(parsed_page: BeautifulSoup):
    all_text = parsed_page.find(
        "div",
        class_="article-formatted-body article-formatted-body article-formatted-body_version-1",
    )
    for code in all_text.select("code"):
        code.decompose()

    return all_text.get_text().rstrip()


async def build_wordcloud(text_lst: list):
    nltk.download("stopwords")
    stop_words = stopwords.words("russian")
    stop_words.extend(["это", "также", "всё", "весь", "который", "мочь"])

    text = " ".join(text_lst)

    from nltk.tokenize import word_tokenize

    nltk.download("punkt")
    text = word_tokenize(text)
    lemmatizer = pymorphy2.MorphAnalyzer()

    def lemmatize_text(tokens):
        text_new = ""
        for word in tokens:
            word = lemmatizer.parse(word)
            text_new = text_new + " " + word[0].normal_form
        return text_new

    text = lemmatize_text(text)
    cloud = WordCloud(width=1000, height=1000, stopwords=stop_words).generate(text)

    plt.imshow(cloud)
    plt.show()

    plt.axis("off")


async def get_trendsetters(parsed_page: BeautifulSoup, ts_dict: dict):
    pass


async def dump_def_key_ts_data(def_dict: dict, authors_dict: dict | None = None):
    date = str(datetime.datetime.now())
    fixed_dict = {}
    for tag in def_dict.keys():
        if def_dict[tag] != 1:
            fixed_dict[tag] = def_dict[tag]
    print(fixed_dict)
    pass


async def main():
    with codecs.open("result.json", encoding="utf-8", mode="r") as f:
        json_data = json.load(f)

    json_data = json_data["articles"]
    urls = [x["href"] for x in json_data]
    test_url = "https://habr.com/ru/articles/323586/"
    tags_dict = {}
    ts_dict = {}
    text = []

    for url in urls:
        try:
            req = requests.get(url)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html.parser")
                # await get_key_definitions(parsed_page=soup, def_dict=tags_dict)
                plain_text = await get_content(parsed_page=soup)
                text.append(plain_text)
                # await get_authors(parsed_page=soup, authors_dict=authors_dict)
        except Exception as e:
            logging.info("could not save data")
            logging.exception("Exception")
    await build_wordcloud(text)
    """
    try:
        req = requests.get(test_url)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "html.parser")
            await get_trendsetters(parsed_page=soup, ts_dict=ts_dict)
    except Exception as e:
        logging.info("could not save data")
        logging.exception("Exception")
    await dump_def_key_ts_data(def_dict=tags_dict)
    """


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="debug/debug.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
    )
    asyncio.run(main())
