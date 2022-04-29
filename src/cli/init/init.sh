if (-not (Test-Path .venv)) {mkdir .venv}; pipenv install --requirements requirements.txt --ignore-pipfile --no-site-packages --skip-lock;
