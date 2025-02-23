from collections import namedtuple
import os
from random import choice
import re

from paperbot.common import Paper


Repo = namedtuple('Repo', ['path', 'url'])


def get_paper_cfg(config):
    """Extract paper configuration values from paperbot config."""
    cfg = dict(
        repo_path=config['papers_we_love']['path'],
        repo_url=config['papers_we_love']['url'],
        history=config['history']['path'],
        depth=config['history']['depth']
    )

    return cfg


def load_history(path: str) -> list:
    """Load history from `path`."""
    try:
        with open(path, 'r') as f:
            history = f.readlines()
    except FileNotFoundError:
        history = []

    return [l.strip() for l in history]


def update_history(paper: Paper, history: list, depth: int) -> list:
    """Add `paper` to `history`, preserving `depth`."""
    new_history = [paper.url] + history
    return new_history[:depth]


def save_history(history: list, path: str):
    """Save `history` to `path`."""
    h = (l + '\n' for l in history)
    with open(path, 'w') as f:
        f.writelines(h)


def papers_in_readme(root: str, file: str, repo: Repo):
    papers = []
    subdir = root[len(repo.path):]
    base_url = repo.url + '/blob/main' + subdir
    path = os.path.join(root, file)
    with open(path, 'r') as f:
        for line in f:
            m = re.match(r'.*\[(.*)\]\((\S*)\).*', line)
            if not m:
                continue

            title = m[1]

            url = m[2] if m[2].startswith('http') else f'{base_url}/{m[2]}'
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


def select_paper(all_papers: list, history: list) -> Paper | None:
    """Select a paper from `all_papers` that isn't in `history`."""
    if len(all_papers) == 0:
        return None
    
    while True:
        paper = choice(all_papers)
        if paper.url not in history:
            return paper
    