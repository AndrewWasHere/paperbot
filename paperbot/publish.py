import sys
if sys.version_info.major == 3 and sys.version_info.minor < 11:
    import tomli as tomllib
else:
    import tomllib

import requests

from atproto import Client, client_utils

from paperbot.common import Paper

msg = "How about reading '{0.title}' @ {0.url} ?"

def get_publish_cfg(config: dict) -> dict:
    """Extract publish configuration values from paperbot config."""
    cfg = dict(
        destinations=config['destinations'],
        discord_credentials=config['discord']['credentials'],
        bluesky_credentials=config['bluesky']['credentials'],
    )

    return cfg


def discord_url_from_credentials(path: str) -> str:
    with open(path, 'rb') as f:
        cfg = tomllib.load(f)

    url = cfg['url']

    return url


def to_discord(paper: Paper, credentials: str):
    """Publish `paper` to discord using `credentials`."""
    url = discord_url_from_credentials(credentials)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    content = msg.format(paper)
    body = {
        'content': content
    }
    resp = requests.post(url, headers=headers, json=body)
    print(f'`{content}` published to discord. resp={resp.status_code}')


def bluesky_extract_from_credentials(path: str) -> tuple:
    with open(path, 'rb') as f:
        cfg = tomllib.load(f)

    user = cfg['user']
    pw = cfg['pw']

    return user, pw


def to_bluesky(paper: Paper, credentials: str):
    """Publish `paper` to bluesky using `credentials`."""
    user, pw = bluesky_extract_from_credentials(credentials)
    content = client_utils.TextBuilder().text(
        f'How about reading '
    ).link(
        f'"{paper.title}"', 
        paper.url
    ).text(
        '?'
    )
    client = Client()
    client.login(user, pw)
    client.send_post(text=content)
    print(f'`How about reading ["{paper.title}"]({paper.url})?` published to bluesky.')