import argparse
import os
from random import choices
import sys

if sys.version_info.major == 3 and sys.version_info.minor < 11:
    import tomli as tomllib
else:
    import tomllib

from paperbot import common, history, lobsters, papers, publish


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c', 
        default=os.path.join(os.path.dirname(__file__), 'paperbot.toml'),
        help='Path to config'
    )
    args = parser.parse_args()
    return args


def expand_path(path):
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)

    return path


def load_config(path):
    with open(path, 'rb') as f:
        cfg = tomllib.load(f)

    cfg['papers_we_love']['path'] = expand_path(cfg['papers_we_love']['path'])
    cfg['history']['path'] = expand_path(cfg['history']['path'])
    cfg['discord']['credentials'] = expand_path(cfg['discord']['credentials'])
    cfg['bluesky']['credentials'] = expand_path(cfg['bluesky']['credentials'])

    return cfg


def choose_papers(config: dict) -> list:
    """Choose papers to publish"""
    history_cfg = history.get_history_cfg(config)
    hist = history.load_history(history_cfg['history'])

    paper_cfg = papers.get_paper_cfg(config)
    papers_in_repo = papers.get_papers_in_repo(
        paper_cfg['repo_path'], 
        paper_cfg['repo_url']
    )

    lobsters_cfg = lobsters.get_lobsters_cfg(config)
    papers_from_lobsters = lobsters.get_papers_from_lobsters(lobsters_cfg)

    pp = [
        common.select_paper(papers_in_repo, hist), 
        common.select_paper(papers_from_lobsters, hist)
    ]
    if config['publish'] != 0:
        pp = choices(pp, k=min(config['publish'], len(pp)))

    for p in pp:
        hist = history.update_history(p, hist, history_cfg['depth'])
        history.save_history(hist, history_cfg['history'])

    return pp


def publish_papers(pp, config):
    publish_cfg = publish.get_publish_cfg(config)
    destinations = publish_cfg['destinations']

    if len(destinations) == 0:
        # No destinations. Print paper to stdout.
        print(pp)
        return
   
    if 'discord' in destinations:
        publish.to_discord(pp, publish_cfg['discord_credentials'])

    if 'bluesky' in destinations:
        publish.to_bluesky(pp, publish_cfg['bluesky_credentials'])
    

def main():
    args = parse_command_line()
    config = load_config(args.config)

    pp = choose_papers(config)
    publish_papers(pp, config)


if __name__ == '__main__':
    main()
