from collections import namedtuple


Paper = namedtuple('Paper', ['title', 'url'])


def get_paper_cfg(config):
    """Extract paper configuration values from paperbot config."""
    cfg = dict(
        repo=config['papers_we_love'],
        history=config['history']['path'],
        depth=config['history']['depth']
    )

    return cfg


def load_history(path: str) -> list:
    try:
        with open(path, 'r') as f:
            history = f.readlines()
    except FileNotFoundError:
        history = []

    return history


def update_history(paper: Paper, history: list, depth: int) -> list:
    new_history = [paper.url] + history
    return new_history[:depth]


def save_history(history: list, path: str):
    with open(path, 'w') as f:
        f.writelines(history)


def select_paper(repo: str, history: list) -> Paper:
    """Select a paper from `repo` that isn't in `history`."""
