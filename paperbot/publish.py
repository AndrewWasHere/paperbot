import sys
if sys.version_info.major == 3 and sys.version_info.minor < 11:
    import tomli as tomllib
else:
    import tomllib

import requests

from paperbot.common import Paper

msg = "'{0.title}' @ {0.url}"

def to_discord(papers: list[Paper], webhook: str, name: str):
    """Publish `papers` to discord using `webhook`."""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    content = f'How about reading {" or ".join([msg.format(paper) for paper in papers])}?'
    body = {
        'content': content
    }
    resp = requests.post(webhook, headers=headers, json=body)
    print(f'`{content}` published to {name}. resp={resp.status_code}')
