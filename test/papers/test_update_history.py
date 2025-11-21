from paperbot.history import update_history, Paper


def test_update_history_empty():
    """Update an empty history"""
    # Set up
    title = 'title'
    url = 'url'

    paper = Paper(title, url)

    # Execute
    h = update_history(paper, [], 100)

    # Validate
    assert len(h) == 1
    assert h[0] == url


def test_update_history_not_full():
    """Update a history not containing its full depth of files"""
    # Set up
    depth = 4
    h_before = [f'url{idx}' for idx in range(depth // 2)][::-1]
        
    # Execute
    paper = Paper(title=f'title{depth}', url=f'url{depth}')
    h_after = update_history(paper, h_before, depth)

    # Validate
    assert len(h_after) == len(h_before) + 1
    assert h_after[-1] == 'url0'
    assert h_after[0] == paper.url


def test_update_history_full():
    """Update a history containing its full depth of files"""
    # Set up
    depth = 4
    h_before = [f'url{idx}' for idx in range(depth)][::-1]
        
    # Execute
    paper = Paper(title=f'title{depth}', url='url{depth}')
    h_after = update_history(paper, h_before, depth)

    # Validate
    assert len(h_after) == len(h_before) == depth
    assert h_after[-1] != 'url0'
    assert h_after[0] == paper.url
