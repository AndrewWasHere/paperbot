from paperbot.common import Paper


def get_history_cfg(config):
    """Returns history configuration as a dict"""
    cfg = dict(
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

