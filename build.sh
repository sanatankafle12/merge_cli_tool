#!/bin/bash

pip install pyinstaller
pyinstaller --onefile merge_cli.py

echo "Executable created in dist/merge_cli"