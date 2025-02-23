import argparse
import os
import tomllib

import paperbot


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c', 
        default=os.path.join(os.path.dirname(__file__), 'paperbot.toml'),
        help='Path to config'
    )
    args = parser.parse_args()
    return args


def load_config(path):
    with open(path, 'rb') as f:
        cfg = tomllib.load(f)

    return cfg


def choose_paper(config):
    paper_cfg = paperbot.papers.get_paper_cfg(config)
    history = paperbot.papers.load_history(paper_cfg['history'])
    repo = paperbot.papers.load_repo(paper_cfg['repo_path'], paper_cfg['repo_url'])
    paper = paperbot.papers.select_paper(repo, history)
    history = paperbot.papers.update_history(paper, history, paper_cfg['depth'])
    paperbot.papers.save_history(history, paper_cfg['history'])

    return paper


def publish(paper, config):
    pass
    

def main():
    args = parse_command_line()
    config = load_config(args.config)

    paper = choose_paper(config)
    publish(paper, config)


if __name__ == '__main__':
    main()
