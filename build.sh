#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install standard Python dependencies
pip install -r requirements.txt

# 2. Install the Deno JavaScript runtime locally into a folder named '.deno'
curl -fsSL https://deno.land/install.sh | DENO_INSTALL=./.deno sh

# 3. Process Django static files and database
python manage.py collectstatic --no-input
python manage.py migrate