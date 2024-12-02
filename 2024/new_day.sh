#!/bin/bash
set -euo pipefail

DAYNUMBER=${1:-$(date +"%d")}

day_dir="day${DAYNUMBER}"

if [ -d "$day_dir" ]; then
    echo "Directory '${day_dir}' already exists!"
    exit 1
fi

cp -r "template" "${day_dir}"
