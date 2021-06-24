import feedparser
import re
import os
from datetime import date

FILE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
INPUT_FILE = "{}/rss_links.txt".format(FILE_DIRECTORY)



def clean_text(text):
    clean_html = re.compile('<.*?>')
    clean_html = re.sub(clean_html, '', text)
    clean_string_formating = clean_html.join(
        s for s in text if ord(s) > 31 and ord(s) < 126)
    return clean_string_formating


def scrape_rss(scrape_type="title"):
    input_file = open(INPUT_FILE, 'r')
    rss_feed = input_file.readline()
    rss_feed = rss_feed.rstrip()
    output = []

    while rss_feed:
        try:
            news_feed = feedparser.parse(rss_feed)
        except Exception as e:
            print('The scraping job failed on {feed}. See exception: '.format(
                feed=rss_feed))
            print(e)
            rss_feed = input_file.readline()
            rss_feed = rss_feed.rstrip()
            continue

        for entry in news_feed.entries:
            if scrape_type == "title":
                output.append(entry.title)
            if scrape_type == "summary":
                output.append(clean_text(entry.summary))

        rss_feed = input_file.readline()
        rss_feed = rss_feed.rstrip()

    input_file.close()
    return output
