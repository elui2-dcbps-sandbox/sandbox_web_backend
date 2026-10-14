# Synthetic backend sandbox

Public rehearsal app. All code and content here are synthetic. The deliberately
old `urllib3` pin exists solely to exercise a dependency-fix workflow.
No network request is made by the app or its tests.

Run `uv sync` and `uv run pytest`.
