# configure pyhon virtual environment

```
virtualenv .venv venv  
.\.venv\Scripts\activate
pip install pip-tools
pip-compile requirements.in requirements.in.dev --output-file requirements.txt
pip-sync
pip install -e src/
```

# run test using tox

```
tox
```
