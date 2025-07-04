#!/usr/bin/env bash
set -euo pipefail

# 1️⃣ Active le virtualenv
source /opt/venv/bin/activate

# 2️⃣ Lance le bot en production
python main.py
