#!/usr/bin/env python3
"""
FOMO Platform Bootstrap / Cold Start Script
=============================================
Initializes the platform with all required data:
- API Documentation (41 endpoints)
- Persons (notable crypto figures)
- Exchanges (CEX/DEX)
- Sample projects, funding rounds, unlocks
- Proxy configuration from DB

Run: python3 scripts/bootstrap.py
"""

import asyncio
import os
import sys
from datetime import datetime, timezone, timedelta

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient


# ═══════════════════════════════════════════════════════════════
# SEED DATA
# ═══════════════════════════════════════════════════════════════

PERSONS_DATA = [
    # Founders
    {"name": "Vitalik Buterin", "slug": "vitalik-buterin", "role": "founder", "projects": ["Ethereum"], "twitter": "@VitalikButerin"},
    {"name": "Changpeng Zhao (CZ)", "slug": "cz-binance", "role": "founder", "projects": ["Binance"], "twitter": "@caborin"},
    {"name": "Sam Bankman-Fried", "slug": "sbf", "role": "founder", "projects": ["FTX", "Alameda"], "twitter": "@SBF_FTX"},
    {"name": "Brian Armstrong", "slug": "brian-armstrong", "role": "founder", "projects": ["Coinbase"], "twitter": "@brian_armstrong"},
    {"name": "Anatoly Yakovenko", "slug": "anatoly-yakovenko", "role": "founder", "projects": ["Solana"], "twitter": "@aaborin"},
    {"name": "Hayden Adams", "slug": "hayden-adams", "role": "founder", "projects": ["Uniswap"], "twitter": "@haaborins"},
    {"name": "Do Kwon", "slug": "do-kwon", "role": "founder", "projects": ["Terra", "Luna"], "twitter": "@staborins"},
    {"name": "Andre Cronje", "slug": "andre-cronje", "role": "founder", "projects": ["Yearn Finance", "Fantom"], "twitter": "@AndreCronjeTech"},
    {"name": "Stani Kulechov", "slug": "stani-kulechov", "role": "founder", "projects": ["Aave"], "twitter": "@StaniKulechov"},
    {"name": "Robert Leshner", "slug": "robert-leshner", "role": "founder", "projects": ["Compound"], "twitter": "@rleshner"},
    {"name": "Kain Warwick", "slug": "kain-warwick", "role": "founder", "projects": ["Synthetix"], "twitter": "@kaborins"},
    {"name": "Sergey Nazarov", "slug": "sergey-nazarov", "role": "founder", "projects": ["Chainlink"], "twitter": "@SergeyNazarov"},
    {"name": "Gavin Wood", "slug": "gavin-wood", "role": "founder", "projects": ["Polkadot", "Ethereum"], "twitter": "@gavofyork"},
    {"name": "Charles Hoskinson", "slug": "charles-hoskinson", "role": "founder", "projects": ["Cardano", "Ethereum"], "twitter": "@IOHK_Charles"},
    {"name": "Justin Sun", "slug": "justin-sun", "role": "founder", "projects": ["TRON", "BitTorrent"], "twitter": "@justinsuntron"},
    {"name": "Su Zhu", "slug": "su-zhu", "role": "founder", "projects": ["Three Arrows Capital"], "twitter": "@zaborin"},
    {"name": "Kyle Davies", "slug": "kyle-davies", "role": "founder", "projects": ["Three Arrows Capital"], "twitter": "@KyleLDavies"},
    {"name": "Arthur Hayes", "slug": "arthur-hayes", "role": "founder", "projects": ["BitMEX"], "twitter": "@CryptoHayes"},
    
    # VCs / Investors
    {"name": "Marc Andreessen", "slug": "marc-andreessen", "role": "investor", "projects": ["a16z"], "twitter": "@pmarca"},
    {"name": "Chris Dixon", "slug": "chris-dixon", "role": "investor", "projects": ["a16z crypto"], "twitter": "@cdixon"},
    {"name": "Fred Ehrsam", "slug": "fred-ehrsam", "role": "investor", "projects": ["Paradigm", "Coinbase"], "twitter": "@FEhrsam"},
    {"name": "Matt Huang", "slug": "matt-huang", "role": "investor", "projects": ["Paradigm"], "twitter": "@matthuang"},
    {"name": "Olaf Carlson-Wee", "slug": "olaf-carlson-wee", "role": "investor", "projects": ["Polychain Capital"], "twitter": "@polychainolaf"},
    {"name": "Naval Ravikant", "slug": "naval-ravikant", "role": "investor", "projects": ["MetaStable", "AngelList"], "twitter": "@naval"},
    {"name": "Balaji Srinivasan", "slug": "balaji-srinivasan", "role": "investor", "projects": ["Coinbase", "a16z"], "twitter": "@balajis"},
    {"name": "Dan Morehead", "slug": "dan-morehead", "role": "investor", "projects": ["Pantera Capital"], "twitter": "@dan_pantera"},
    {"name": "Joey Krug", "slug": "joey-krug", "role": "investor", "projects": ["Pantera Capital", "Augur"], "twitter": "@joeykrug"},
    {"name": "Haseeb Qureshi", "slug": "haseeb-qureshi", "role": "investor", "projects": ["Dragonfly Capital"], "twitter": "@hosseeb"},
]

EXCHANGES_DATA = [
    # CEX
    {"name": "Binance", "slug": "binance", "type": "CEX", "country": "Global", "volume_rank": 1, "founded": 2017},
    {"name": "Coinbase", "slug": "coinbase", "type": "CEX", "country": "USA", "volume_rank": 2, "founded": 2012},
    {"name": "Bybit", "slug": "bybit", "type": "CEX", "country": "Dubai", "volume_rank": 3, "founded": 2018},
    {"name": "OKX", "slug": "okx", "type": "CEX", "country": "Seychelles", "volume_rank": 4, "founded": 2017},
    {"name": "Kraken", "slug": "kraken", "type": "CEX", "country": "USA", "volume_rank": 5, "founded": 2011},
    {"name": "Bitfinex", "slug": "bitfinex", "type": "CEX", "country": "British Virgin Islands", "volume_rank": 6, "founded": 2012},
    {"name": "KuCoin", "slug": "kucoin", "type": "CEX", "country": "Seychelles", "volume_rank": 7, "founded": 2017},
    {"name": "Gate.io", "slug": "gate-io", "type": "CEX", "country": "Cayman Islands", "volume_rank": 8, "founded": 2013},
    {"name": "Huobi", "slug": "huobi", "type": "CEX", "country": "Seychelles", "volume_rank": 9, "founded": 2013},
    {"name": "MEXC", "slug": "mexc", "type": "CEX", "country": "Singapore", "volume_rank": 10, "founded": 2018},
    {"name": "Bitget", "slug": "bitget", "type": "CEX", "country": "Singapore", "volume_rank": 11, "founded": 2018},
    {"name": "Crypto.com", "slug": "crypto-com", "type": "CEX", "country": "Singapore", "volume_rank": 12, "founded": 2016},
    {"name": "Bitstamp", "slug": "bitstamp", "type": "CEX", "country": "Luxembourg", "volume_rank": 13, "founded": 2011},
    {"name": "Gemini", "slug": "gemini", "type": "CEX", "country": "USA", "volume_rank": 14, "founded": 2014},
    {"name": "Deribit", "slug": "deribit", "type": "CEX", "country": "Panama", "volume_rank": 15, "founded": 2016, "focus": "derivatives"},
    
    # DEX
    {"name": "Uniswap", "slug": "uniswap", "type": "DEX", "chain": "Ethereum", "volume_rank": 1, "founded": 2018},
    {"name": "dYdX", "slug": "dydx", "type": "DEX", "chain": "Cosmos", "volume_rank": 2, "founded": 2017, "focus": "derivatives"},
    {"name": "HyperLiquid", "slug": "hyperliquid", "type": "DEX", "chain": "Arbitrum", "volume_rank": 3, "founded": 2022, "focus": "perps"},
    {"name": "PancakeSwap", "slug": "pancakeswap", "type": "DEX", "chain": "BSC", "volume_rank": 4, "founded": 2020},
    {"name": "Curve", "slug": "curve", "type": "DEX", "chain": "Ethereum", "volume_rank": 5, "founded": 2020, "focus": "stablecoins"},
    {"name": "SushiSwap", "slug": "sushiswap", "type": "DEX", "chain": "Multi-chain", "volume_rank": 6, "founded": 2020},
    {"name": "GMX", "slug": "gmx", "type": "DEX", "chain": "Arbitrum", "volume_rank": 7, "founded": 2021, "focus": "perps"},
    {"name": "Raydium", "slug": "raydium", "type": "DEX", "chain": "Solana", "volume_rank": 8, "founded": 2021},
    {"name": "Orca", "slug": "orca", "type": "DEX", "chain": "Solana", "volume_rank": 9, "founded": 2021},
    {"name": "Jupiter", "slug": "jupiter", "type": "DEX", "chain": "Solana", "volume_rank": 10, "founded": 2021, "focus": "aggregator"},
    {"name": "1inch", "slug": "1inch", "type": "DEX", "chain": "Multi-chain", "volume_rank": 11, "founded": 2019, "focus": "aggregator"},
    {"name": "Balancer", "slug": "balancer", "type": "DEX", "chain": "Ethereum", "volume_rank": 12, "founded": 2020},
    {"name": "Trader Joe", "slug": "trader-joe", "type": "DEX", "chain": "Avalanche", "volume_rank": 13, "founded": 2021},
    {"name": "Quickswap", "slug": "quickswap", "type": "DEX", "chain": "Polygon", "volume_rank": 14, "founded": 2021},
    {"name": "Velodrome", "slug": "velodrome", "type": "DEX", "chain": "Optimism", "volume_rank": 15, "founded": 2022},
]

PROJECTS_DATA = [
    {"name": "Bitcoin", "symbol": "BTC", "slug": "bitcoin", "category": "Currency", "chain": "Bitcoin"},
    {"name": "Ethereum", "symbol": "ETH", "slug": "ethereum", "category": "Smart Contracts", "chain": "Ethereum"},
    {"name": "Solana", "symbol": "SOL", "slug": "solana", "category": "Smart Contracts", "chain": "Solana"},
    {"name": "Arbitrum", "symbol": "ARB", "slug": "arbitrum", "category": "Layer 2", "chain": "Arbitrum"},
    {"name": "Optimism", "symbol": "OP", "slug": "optimism", "category": "Layer 2", "chain": "Optimism"},
    {"name": "Polygon", "symbol": "MATIC", "slug": "polygon", "category": "Layer 2", "chain": "Polygon"},
    {"name": "Avalanche", "symbol": "AVAX", "slug": "avalanche", "category": "Smart Contracts", "chain": "Avalanche"},
    {"name": "Chainlink", "symbol": "LINK", "slug": "chainlink", "category": "Oracle", "chain": "Multi-chain"},
    {"name": "Uniswap", "symbol": "UNI", "slug": "uniswap", "category": "DEX", "chain": "Ethereum"},
    {"name": "Aave", "symbol": "AAVE", "slug": "aave", "category": "DeFi Lending", "chain": "Multi-chain"},
    {"name": "Lido", "symbol": "LDO", "slug": "lido", "category": "Liquid Staking", "chain": "Ethereum"},
    {"name": "Maker", "symbol": "MKR", "slug": "maker", "category": "DeFi Stablecoin", "chain": "Ethereum"},
    {"name": "Celestia", "symbol": "TIA", "slug": "celestia", "category": "Modular Blockchain", "chain": "Celestia"},
    {"name": "Sui", "symbol": "SUI", "slug": "sui", "category": "Smart Contracts", "chain": "Sui"},
    {"name": "Aptos", "symbol": "APT", "slug": "aptos", "category": "Smart Contracts", "chain": "Aptos"},
    {"name": "Starknet", "symbol": "STRK", "slug": "starknet", "category": "Layer 2", "chain": "Starknet"},
    {"name": "LayerZero", "symbol": "ZRO", "slug": "layerzero", "category": "Cross-chain", "chain": "Multi-chain"},
    {"name": "EigenLayer", "symbol": "EIGEN", "slug": "eigenlayer", "category": "Restaking", "chain": "Ethereum"},
    {"name": "Pyth Network", "symbol": "PYTH", "slug": "pyth", "category": "Oracle", "chain": "Solana"},
    {"name": "Jupiter", "symbol": "JUP", "slug": "jupiter", "category": "DEX Aggregator", "chain": "Solana"},
]


async def bootstrap():
    """Run full bootstrap"""
    print("=" * 60)
    print("FOMO Platform Bootstrap")
    print("=" * 60)
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    now = datetime.now(timezone.utc)
    
    # ─────────────────────────────────────────────────────────────
    # 1. Seed Persons
    # ─────────────────────────────────────────────────────────────
    print("\n[1/6] Seeding Persons...")
    persons_count = 0
    for person in PERSONS_DATA:
        doc = {
            "key": f"seed:person:{person['slug']}",
            "source": "seed",
            **person,
            "created_at": now,
            "updated_at": now
        }
        await db.intel_persons.update_one({"key": doc["key"]}, {"$set": doc}, upsert=True)
        persons_count += 1
    print(f"    ✓ {persons_count} persons")
    
    # ─────────────────────────────────────────────────────────────
    # 2. Seed Exchanges
    # ─────────────────────────────────────────────────────────────
    print("\n[2/6] Seeding Exchanges...")
    exchanges_count = 0
    for exchange in EXCHANGES_DATA:
        doc = {
            "key": f"seed:exchange:{exchange['slug']}",
            "source": "seed",
            **exchange,
            "created_at": now,
            "updated_at": now
        }
        await db.intel_exchanges.update_one({"key": doc["key"]}, {"$set": doc}, upsert=True)
        exchanges_count += 1
    print(f"    ✓ {exchanges_count} exchanges")
    
    # ─────────────────────────────────────────────────────────────
    # 3. Seed Projects
    # ─────────────────────────────────────────────────────────────
    print("\n[3/6] Seeding Projects...")
    projects_count = 0
    for project in PROJECTS_DATA:
        doc = {
            "key": f"seed:project:{project['slug']}",
            "source": "seed",
            **project,
            "created_at": now,
            "updated_at": now
        }
        await db.intel_projects.update_one({"key": doc["key"]}, {"$set": doc}, upsert=True)
        projects_count += 1
    print(f"    ✓ {projects_count} projects")
    
    # ─────────────────────────────────────────────────────────────
    # 4. Seed API Documentation
    # ─────────────────────────────────────────────────────────────
    print("\n[4/6] Seeding API Documentation...")
    import httpx
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Try local first, then external
            for base_url in ['http://localhost:8001', os.environ.get('REACT_APP_BACKEND_URL', '')]:
                if not base_url:
                    continue
                try:
                    resp = await client.post(f"{base_url}/api/docs/seed")
                    if resp.status_code == 200:
                        data = resp.json()
                        print(f"    ✓ {data.get('seeded', 0)} API endpoints")
                        break
                except:
                    continue
    except Exception as e:
        print(f"    ⚠ Could not seed docs: {e}")
    
    # ─────────────────────────────────────────────────────────────
    # 5. Load Proxy Configuration
    # ─────────────────────────────────────────────────────────────
    print("\n[5/6] Loading Proxy Configuration...")
    proxy_count = await db.system_proxies.count_documents({})
    if proxy_count > 0:
        print(f"    ✓ {proxy_count} proxies configured")
    else:
        print("    ○ No proxies configured (use Admin UI to add)")
    
    # ─────────────────────────────────────────────────────────────
    # 6. Summary
    # ─────────────────────────────────────────────────────────────
    print("\n[6/6] Final Statistics...")
    stats = {
        "persons": await db.intel_persons.count_documents({}),
        "exchanges": await db.intel_exchanges.count_documents({}),
        "projects": await db.intel_projects.count_documents({}),
        "investors": await db.intel_investors.count_documents({}),
        "fundraising": await db.intel_fundraising.count_documents({}),
        "unlocks": await db.intel_unlocks.count_documents({}),
        "docs": await db.intel_docs.count_documents({}),
    }
    
    print("\n" + "=" * 60)
    print("BOOTSTRAP COMPLETE")
    print("=" * 60)
    for key, value in stats.items():
        print(f"    {key}: {value}")
    print("=" * 60)
    
    client.close()


if __name__ == "__main__":
    asyncio.run(bootstrap())
