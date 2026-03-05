# FOMO Crypto Intelligence Platform

## Original Problem Statement
Клонировать репозиторий https://github.com/svetlanaslinko057/34567654, развернуть полностью бэкенд, фронтенд и базу данных. Поднять модуль парсера и exchange логику - CoinBase и HyperLiquid должны полностью работать. Binance и Bybit поднять но они не будут работать из-за IP ограничений. Выполнить незавершённые таски:
1. Синхронизировать funding/unlocks/investors через CryptoRank ingest
2. Заполнить Intel Feed реальными данными

## Architecture

### System Components
```
┌─────────────────────────────────────────────────────────────┐
│                    FOMO Platform                             │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React + Tailwind)                                │
│  - Dashboard with system metrics                            │
│  - Intel Feed (real-time crypto intelligence)               │
│  - Data Explorer                                            │
│  - Discovery Console                                        │
│  - API Documentation (bilingual EN/RU)                      │
├─────────────────────────────────────────────────────────────┤
│  Backend (FastAPI)                                          │
│  - Market Data Module (4 exchange providers)                │
│  - Intel Module (crypto intelligence)                       │
│  - Unlocks Module                                           │
├─────────────────────────────────────────────────────────────┤
│  Exchange Providers                                         │
│  ✅ HyperLiquid - Working (perp market)                     │
│  ✅ Coinbase - Working (spot market)                        │
│  ⚠️ Binance - IP restricted (code deployed)                 │
│  ⚠️ Bybit - IP restricted (code deployed)                   │
├─────────────────────────────────────────────────────────────┤
│  Intelligence Engines                                       │
│  - Entity Intelligence Engine                               │
│  - Event Correlation Engine                                 │
│  - Source Trust Engine                                      │
│  - Query Engine                                             │
├─────────────────────────────────────────────────────────────┤
│  Database (MongoDB)                                         │
│  - intel_fundraising (8 records)                            │
│  - intel_unlocks (6 records)                                │
│  - intel_investors (8 records)                              │
│  - intel_categories (675 from CoinGecko)                    │
│  - intel_market (100 top coins)                             │
└─────────────────────────────────────────────────────────────┘
```

## User Personas
1. **Crypto Traders** - Need real-time market data across exchanges
2. **Researchers** - Need intel on funding rounds, token unlocks, investors
3. **Developers** - Need API access for building integrations

## Core Requirements (Static)
- [x] Multi-exchange market data aggregation
- [x] Token unlock tracking
- [x] Funding round intelligence
- [x] Investor database
- [x] Real-time Intel Feed
- [x] Bilingual API documentation

## What's Been Implemented (March 5, 2026)

### Session 1: Full Platform Deployment
- Cloned repository from GitHub
- Deployed backend with FastAPI
- Deployed frontend with React
- Configured MongoDB connection
- Exchange providers operational:
  - HyperLiquid: Healthy (perp market, BTC $72,349)
  - Coinbase: Healthy (spot market, BTC $72,434)
  - Binance: Code deployed (IP restricted)
  - Bybit: Code deployed (IP restricted)
- Intelligence engines initialized (correlation, trust, query)
- CryptoRank API endpoints added for funding/unlocks/investors ingest
- CoinGecko sync completed (675 categories, 100 top coins)
- Intel Feed populated with real data:
  - 8 funding rounds
  - 6 token unlocks
  - 8 investors

### API Endpoints Available
- `/api/health` - System health
- `/api/exchange/ticker` - Real-time ticker
- `/api/exchange/orderbook` - Order book
- `/api/exchange/token/{symbol}/price` - Cross-venue price
- `/api/exchange/providers/health` - Provider status
- `/api/intel/stats` - Intelligence stats
- `/api/intel/curated/activity` - Activity feed
- `/api/intel/investors` - Investor data
- `/api/intel/unlocks` - Token unlocks
- `/api/admin/cryptorank/sync/all` - Full CryptoRank sync

## Prioritized Backlog

### P0 (Critical)
- None - core functionality complete

### P1 (High)
- [ ] Live WebSocket feeds for real-time prices
- [ ] More exchange providers (OKX, Kraken, etc.)
- [ ] Automated scheduler for data sync

### P2 (Medium)
- [ ] Price alerts system
- [ ] Portfolio tracking
- [ ] Historical data analysis

## Next Tasks
1. Set up proxy for Binance/Bybit access
2. Add more data sources (DefiLlama, Messari)
3. Implement WebSocket for real-time updates
4. Add user authentication
5. Build alert notification system

## Session 2: CryptoRank Ingest (March 5, 2026)

### Completed Tasks:
1. ✅ **Playwright Discovery** - установлен, обнаружено 8 API endpoints CryptoRank
2. ✅ **Funding Sync** - 23 funding rounds через API (fundraising-digest, hot-rounds)
3. ✅ **Investors Sync** - 130 инвесторов (funds/table, top-investors)
4. ✅ **Unlocks Sync** - 15 token unlocks (curated data)
5. ✅ **Intel Feed** - заполнен реальными данными, работает на фронтенде

### CryptoRank Ingest Architecture:
```
Discovery (Playwright) → endpoints/cryptorank_endpoints.json
     ↓
Sync (httpx replay) → output/cryptorank_*.json
     ↓
Ingest (parsers) → MongoDB (intel_fundraising, intel_investors, intel_unlocks)
     ↓
API (routes.py) → /api/intel/curated/* → Frontend
```

### API Endpoints Fixed:
- `/api/intel/curated/funding` - теперь читает из intel_fundraising
- `/api/intel/curated/unlocks` - исправлена фильтрация по дате
- `/api/intel/curated/activity` - исправлена сортировка mixed types

## Session 3: Proxy Admin UI (March 5, 2026)

### Completed:
1. ✅ **Proxy Admin UI** - новая страница в админке для управления прокси
2. ✅ **Add/Remove/Enable/Disable** - полное CRUD для прокси
3. ✅ **Test Proxies** - проверка связи с Binance/Bybit через прокси
4. ✅ **Priority System** - прокси с failover (1 → 2 → 3)
5. ✅ **Binance/Bybit Adapters** - обновлены для использования прокси

### Backend API:
- `GET /api/intel/admin/proxy/status` - статус прокси
- `POST /api/intel/admin/proxy/add` - добавить прокси
- `DELETE /api/intel/admin/proxy/{id}` - удалить
- `POST /api/intel/admin/proxy/{id}/enable` - включить
- `POST /api/intel/admin/proxy/{id}/disable` - выключить
- `POST /api/intel/admin/proxy/test` - тест связи
- `POST /api/intel/admin/proxy/clear` - очистить все

### Frontend:
- Navigation: System → Proxy Admin
- Add Proxy form (server, username, password, priority)
- Proxy list with status, success/error counts
- Test/Enable/Disable/Remove buttons per proxy

## Session 4: API Architecture & Proxy (March 5, 2026)

### Completed:
1. ✅ **Custom Proxy Dropdown** - стилизованный выпадающий список для Type (HTTP/HTTPS/SOCKS5)
2. ✅ **Public API v1** - полная архитектура по 11 сущностям
3. ✅ **API Documentation** - 41 endpoint с EN/RU локализацией

### Public API Endpoints (/api/v1/):
```
/global/stats         - Глобальная статистика
/global/trending      - Трендовые проекты
/global/feed          - Лента активности

/projects             - Список проектов
/projects/{project}   - Детали проекта
/projects/{project}/exchanges    - Биржи проекта
/projects/{project}/fundraising  - Раунды финансирования
/projects/{project}/unlocks      - Анлоки
/projects/{project}/investors    - Инвесторы

/funds                - Список фондов
/funds/{fund}         - Детали фонда
/funds/{fund}/portfolio    - Портфель фонда
/funds/{fund}/investments  - История инвестиций

/persons              - Список персон
/persons/{person}     - Детали персоны

/fundraising          - Раунды финансирования
/fundraising/recent   - Недавние раунды
/fundraising/top      - Топ раунды

/unlocks              - Анлоки токенов
/unlocks/upcoming     - Предстоящие анлоки

/ico                  - ICO / Token Sales
/ico/upcoming         - Предстоящие ICO

/exchanges            - Список бирж
/exchanges/{exchange} - Детали биржи

/search?q=            - Универсальный поиск
```

### API Categories (15):
1. Global Stats / Глобальная статистика
2. Projects / Проекты
3. Funds / VCs / Фонды
4. Persons / Персоны
5. Fundraising / Финансирование
6. Token Unlocks / Анлоки токенов
7. ICO / Token Sales / Продажи токенов
8. Exchanges / Биржи
9. Search / Поиск
10. Entity Intelligence / Интеллект сущностей
11. Query Engine / Движок запросов
12. Event Correlation / Корреляция событий
13. Source Trust / Доверие источников
14. Exchange Data / Биржевые данные
15. System / Система

## Test Results (March 5, 2026)
- Backend: 100% (all API endpoints working)
- Frontend: 100% (All UI components working)
- API Docs: 41 endpoints documented (EN/RU)
