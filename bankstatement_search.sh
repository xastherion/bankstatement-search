#!/bin/bash
# Wrapper zum Suchen in PDF-Kontoauszügen
# Verwendung: sh bankstatement_search.sh "Suchtext"

if [ $# -eq 0 ]; then
    echo "Verwendung: sh bankstatement_search.sh 'Suchtext'" >&2
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 "$SCRIPT_DIR/bankstatement_search.py" "$@"
