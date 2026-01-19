# CryptoTrack - Live Cryptocurrency Rates CLI Tool

A Python CLI tool that displays live cryptocurrency rates using the CoinGecko public API (no API key required).

## Setup

1. Activate the virtual environment:
   ```bash
   source crypto_env/bin/activate
   ```

2. The tool is ready to use! All dependencies are installed.

## Usage

### Basic Commands

- **Show top cryptocurrencies** (default shows 10):
  ```bash
  python cryptotrack.py --top 20
  ```

- **Get specific crypto price**:
  ```bash
  python cryptotrack.py --price bitcoin
  python cryptotrack.py --price ethereum
  ```

- **Search for cryptocurrencies**:
  ```bash
  python cryptotrack.py --search cardano
  ```

- **Watch live updates** (updates every 30 seconds by default):
  ```bash
  python cryptotrack.py --watch bitcoin
  python cryptotrack.py --watch bitcoin --interval 10
  ```

- **Interactive mode**:
  ```bash
  python cryptotrack.py --interactive
  ```

### Interactive Mode Commands

When in interactive mode, you can use:
- `top [number]` - Show top N cryptocurrencies
- `search [query]` - Search for cryptocurrencies
- `price [crypto]` - Get price of specific crypto
- `watch [crypto]` - Watch live updates
- `quit` - Exit interactive mode

### Examples

```bash
# Show top 15 cryptocurrencies
python cryptotrack.py -t 15

# Get Bitcoin price
python cryptotrack.py -p bitcoin

# Search for "sol"
python cryptotrack.py -s sol

# Watch Ethereum with 10-second updates
python cryptotrack.py -w ethereum -i 10

# Run in interactive mode
python cryptotrack.py --interactive
```

## Features

- Real-time cryptocurrency prices from CoinGecko
- No API key required
- Price change indicators (green/red)
- Market cap and volume data
- Search functionality
- Live watching mode
- Interactive command-line interface
- Supports common crypto IDs (bitcoin, ethereum, etc.)

## Common Crypto IDs

- bitcoin, btc
- ethereum, eth
- cardano, ada
- solana, sol
- polkadot, dot
- dogecoin, doge
- litecoin, ltc
- avalanche, avax
- chainlink, link
- polygon, matic