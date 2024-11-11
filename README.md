# Cryonogen - A Proper Python Package

On 2024JAN20, Cryonogen was re-factored into a proper python package for a containerized deployment.
This project drew inspiration from Aranel Fyre, which is a re-build of Aranel SDT.

```bash
# Setting up the environment
# The first venv is uv's subcommand
# The second venv is the directory
uv venv venv
source ./venv/bin/activate
uv pip install -r pyproject.toml
```

Since `cryo` is a python package (see `pyproject.toml`), it can be installed into the current python environment as an editable installation:

```bash
# To install in editable mode
uv pip install --editable .

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

To prepare the `cryonogen.db` database file:

```bash
# outputs cryonogen.db in $PWD
python to-sqlite.py process \
  --box datasheet/BoxManifest.xlsx \
  --vial datasheet/VialManifest.xlsx
```
