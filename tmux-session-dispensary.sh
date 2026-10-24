#!/usr/bin/env bash

set -euo pipefail

SEARCH_DIRS=(
    "$HOME/Developer"
    "$HOME/Developer/github.com/"
)

selected=$(
    fd --type d --max-depth 1 --hidden \
        --exclude .git \
        . "${SEARCH_DIRS[@]}" |
        awk -v home="$HOME/" '
            {
                path = $0
                sub("^" home, "", path)

                n = split(path, parts, "/")
                if (n >= 2)
                    print parts[n-1] "/" parts[n] "\t" $0
                else
                    print parts[n] "\t" $0
            }
        ' |
        sk --delimiter="$(printf '\t')" --with-nth=1 \
            --prompt="tmux > " |
        cut -f2-
) || exit 0

[[ -n "$selected" ]] || exit 0

slug=$(
    basename "$selected" |
        tr '[:upper:]' '[:lower:]' |
        sed -E 's/[[:space:]]+/-/g; s/[^a-z0-9-]//g; s/-+/-/g; s/^-|-$//g'
)

[[ -n "$slug" ]] || slug="project"

path_hash=$(printf '%s' "$selected" | sha256sum | cut -c1-8)
session_name="${slug}-${path_hash}"

LOG="${XDG_STATE_HOME:-$HOME/.local/state}/tmux-launcher.log"
mkdir -p "$(dirname "$LOG")"

setsid -f kitty --directory "$selected" \
    tmux new-session -A -s "$session_name" -c "$selected" \
    >>"$LOG" 2>&1 </dev/null

exit 0
