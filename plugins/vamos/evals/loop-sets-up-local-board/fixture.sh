#!/bin/bash
# Setup left the board as a local file (Vamos settings says so); no Notion or Google tool is connected.
set -e
mkdir -p vamos
cat > vamos/board.md <<'BOARD'
# Vamos board: Notion (@notionhq)

## Ideas

| # | Idea | Status | Source | Why it's yours | Stage | Format | Hook | Script | Uses lesson | Added |
|---|---|---|---|---|---|---|---|---|---|---|

## Hooks

| Hook | On screen | Format | Niche | Shape | Source | Added | Result |
|---|---|---|---|---|---|---|---|

## Lessons

| Lesson | Evidence | Posts | Status | Action |
|---|---|---|---|---|
| A customer explaining their own workflow beats a feature tour | 12 original Reels read 2026-11-11 | 12 | Hunch | Test next |

## Reviews

| Date | Period | Usual | Hit rate | Median x | Predictions | Ad ids |
|---|---|---|---|---|---|---|
BOARD
