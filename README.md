# 4482_fall_2026

Welcome to the code base for your Fall 4482 Class. Simply click the "open in Colab" icon on any jupyter notebook to open the file in Colab. Make sure to immediately save a copy if you want to modify the code in any way or you will lose your work!

## Testing notebooks

The notebooks remain in their teaching directories and are executed in place
with pytest and nbmake. Test execution does not write cell output back to the
source notebooks.

Create a Python 3.11 virtual environment, install the pinned test dependencies,
and run pytest from the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --requirement requirements-notebook-tests.txt
python -m pytest
```

The suite runs sequentially, uses the `python3` kernel and headless Matplotlib,
and permits up to 600 seconds for each cell. Dataset URLs are intentionally
accessed live, so unavailable network resources fail the test.

Eleven notebooks currently have expected-failure entries in `conftest.py`
because they contain Colab-only operations, instructional placeholders,
version-incompatible plotting code, a known syntax error, or a platform-only
shell dependency. The `wget` entry applies only on macOS; it executes normally
on Ubuntu CI. A strict expected failure still executes the notebook. After
repairing one, remove its entry from `EXPECTED_FAILURES`; an unexpected pass
fails the suite so that this registry cannot become stale.

GitHub Actions runs the same command for every push and pull request.
