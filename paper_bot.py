import argparse
import os
import tomllib

from paperbot import papers, publish


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


def choose_paper(config):
    paper_cfg = papers.get_paper_cfg(config)
    history = papers.load_history(paper_cfg['history'])
    papers_in_repo = papers.get_papers_in_repo(
        paper_cfg['repo_path'], 
        paper_cfg['repo_url']
    )
    if paper := papers.select_paper(papers_in_repo, history):
        history = papers.update_history(paper, history, paper_cfg['depth'])
        papers.save_history(history, paper_cfg['history'])

    return paper


def publish_paper(paper, config):
    publish_cfg = publish.get_publish_cfg(config)
    destinations = publish_cfg['destinations']

    if len(destinations) == 0:
        # No destinations. Print paper to stdout.
        print(paper)
        return
   
    if 'discord' in destinations:
        publish.to_discord(paper, publish_cfg['discord_credentials'])

    if 'bluesky' in destinations:
        publish.to_bluesky(paper, publish_cfg['bluesky_credentials'])
    

def main():
    args = parse_command_line()
    config = load_config(args.config)

    paper = choose_paper(config)
    publish_paper(paper, config)


if __name__ == '__main__':
    main()
