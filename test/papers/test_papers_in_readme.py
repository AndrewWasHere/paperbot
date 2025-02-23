import os
from tempfile import gettempdir, TemporaryDirectory
from pytest import fixture

from paperbot.papers import papers_in_readme, Repo


@fixture
def readme():
    """Creates a README.md in a temporary directory under the root tempdir"""
    contents = """# API Design

* [Architectural Styles and the Design of Network-based Software Architectures (REST) by Roy Fielding](https://www.ics.uci.edu/~fielding/pubs/dissertation/fielding_dissertation.pdf)

* :scroll: [Little Manual of API Design](api-design.pdf)
* [A paper that isn't a PDF](https://arxiv.org/10.22345/12345.54321)
"""

    with TemporaryDirectory() as d:
        with open(os.path.join(d, 'README.md'), 'w') as f:
            f.write(contents)
        
        yield d


def test_papers_in_readme(readme):
    # Set up
    root = readme
    subdir = os.path.basename(readme)
    file = 'README.md'
    url = 'http://somewhere.over.the.rainbow'
    repo = Repo(path=gettempdir(), url=url)

    # Execute
    papers = papers_in_readme(root, file, repo)

    # Test
    assert len(papers) == 3
    assert papers[0].title == 'Architectural Styles and the Design of Network-based Software Architectures (REST) by Roy Fielding'
    assert papers[0].url == 'https://www.ics.uci.edu/~fielding/pubs/dissertation/fielding_dissertation.pdf'
    assert papers[1].title == 'Little Manual of API Design'
    assert papers[1].url == url + '/blob/main/' + subdir + '/' + 'api-design.pdf'
    assert papers[2].title == "A paper that isn't a PDF"
    assert papers[2].url == 'https://arxiv.org/10.22345/12345.54321'
