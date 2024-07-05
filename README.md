# Cryonogen - A Proper Python Package

On 2024JAN20, Cryonogen was re-factored into a proper python package for a containerized deployment.
This project drew inspiration from Aranel Fyre, which is a re-build of Aranel SDT.

```bash
# Setting up the environment
python -m venv venv
source ./venv/bin/activate
pip install pipenv

# Installing dependencies
pipenv install \
  Flask==3.0.0 \
  Flask-Cors==4.0.0 \
  pandas==2.1.4 \
  openpyxl==3.1.2 \
  shiv==1.0.4
```

Since `cryo` is a python package (see `pyproject.toml`), it can be installed into the current python environment as an editable installation:

```bash
# To install in editable mode
pip install --editable .

# To compile with shiv
shiv -c cryo -o cryo.pyz --compressed .

# To build the Docker container
docker build --tag cryonogen:latest .
```

Once the container is built, run as follows:

```bash
# run in detached mode (exposing :9091)
docker run --name cryonogen --detach \
  --restart unless-stopped \
  -v $PWD/datasheet:/datasheet \
  -p 9091:9091 \
  cryonogen:latest
```
