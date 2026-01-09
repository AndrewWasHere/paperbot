from bs4 import BeautifulSoup
import requests
from paperbot.common import Paper
from paperbot.history import get_history_cfg


def read_lobsters_rss(rss: str) -> list:
    """Extract [Paper(title, url), ...] from lobsters rss feed"""
    resp = requests.get(rss)
    if resp.status_code != 200:
        return []

    soup = BeautifulSoup(resp.text, 'xml')
    return [
        Paper(item.title.text, item.link.text) 
        for item in soup.find_all('item') 
        if 'lobste.rs' not in item.link
    ]


def read_lobsters_front_page(url: str) -> list:
    """Extract [Paper(title, url), ...] from lobsters main page"""
    resp = requests.get(url)
    if resp.status_code != 200:
        return []
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    articles = soup.find_all('a', class_='u-url')
    return [Paper(a.text, a['href']) for a in articles]


def get_papers_from_lobsters(config: dict) -> list:
    """Return list of papers from lobsters"""
    papers = read_lobsters_rss(config['rss'])
    if len(papers) == 0:
        papers = read_lobsters_front_page(config['url'])

    return papers