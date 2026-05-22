#!/bin/bash

# Check if a word is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <word>"
    exit 1
fi

WORD="$1"
API_URL="https://api.dictionaryapi.dev/api/v2/entries/en/$WORD"

# Fetch the JSON from the API
RESPONSE=$(curl -s "$API_URL")

# If the API returned an error
if echo "$RESPONSE" | jq -e '.title? | contains("No Definitions Found")' >/dev/null; then
    echo "No definitions found for '$WORD'."
    exit 1
fi

# Print top 3 definitions from the first part of speech
echo "Top 3 definitions for \"$WORD\":"
echo "$RESPONSE" | jq -r '
  .[0].meanings[0].definitions[:3][] |
  "- " + .definition
'

echo
# Print top 2 definitions where partOfSpeech is verb
echo "Top 2 verb definitions:"
echo "$RESPONSE" | jq -r '
  .[0].meanings[] 
  | select(.partOfSpeech == "verb") 
  | .definitions[:2][] 
  | "- " + .definition
'
