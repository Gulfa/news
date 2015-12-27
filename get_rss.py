import feedparser
from datetime import datetime
from dateutil.parser import parse
from html.parser import HTMLParser

delchars = dict( (ord(c),None) for c in map(chr, range(256)) if not c.isalnum())

class myHTMLparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = ""
    def handle_data(self, data):
        self.content += data

def consume_feed(url):
    feed = feedparser.parse(url)
    data = {"title":feed["channel"]["title"],
            "items":[]}

    for item in feed["items"]:
        data["items"].append(get_data(item))
    return data
        
def get_data(item):
    date = parse(item["published"])
    title_words = to_words(item["title"])
    parser = myHTMLparser()
    parser.feed(item["description"])
    description_words = to_words(parser.content)
    return {"date":date, "title":title_words, "story":description_words}

def to_words(string):
    words = string.split()
    return [w.strip().lower().translate(delchars) for w in words]

guardian_url = "http://www.theguardian.com/uk-news/rss"
print(consume_feed(guardian_url))
