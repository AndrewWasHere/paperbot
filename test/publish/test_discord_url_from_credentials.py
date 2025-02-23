from tempfile import NamedTemporaryFile

from pytest import fixture

from paperbot.publish import discord_url_from_credentials


@fixture
def url():
    return 'https://pretend.discord.url'

@fixture
def credentials(url):
    with NamedTemporaryFile() as f:
        f.write(f'url = "{url}"'.encode())
        f.seek(0)
        yield f.name


def test_discord_url_from_credentials(url, credentials):
    credentials_url = discord_url_from_credentials(credentials)

    assert credentials_url == url
