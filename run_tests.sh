#!/usr/bin/env bash
# Run all practice tests. Pass a folder to run just one problem, e.g.
#   ./run_tests.sh problems/p1_card_range
set -e
cd "$(dirname "$0")"
python3 -m pytest "${1:-problems}" -v
