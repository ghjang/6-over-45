# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Korean lottery (Lotto 6/45) analysis web application that:
- Fetches latest lottery results from donghang lottery (https://dhlottery.co.kr)
- Tracks number frequency statistics
- Generates next draw predictions using various algorithms
- Visualizes data via D3.js charts in a SvelteKit web app

## Data Flow

1. **fetch_latest.py** scrapes the latest lottery draw results from the official Korean lottery website
2. **update_frequency.py** merges latest results into frequency.json
3. **update_guesses.py** generates 5 prediction combinations using different strategies:
   - Cumulative frequency (with/without bonus)
   - Recent 12-week hot trend
   - Cold numbers (inverse frequency weighting)
   - Pure random

The generated JSON files in `data/` are consumed by the SvelteKit web app.

## Web App Structure

Located in `web/` directory - a SvelteKit application using:
- **s-comp-core**: UI component library (Tab, ToggleGroup, RadioButton)
- **D3.js**: For BarChart and LineChart visualizations
- **Adapter Static**: Builds to static site for GitHub Pages deployment

Key routes/components:
- `+page.svelte`: Main tab container (LottoFrequency, PreviousDrawResult, NextGuess)
- `LottoFrequency.svelte`: Frequency visualization with bar/line chart toggle
- `LottoBall.svelte`: Displays lottery numbers with official color coding (Yellow/Blue/Red/Gray/Green based on number range)

## Development Commands

```bash
# Web app (in web/ directory)
npm run dev          # Start dev server
npm run build        # Production build to web/build/
npm run preview      # Preview production build
npm run check        # Type checking with svelte-check
npm run lint         # Prettier + ESLint check
npm run format       # Format with Prettier
npm run test         # Run all tests (integration + unit)
npm run test:integration  # Playwright tests
npm run test:unit         # Vitest tests

# Python scripts
python scripts/fetch_latest.py     # Fetch latest lottery results
python scripts/update_frequency.py # Update frequency.json with latest results
python scripts/update_guesses.py   # Generate predictions and update guesses
```

## CI/CD

- **update_guesses.yml**: Runs weekly (Mondays 01:00 UTC) or on frequency.json push. Executes the 3 Python scripts in sequence and commits results.
- **6-over-45-github-pages.yml**: Triggered after update_guesses succeeds. Builds the SvelteKit app, copies JSON data to build/, deploys to GitHub Pages, and creates a release tagged `release-{draw_number}`.

## Important Notes

- The app uses `/6-over-45` as base path in production (configured in svelte.config.js)
- JSON data files are copied to `web/build/data/` during deployment
- LottoBall color coding follows official Korean lottery standards: 1-10 (Yellow), 11-20 (Blue), 21-30 (Red), 31-40 (Gray), 41-45 (Green)
- Korean language is used throughout the UI and comments
