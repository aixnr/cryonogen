#!/usr/bin/env bash
set -eu

TARGET=cryonogen

mkdir /tmp/${TARGET}
rsync -azh --info=progress2 --exclude venv --exclude build --exclude cryonogen.egg-info --exclude __pycache__ * /tmp/${TARGET}/
tar -I 'zstd -19' -cf $HOME/Downloads/${TARGET}_$(date +"%Y-%m-%d").tar.zst --directory=/tmp/ ${TARGET}
rm -rf /tmp/${TARGET}
