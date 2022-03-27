#!/bin/bash
cd "$(dirname "$0")"

# Activate virtual environment
source env/bin/activate

# Run package
python3 -m personal_economy
