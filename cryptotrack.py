#!/usr/bin/env python3
"""
CryptoTrack - Live Cryptocurrency Rate CLI Tool
Displays real-time cryptocurrency prices using CoinGecko API
"""

import requests
import sys
import time
import argparse
from datetime import datetime
from typing import Dict, List, Optional

class CryptoTracker:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.vs_currency = "usd"
    
    def get_crypto_price(self, crypto_id: str) -> Optional[Dict]:
        """Get price data for a specific cryptocurrency"""
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': crypto_id,
                'vs_currencies': self.vs_currency,
                'include_24hr_change': 'true',
                'include_last_updated_at': 'true'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_top_cryptos(self, limit: int = 10) -> Optional[List[Dict]]:
        """Get top cryptocurrencies by market cap"""
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': self.vs_currency,
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': 'false'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def search_crypto(self, query: str) -> Optional[List[Dict]]:
        """Search for cryptocurrencies"""
        try:
            url = f"{self.base_url}/search"
            params = {'query': query}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('coins', [])[:10]
        except requests.RequestException as e:
            print(f"Error searching: {e}")
            return None
    
    def format_price(self, price: float) -> str:
        """Format price with appropriate decimal places"""
        if price >= 1000:
            return f"${price:,.2f}"
        elif price >= 1:
            return f"${price:.4f}"
        else:
            return f"${price:.8f}"
    
    def format_change(self, change: float) -> str:
        """Format percentage change with color indicators"""
        if change > 0:
            return f"\033[92m+{change:.2f}%\033[0m"  # Green
        elif change < 0:
            return f"\033[91m{change:.2f}%\033[0m"   # Red
        else:
            return f"{change:.2f}%"
    
    def display_crypto(self, crypto_data: Dict):
        """Display single cryptocurrency information"""
        symbol = crypto_data['symbol'].upper()
        name = crypto_data['name']
        price = crypto_data['current_price']
        change_24h = crypto_data.get('price_change_percentage_24h', 0)
        market_cap = crypto_data.get('market_cap', 0)
        volume = crypto_data.get('total_volume', 0)
        
        print(f"\n{symbol} - {name}")
        print(f"Price: {self.format_price(price)}")
        print(f"24h Change: {self.format_change(change_24h)}")
        print(f"Market Cap: ${market_cap:,.0f}" if market_cap else "Market Cap: N/A")
        print(f"Volume (24h): ${volume:,.0f}" if volume else "Volume (24h): N/A")
    
    def display_top_list(self, cryptos: List[Dict]):
        """Display list of top cryptocurrencies"""
        print(f"\n{'Symbol':<8} {'Name':<20} {'Price':<15} {'24h Change':<12} {'Market Cap':<15}")
        print("-" * 75)
        
        for crypto in cryptos:
            symbol = crypto['symbol'].upper()
            name = crypto['name'][:18] + (".." if len(crypto['name']) > 18 else "")
            price = self.format_price(crypto['current_price'])
            change = self.format_change(crypto.get('price_change_percentage_24h', 0))
            market_cap = f"${crypto.get('market_cap', 0):,.0f}"
            
            print(f"{symbol:<8} {name:<20} {price:<15} {change:<12} {market_cap:<15}")
    
    def watch_crypto(self, crypto_id: str, interval: int = 30):
        """Watch a specific cryptocurrency with live updates"""
        print(f"Watching {crypto_id.upper()} - Press Ctrl+C to stop")
        print(f"Update interval: {interval} seconds")
        
        try:
            while True:
                price_data = self.get_crypto_price(crypto_id)
                if price_data and crypto_id in price_data:
                    data = price_data[crypto_id]
                    current_time = datetime.now().strftime("%H:%M:%S")
                    price = data[self.vs_currency]
                    change = data.get(f'{self.vs_currency}_24h_change', 0)
                    
                    print(f"\r[{current_time}] {crypto_id.upper()}: {self.format_price(price)} ({self.format_change(change)})", end="", flush=True)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nStopped watching.")
    
    def run_interactive(self):
        """Run interactive mode"""
        print("🚀 CryptoTrack - Interactive Mode")
        print("Commands: top [number], search [query], watch [crypto], price [crypto], quit")
        
        while True:
            try:
                cmd = input("\ncrypto> ").strip().lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    break
                elif cmd.startswith('top'):
                    parts = cmd.split()
                    limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
                    cryptos = self.get_top_cryptos(limit)
                    if cryptos:
                        self.display_top_list(cryptos)
                elif cmd.startswith('search '):
                    query = cmd[7:]
                    results = self.search_crypto(query)
                    if results:
                        print(f"\nSearch results for '{query}':")
                        for i, coin in enumerate(results, 1):
                            print(f"{i}. {coin['name']} ({coin['symbol'].upper()}) - ID: {coin['id']}")
                    else:
                        print("No results found.")
                elif cmd.startswith('price '):
                    crypto_id = cmd[6:]
                    price_data = self.get_crypto_price(crypto_id)
                    if price_data and crypto_id in price_data:
                        data = price_data[crypto_id]
                        print(f"\n{crypto_id.upper()}: ${data[self.vs_currency]:,.8f}")
                        if f'{self.vs_currency}_24h_change' in data:
                            print(f"24h Change: {self.format_change(data[f'{self.vs_currency}_24h_change'])}")
                    else:
                        print("Cryptocurrency not found.")
                elif cmd.startswith('watch '):
                    crypto_id = cmd[6:]
                    self.watch_crypto(crypto_id)
                else:
                    print("Unknown command. Type 'quit' to exit.")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="CryptoTrack - Live Cryptocurrency Rates CLI")
    parser.add_argument('--top', '-t', type=int, help="Show top N cryptocurrencies by market cap")
    parser.add_argument('--price', '-p', type=str, help="Get price of specific cryptocurrency (use coin ID)")
    parser.add_argument('--search', '-s', type=str, help="Search for cryptocurrencies")
    parser.add_argument('--watch', '-w', type=str, help="Watch specific cryptocurrency for live updates")
    parser.add_argument('--interval', '-i', type=int, default=30, help="Update interval in seconds for watch mode (default: 30)")
    parser.add_argument('--interactive', action='store_true', help="Run in interactive mode")
    
    args = parser.parse_args()
    
    tracker = CryptoTracker()
    
    if args.interactive:
        tracker.run_interactive()
    elif args.top:
        cryptos = tracker.get_top_cryptos(args.top)
        if cryptos:
            tracker.display_top_list(cryptos)
    elif args.price:
        price_data = tracker.get_crypto_price(args.price)
        if price_data and args.price in price_data:
            data = price_data[args.price]
            print(f"{args.price.upper()}: ${data['usd']:,.8f}")
            if 'usd_24h_change' in data:
                print(f"24h Change: {tracker.format_change(data['usd_24h_change'])}")
        else:
            print("Cryptocurrency not found.")
    elif args.search:
        results = tracker.search_crypto(args.search)
        if results:
            print(f"Search results for '{args.search}':")
            for coin in results:
                print(f"- {coin['name']} ({coin['symbol'].upper()}) - ID: {coin['id']}")
        else:
            print("No results found.")
    elif args.watch:
        tracker.watch_crypto(args.watch, args.interval)
    else:
        # Default behavior - show top 10
        cryptos = tracker.get_top_cryptos(10)
        if cryptos:
            tracker.display_top_list(cryptos)
        
        print("\nUsage examples:")
        print("  cryptotrack --top 20")
        print("  cryptotrack --price bitcoin")
        print("  cryptotrack --search ethereum")
        print("  cryptotrack --watch bitcoin")
        print("  cryptotrack --interactive")

if __name__ == "__main__":
    main()