import argparse
import os
import tomllib

from paperbot import papers


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


def publish(paper, config):
    print(paper)
    

def main():
    args = parse_command_line()
    config = load_config(args.config)

    paper = choose_paper(config)
    publish(paper, config)


if __name__ == '__main__':
    main()
