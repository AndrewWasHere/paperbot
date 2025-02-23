import requests
import tomllib

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


def to_bluesky(paper: Paper, credentials: str):
    """Publish `paper` to bluesky using `credentials`."""
    print(f'`{msg.format(paper)}` published to bluesky... Once this is implemented.')