#!/bin/bash
cd "$(dirname "$0")"
pwd

# Activate virtual environment
source env/bin/activate

# Run package
python3 personal_economy/ 
