from collections import namedtuple
import os
from random import choice
import re

from paperbot.common import Paper
from paperbot.history import get_history_cfg


Repo = namedtuple('Repo', ['path', 'url'])


def get_paper_cfg(config: dict) -> dict:
    """Extract paper configuration values from paperbot config."""
    cfg = dict(
        repo_path=config['papers_we_love']['path'],
        repo_url=config['papers_we_love']['url'],
        **get_history_cfg()
    )

    return cfg


def papers_in_readme(root: str, file: str, repo: Repo):
    def parse_paper(s: str):
        t = u = None

        # Match '* [:scroll:](<papers-we-love url>) [<title>](<original url>)'
        m = re.match(r'\*.*\[:scroll:\]\((\S*)\).*\[(.*?)\]\((\S*)\).*', s)
        if m:
            t = m[2]
            u = m[1] if m[1].startswith('http') else f'{base_url}/{m[1]}'
        else:
            # Match '* [<title>](<url>)...' or '* :scroll: [<title>](<url>)'
            m = re.match(r'\*.*?\[(.*?)\]\((\S*)\).*', s)
            if m:
                t = m[1]
                u = m[2] if m[2].startswith('http') else f'{base_url}/{m[2]}'
        
        return t, u

    papers = []
    subdir = root[len(repo.path):]
    base_url = repo.url + '/blob/main' + subdir
    path = os.path.join(root, file)
    with open(path, 'r') as f:
        buffer = ''
        for line in f:
            if line.startswith('*'):
                title, url = parse_paper(buffer)
                if title and url:
                    papers.append(Paper(title=title, url=url))

                buffer = line.strip()
            else:
                buffer = f'{buffer} {line.strip()}'

        title, url = parse_paper(buffer)
        if title and url:
            papers.append(Paper(title=title, url=url)) 

    return papers


def get_papers_in_repo(path: str, url: str) -> list:
    """Load papers from Papers We Love repo."""
    papers = []
    repo = Repo(path=path, url=url)
    for root, dirs, files in os.walk(path):
        if root == path:
            continue
        for f in files:
            if f == 'README.md':
                papers += papers_in_readme(root, f, repo)
                break

    return papers

