# Support/Resistance Breakout Discord Bot

A Discord bot that monitors configured tickers, detects support/resistance breakouts, and posts alerts with helpful context.

## Features
- Config-driven setup using environment variables (`.env` supported)
- Structured logging
- Pluggable market data provider interface with an example CoinGecko implementation
- Support/resistance breakout detection with basic volume and threshold filters
- Discord commands for runtime configuration and status
- Optional state persistence for tracked tickers
- Configurable signal polling cadence

## Quick start
1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. In the Discord Developer Portal, enable the **Message Content Intent** for your bot so it can respond to text commands.
3. Copy `.env.example` to `.env` and fill in your Discord bot token and channel IDs.
4. Run the bot:
   ```bash
   python -m src.main
   ```

## Deploying to Railway
Railway can build and run the bot using the included `Procfile` and `runtime.txt`:

1. Create a new Railway project and link this repository.
2. Set required environment variables (`DISCORD_TOKEN`, `DISCORD_CHANNEL_ID`, etc.).
3. Railway will install dependencies from `requirements.txt`, use the Python version declared in `runtime.txt`, and start the worker process defined in `Procfile`:
   ```
   worker: python -m src.main
   ```
4. Ensure the Discord bot token has the **Message Content Intent** enabled in the Developer Portal.

## Environment variables
See `.env.example` for all supported variables. Key settings include:
- `DISCORD_TOKEN` — Discord bot token
- `DISCORD_CHANNEL_ID` — default channel for alerts
- `TICKERS` — comma-separated tickers/symbols to monitor
- `POLL_INTERVAL` — seconds between market checks
- `MARKET_DATA_PROVIDER` — provider identifier (currently `coingecko`)

Set `ENV_FILE` if you want the app to load a specific dotenv file path (the value is passed directly to `python-dotenv` when installed). If `python-dotenv` is missing, the loader is a no-op so the bot can still run purely from environment variables.

## Project structure
- `src/config.py` — configuration loading and validation
- `src/logging_config.py` — logger setup
- `src/data/` — HTTP client, provider interfaces, caching
- `src/signals/` — data models and support/resistance detection logic
- `src/bot/` — Discord client, commands, and message formatting
- `src/storage/` — basic persistence utilities
- `src/main.py` — application entry point

## Testing
Install dev dependencies and run pytest:
```bash
pip install -e .[dev]
python -m pytest
```
