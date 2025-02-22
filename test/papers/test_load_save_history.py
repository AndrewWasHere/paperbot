from tempfile import NamedTemporaryFile

from paperbot.papers import load_history, save_history


def test_load_empty_history():
    # Set up
    with NamedTemporaryFile() as f:
        # Execute
        h = load_history(f.name)

    # Validate
    assert len(h) == 0


def test_load_missing_history():
    # No set up required

    # Execute
    h = load_history('')

    # Validate
    assert len(h) == 0


def test_save_and_load_history():
    # Set up
    h_before = ['1', '2', '3']

    # Execute
    with NamedTemporaryFile() as f:
        save_history(h_before, f.name)

        f.seek(0)
        h_after = load_history(f.name)

    # Validate
    assert h_after == h_before
