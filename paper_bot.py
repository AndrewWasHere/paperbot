import argparse
import os
from random import choices
import sys

if sys.version_info.major == 3 and sys.version_info.minor < 11:
    import tomli as tomllib
else:
    import tomllib

from paperbot import common, history, papers, publish


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
    paper_cfg = papers.get_paper_cfg(config)
    history = history.load_history(paper_cfg['history'])
    papers_in_repo = papers.get_papers_in_repo(
        paper_cfg['repo_path'], 
        paper_cfg['repo_url']
    )

    lobsters_cfg = lobsters.get_lobsters_cfg(config)
    papers_from_lobsters = lobsters.get_papers_from_lobsters(lobster_cfg)

    pp = [
        common.select_paper(papers_in_repo, history), 
        common.select_paper(papers_from_lobsters, history)
    ]
    if config['publish'] != 0:
        pp = choices(pp, k=min(config['publish'], len(pp)))

    for p in pp:
        history = history.update_history(p, history, paper_cfg['depth'])
        history.save_history(history, paper_cfg['history'])

    return papers


def publish_paper(papers, config):
    publish_cfg = publish.get_publish_cfg(config)
    destinations = publish_cfg['destinations']

    if len(destinations) == 0:
        # No destinations. Print paper to stdout.
        print(papers)
        return
   
    if 'discord' in destinations:
        publish.to_discord(papers, publish_cfg['discord_credentials'])

    if 'bluesky' in destinations:
        publish.to_bluesky(papers, publish_cfg['bluesky_credentials'])
    

def main():
    args = parse_command_line()
    config = load_config(args.config)

    papers = choose_papers(config)
    publish_papers(papers, config)


if __name__ == '__main__':
    main()
