from pathlib import Path

from conftest import EXPECTED_FAILURES


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NOTEBOOK_COUNT = 32
EXPECTED_XFAIL_COUNT = 11


def test_all_notebooks_are_in_the_execution_suite() -> None:
    notebooks = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in path.parts
    }

    assert len(notebooks) == EXPECTED_NOTEBOOK_COUNT
    assert set(EXPECTED_FAILURES) <= notebooks
    assert len(EXPECTED_FAILURES) == EXPECTED_XFAIL_COUNT
