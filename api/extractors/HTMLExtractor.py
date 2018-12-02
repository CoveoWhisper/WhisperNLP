import re
import urllib.request
from bs4 import BeautifulSoup

class HTMLExtractor:
    def __init__(self, content):
        self.content = content

    def extractAllText(self):
        soup = BeautifulSoup(self.content, features='html.parser')
        data = soup.findAll(text=True)
        result = filter(visible, data)
        return ' '.join(result)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True