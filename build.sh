#!/bin/bash
set -e
pyflakes3 bootstart/*.py
poetry -vvv build

