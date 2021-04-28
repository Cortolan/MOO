import feedparser
import re

def cleanhtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def scrape_rss(scrape_type = "title"):
  input_file = open(input_file, 'r')
  rss_feed = input_file.readline()
  rss_feed = rss_feed.rstrip()
  
  while rss_feed:
    try:
        news_feed = feedparser.parse(rss_feed)
        return print('The scraping job succeeded: ', news_feed.status_code)
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)
        continue

    for entry in news_feed.entries:
      # Params available summary_detail, published_parsed, links, title, summary, guidislink, title_detail, link, published, id
      if scrape_type == "title":
        print(entry.title)
      if scrape_type == "summary":
        print(cleanhtml(entry.summary))
     
    rss_feed = input_file.readline()
    rss_feed = rss_feed.rstrip()

  input_file.close()


input_file = "rss_links.txt"
scrape_rss()
