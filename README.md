# habr_parser
ITMO magester's class lab

## to_do
- Parse habr.com search pages
- save data in a format of {"title": title, "link": link}
- Text processing (find key topics and definitions(I've used tags), find key trendsetters from the text, and make word cloud based on article's text)

## How To Run

1. Clone repository with ```git clone https://github.com/VKostya/habr_parser.git```
2. Run ```pip install requirements.txt``` command in a folder
3. Run scrapping.py to get a .json file with habr articles
4. Run text_processing.py to process and analyze collected articles

## Results:
- collected 48 repeated tags
- collected 48 repeated "trendsetter" - some of them are key definitions actually

All the results are stored at /static/

Word cloud for blockchain related articles:
![word cloud image](./static/wordcloud.png)
