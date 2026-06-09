from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent

EXPECTED_FAILURES = {
    "labs/KNN_Lab.ipynb": "imports the Colab-only google.colab package",
    "labs/Lab3_Classification_Intro.ipynb": (
        "contains an instructional XXX placeholder used as Python code"
    ),
    "labs/Preparation_for_Data_Mining_with_Python_in_Colab_Lab1.ipynb": (
        "uses Google Drive paths and Colab-only export commands"
    ),
    "labs/cluster_4482_examples.ipynb": (
        "uses a seaborn scatterplot call incompatible with current seaborn"
    ),
    "labs/titanic lab2.ipynb": (
        "contains an instructional dataframe-name placeholder"
    ),
    "tutorials/4482_KNN_scaled.ipynb": "imports the Colab-only google.colab package",
    "tutorials/4482_classification_MLP_titanic_cleaned.ipynb": (
        "imports the Colab-only google.colab package"
    ),
    "tutorials/Preparation_for_Data_Mining_with_Python_in_Colab_Fall2023.ipynb": (
        "uses Google Drive paths and Colab-only export commands"
    ),
    "tutorials/Titanic data exploration tutorial - EDA.ipynb": (
        "contains an existing Python indentation error"
    ),
    "tutorials/Titanic_data_exploration_tutorial_EDA.ipynb": (
        "uses a pandas box plot call incompatible with current Matplotlib"
    ),
    "tutorials/apriori_tutorial.ipynb": (
        "requires the wget executable, which is not provided by macOS"
    ),
}

CONDITIONAL_XFAILS = {
    "tutorials/apriori_tutorial.ipynb": sys.platform == "darwin",
}

# The Apriori notebook downloads this file on systems that provide wget.
# Remove only files created by the test run, preserving pre-existing files.
GENERATED_FILE_PATTERNS = ("tutorials/sns_baskets.csv*",)

os.environ.setdefault("MPLBACKEND", "Agg")


def _notebook_path(item: pytest.Item) -> str | None:
    path = Path(str(item.path)).resolve()
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return None
    if relative.suffix != ".ipynb":
        return None
    return relative.as_posix()


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pytest_sessionstart(session: pytest.Session) -> None:
    notebooks = sorted(ROOT.rglob("*.ipynb"))
    session.config._notebook_hashes = {path: _digest(path) for path in notebooks}
    session.config._generated_files_present = {
        path
        for pattern in GENERATED_FILE_PATTERNS
        for path in ROOT.glob(pattern)
    }


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    for item in items:
        path = _notebook_path(item)
        if path not in EXPECTED_FAILURES:
            continue
        if not CONDITIONAL_XFAILS.get(path, True):
            continue
        item.add_marker("notebook_xfail")
        item.add_marker(
            pytest.mark.xfail(reason=EXPECTED_FAILURES[path], strict=True)
        )


def pytest_sessionfinish(
    session: pytest.Session, exitstatus: int
) -> None:
    changed = [
        path.relative_to(ROOT).as_posix()
        for path, original_hash in session.config._notebook_hashes.items()
        if not path.exists() or _digest(path) != original_hash
    ]

    generated_after = {
        path
        for pattern in GENERATED_FILE_PATTERNS
        for path in ROOT.glob(pattern)
    }
    for path in generated_after - session.config._generated_files_present:
        path.unlink()

    if changed:
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter is not None:
            reporter.write_sep(
                "=", "Notebook execution modified source files"
            )
            for path in changed:
                reporter.write_line(path)
