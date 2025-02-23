from paperbot.common import Paper


def get_publish_cfg(config: dict) -> dict:
    """Extract publish configuration values from paperbot config."""
    cfg = dict(
        destinations=config['destinations'],
        discord_credentials=config['discord']['credentials'],
        bluesky_credentials=config['bluesky']['credentials'],
    )

    return cfg


def to_discord(paper: Paper, credentials: str):
    """Publish `paper` to discord using `credentials`."""


def to_bluesky(paper: Paper, credentials: str):
    """Publish `paper` to bluesky using `credentials`."""