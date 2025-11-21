from collections import namedtuple


Paper = namedtuple('Paper', ['title', 'url'])


def select_paper(all_papers: list[Paper], history: list):
    """Select a paper from `all_papers` that isn't in `history`."""
    if len(all_papers) == 0:
        return None
    
    while True:
        paper = choice(all_papers)
        if paper.url not in history:
            return paper
    