"""
API Documentation Registry

Stores structured API documentation in MongoDB with bilingual support (EN/RU).
Provides complete endpoint descriptions, parameters, examples.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class ApiParameter:
    """API Parameter definition"""
    name: str
    type: str  # string, integer, number, boolean, array, object
    required: bool = False
    location: str = "query"  # query, path, body, header
    description_en: str = ""
    description_ru: str = ""
    default: Any = None
    example: Any = None
    enum: List[str] = None


@dataclass
class ApiResponse:
    """API Response definition"""
    status_code: int
    description_en: str
    description_ru: str
    example: Dict[str, Any] = None
    schema: Dict[str, Any] = None


@dataclass
class ApiEndpoint:
    """Complete API Endpoint documentation"""
    endpoint_id: str
    path: str
    method: HttpMethod
    
    # Bilingual descriptions
    title_en: str
    title_ru: str
    description_en: str
    description_ru: str
    
    # Category/tags
    category: str
    tags: List[str] = field(default_factory=list)
    
    # Parameters
    parameters: List[ApiParameter] = field(default_factory=list)
    
    # Request body (for POST/PUT)
    request_body: Dict[str, Any] = None
    request_example: Dict[str, Any] = None
    
    # Responses
    responses: List[ApiResponse] = field(default_factory=list)
    
    # Metadata
    version: str = "2.0.0"
    deprecated: bool = False
    auth_required: bool = False
    rate_limit: str = None
    
    created_at: str = None
    updated_at: str = None


# ═══════════════════════════════════════════════════════════════
# API DOCUMENTATION REGISTRY
# ═══════════════════════════════════════════════════════════════

API_DOCUMENTATION: List[ApiEndpoint] = [
    
    # ───────────────────────────────────────────────────────────
    # ENTITY INTELLIGENCE API
    # ───────────────────────────────────────────────────────────
    
    ApiEndpoint(
        endpoint_id="entity_get",
        path="/api/intel/entity/{query}",
        method=HttpMethod.GET,
        title_en="Get Entity by Identifier",
        title_ru="Получить сущность по идентификатору",
        description_en="Resolve any identifier (symbol, name, address, slug, external key) to entity profile. Returns full entity data with event counts. This is the main endpoint for entity lookup.",
        description_ru="Разрешает любой идентификатор (символ, название, адрес, slug, внешний ключ) в профиль сущности. Возвращает полные данные сущности с количеством событий. Это основной endpoint для поиска сущностей.",
        category="entity",
        tags=["entity", "resolution", "profile"],
        parameters=[
            ApiParameter(
                name="query",
                type="string",
                required=True,
                location="path",
                description_en="Entity identifier: symbol (BTC), name (Bitcoin), address (0x...), slug (bitcoin), or external key (coingecko:bitcoin)",
                description_ru="Идентификатор сущности: символ (BTC), название (Bitcoin), адрес (0x...), slug (bitcoin) или внешний ключ (coingecko:bitcoin)",
                example="arbitrum"
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Entity profile with event counts",
                description_ru="Профиль сущности с количеством событий",
                example={
                    "ts": 1772717367700,
                    "entity": {
                        "entity_id": "ent_arbitrum_abc123",
                        "type": "token",
                        "canonical": {"name": "Arbitrum", "symbol": "ARB"},
                        "keys": {"coingecko": "arbitrum", "cryptorank": "arb"},
                        "confidence": 0.92
                    },
                    "event_counts": {"funding_round": 3, "unlock_event": 12},
                    "total_events": 15
                }
            ),
            ApiResponse(
                status_code=404,
                description_en="Entity not found",
                description_ru="Сущность не найдена"
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="entity_timeline",
        path="/api/intel/entity/{query}/timeline",
        method=HttpMethod.GET,
        title_en="Get Entity Timeline",
        title_ru="Получить хронологию событий сущности",
        description_en="Get chronological event timeline for entity. Shows all events in order: funding rounds, unlocks, listings, sales. Essential for understanding project lifecycle.",
        description_ru="Получить хронологическую ленту событий для сущности. Показывает все события по порядку: раунды финансирования, анлоки, листинги, продажи. Важно для понимания жизненного цикла проекта.",
        category="entity",
        tags=["entity", "timeline", "events", "lifecycle"],
        parameters=[
            ApiParameter(
                name="query",
                type="string",
                required=True,
                location="path",
                description_en="Entity identifier",
                description_ru="Идентификатор сущности",
                example="eigenlayer"
            ),
            ApiParameter(
                name="types",
                type="string",
                required=False,
                location="query",
                description_en="Comma-separated event types filter",
                description_ru="Фильтр типов событий через запятую",
                example="funding_round,unlock_event"
            ),
            ApiParameter(
                name="limit",
                type="integer",
                required=False,
                location="query",
                description_en="Maximum number of events",
                description_ru="Максимальное количество событий",
                default=100,
                example=50
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Entity timeline with events",
                description_ru="Хронология сущности с событиями",
                example={
                    "entity": {"entity_id": "ent_eigen_123", "canonical": {"name": "EigenLayer"}},
                    "timeline": [
                        {"type": "funding_round", "ts": "2024-03-01", "data": {"raised_usd": 50000000}},
                        {"type": "unlock_event", "ts": "2024-06-01", "data": {"amount_usd": 120000000}}
                    ],
                    "count": 2
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="entity_stats",
        path="/api/intel/entity/stats",
        method=HttpMethod.GET,
        title_en="Get Entity Intelligence Statistics",
        title_ru="Получить статистику Entity Intelligence",
        description_en="Get statistics about the Entity Intelligence Engine: total entities, index entries, events count, resolver cache size.",
        description_ru="Получить статистику движка Entity Intelligence: всего сущностей, записей в индексе, количество событий, размер кэша резолвера.",
        category="entity",
        tags=["entity", "stats", "monitoring"],
        parameters=[],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Entity intelligence statistics",
                description_ru="Статистика Entity Intelligence",
                example={
                    "ts": 1772717367700,
                    "entities": 7362,
                    "index_entries": 24890,
                    "events": 10210,
                    "resolver_cache_size": 156
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="entity_resolve",
        path="/api/intel/entity/resolve",
        method=HttpMethod.POST,
        title_en="Resolve Identifier to Entity ID",
        title_ru="Разрешить идентификатор в Entity ID",
        description_en="Resolve any identifier to canonical entity_id. Returns whether the identifier was successfully resolved.",
        description_ru="Разрешить любой идентификатор в канонический entity_id. Возвращает успешность разрешения идентификатора.",
        category="entity",
        tags=["entity", "resolution"],
        parameters=[
            ApiParameter(
                name="query",
                type="string",
                required=True,
                location="query",
                description_en="Identifier to resolve",
                description_ru="Идентификатор для разрешения",
                example="bitcoin"
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Resolution result",
                description_ru="Результат разрешения",
                example={
                    "ts": 1772717367700,
                    "query": "bitcoin",
                    "entity_id": "ent_bitcoin_abc123",
                    "resolved": True
                }
            )
        ]
    ),
    
    # ───────────────────────────────────────────────────────────
    # QUERY ENGINE API
    # ───────────────────────────────────────────────────────────
    
    ApiEndpoint(
        endpoint_id="query_events",
        path="/api/intel/engine/query/events",
        method=HttpMethod.POST,
        title_en="Query Events with Filters",
        title_ru="Запрос событий с фильтрами",
        description_en="Query events with flexible filters: entity, event_type, investor, amount range, date range, source, confidence. Supports pagination and sorting.",
        description_ru="Запрос событий с гибкими фильтрами: сущность, тип события, инвестор, диапазон сумм, диапазон дат, источник, уверенность. Поддерживает пагинацию и сортировку.",
        category="query",
        tags=["query", "events", "filters", "search"],
        parameters=[
            ApiParameter(
                name="entity",
                type="string",
                required=False,
                location="query",
                description_en="Filter by entity ID",
                description_ru="Фильтр по ID сущности"
            ),
            ApiParameter(
                name="event_type",
                type="string",
                required=False,
                location="query",
                description_en="Filter by event type: funding_round, unlock_event, token_sale, listing",
                description_ru="Фильтр по типу события: funding_round, unlock_event, token_sale, listing",
                enum=["funding_round", "unlock_event", "token_sale", "listing", "investor_activity"]
            ),
            ApiParameter(
                name="investor",
                type="string",
                required=False,
                location="query",
                description_en="Filter by investor name",
                description_ru="Фильтр по имени инвестора",
                example="a16z"
            ),
            ApiParameter(
                name="min_amount",
                type="number",
                required=False,
                location="query",
                description_en="Minimum amount in USD",
                description_ru="Минимальная сумма в USD",
                example=50000000
            ),
            ApiParameter(
                name="days_back",
                type="integer",
                required=False,
                location="query",
                description_en="Filter events from last N days",
                description_ru="Фильтр событий за последние N дней",
                example=30
            ),
            ApiParameter(
                name="limit",
                type="integer",
                required=False,
                location="query",
                description_en="Maximum results",
                description_ru="Максимум результатов",
                default=50
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Query results with events",
                description_ru="Результаты запроса с событиями",
                example={
                    "ts": 1772717367700,
                    "query": {"event_type": "funding_round", "investor": "a16z"},
                    "total": 156,
                    "count": 50,
                    "results": [{"entity_id": "ent_123", "type": "funding_round", "data": {}}]
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="query_investor_portfolio",
        path="/api/intel/engine/query/investor/{investor}/portfolio",
        method=HttpMethod.GET,
        title_en="Get Investor Portfolio",
        title_ru="Получить портфель инвестора",
        description_en="Get all projects an investor has funded. Shows total invested amount, number of rounds, and detailed investment history.",
        description_ru="Получить все проекты, которые финансировал инвестор. Показывает общую сумму инвестиций, количество раундов и детальную историю инвестиций.",
        category="query",
        tags=["query", "investor", "portfolio", "analysis"],
        parameters=[
            ApiParameter(
                name="investor",
                type="string",
                required=True,
                location="path",
                description_en="Investor name",
                description_ru="Имя инвестора",
                example="a16z"
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Investor portfolio",
                description_ru="Портфель инвестора",
                example={
                    "ts": 1772717367700,
                    "investor": "a16z",
                    "portfolio_size": 45,
                    "total_invested": 2500000000,
                    "portfolio": [
                        {"entity_id": "ent_uniswap", "total_invested": 150000000, "round_count": 2}
                    ]
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="query_unlocks_upcoming",
        path="/api/intel/engine/query/unlocks/upcoming",
        method=HttpMethod.GET,
        title_en="Get Upcoming Token Unlocks",
        title_ru="Получить предстоящие разблокировки токенов",
        description_en="Get upcoming token unlocks within specified time window. Shows unlock count and total USD exposure.",
        description_ru="Получить предстоящие разблокировки токенов в указанном временном окне. Показывает количество анлоков и общую экспозицию в USD.",
        category="query",
        tags=["query", "unlocks", "upcoming", "risk"],
        parameters=[
            ApiParameter(
                name="days",
                type="integer",
                required=False,
                location="query",
                description_en="Days ahead to look",
                description_ru="Дней вперёд для просмотра",
                default=30,
                example=7
            ),
            ApiParameter(
                name="min_usd",
                type="number",
                required=False,
                location="query",
                description_en="Minimum unlock value in USD",
                description_ru="Минимальная стоимость анлока в USD",
                default=0,
                example=10000000
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Upcoming unlocks",
                description_ru="Предстоящие разблокировки",
                example={
                    "ts": 1772717367700,
                    "days_ahead": 30,
                    "unlock_count": 45,
                    "total_usd_exposure": 890000000,
                    "unlocks": []
                }
            )
        ]
    ),
    
    # ───────────────────────────────────────────────────────────
    # CORRELATION ENGINE API
    # ───────────────────────────────────────────────────────────
    
    ApiEndpoint(
        endpoint_id="correlation_run",
        path="/api/intel/engine/correlation/run",
        method=HttpMethod.POST,
        title_en="Run Event Correlation",
        title_ru="Запустить корреляцию событий",
        description_en="Run correlation engine to build relationships between events. Discovers chains: Funding → Token Sale → Listing → Unlock.",
        description_ru="Запустить движок корреляции для построения связей между событиями. Обнаруживает цепочки: Funding → Token Sale → Listing → Unlock.",
        category="correlation",
        tags=["correlation", "relations", "pipeline", "analysis"],
        parameters=[
            ApiParameter(
                name="limit",
                type="integer",
                required=False,
                location="query",
                description_en="Maximum entities to process",
                description_ru="Максимум сущностей для обработки",
                default=500
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Correlation results",
                description_ru="Результаты корреляции",
                example={
                    "ts": 1772717367700,
                    "ok": True,
                    "entities_processed": 500,
                    "relations_created": 1250,
                    "elapsed_sec": 12.5
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="correlation_timeline",
        path="/api/intel/engine/correlation/entity/{entity_id}/timeline",
        method=HttpMethod.GET,
        title_en="Get Entity Correlation Timeline",
        title_ru="Получить таймлайн корреляций сущности",
        description_en="Get full event timeline with correlations for entity. Shows lifecycle: Funding → Sale → Listing → Unlock with relation types.",
        description_ru="Получить полную хронологию событий с корреляциями для сущности. Показывает жизненный цикл: Funding → Sale → Listing → Unlock с типами связей.",
        category="correlation",
        tags=["correlation", "timeline", "lifecycle"],
        parameters=[
            ApiParameter(
                name="entity_id",
                type="string",
                required=True,
                location="path",
                description_en="Entity ID",
                description_ru="ID сущности"
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Timeline with correlations",
                description_ru="Хронология с корреляциями",
                example={
                    "entity_id": "ent_layerzero",
                    "event_count": 5,
                    "relation_count": 4,
                    "lifecycle": [
                        {"stage": "funding", "date": "2024-01-15"},
                        {"stage": "token_sale", "date": "2024-06-01"},
                        {"stage": "listing", "date": "2024-06-15"}
                    ]
                }
            )
        ]
    ),
    
    # ───────────────────────────────────────────────────────────
    # SOURCE TRUST ENGINE API
    # ───────────────────────────────────────────────────────────
    
    ApiEndpoint(
        endpoint_id="trust_scores",
        path="/api/intel/engine/trust/scores",
        method=HttpMethod.GET,
        title_en="Get Source Trust Scores",
        title_ru="Получить рейтинги доверия источников",
        description_en="Get trust scores for all data sources. Higher score = more reliable source. Affects event confidence and dedup decisions.",
        description_ru="Получить рейтинги доверия для всех источников данных. Высокий рейтинг = более надёжный источник. Влияет на уверенность событий и решения по дедупликации.",
        category="trust",
        tags=["trust", "sources", "quality"],
        parameters=[],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Trust scores for all sources",
                description_ru="Рейтинги доверия для всех источников",
                example={
                    "ts": 1772717367700,
                    "count": 8,
                    "sources": [
                        {"source_id": "cryptorank", "trust_score": 0.93},
                        {"source_id": "coingecko", "trust_score": 0.91},
                        {"source_id": "dropstab", "trust_score": 0.89}
                    ]
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="trust_source_detail",
        path="/api/intel/engine/trust/source/{source_id}",
        method=HttpMethod.GET,
        title_en="Get Source Trust Details",
        title_ru="Получить детали доверия источника",
        description_en="Get detailed trust information for specific source including metrics: success_rate, schema_stability, freshness, cross_source_agreement.",
        description_ru="Получить детальную информацию о доверии для конкретного источника включая метрики: success_rate, schema_stability, freshness, cross_source_agreement.",
        category="trust",
        tags=["trust", "source", "metrics"],
        parameters=[
            ApiParameter(
                name="source_id",
                type="string",
                required=True,
                location="path",
                description_en="Source identifier",
                description_ru="Идентификатор источника",
                example="cryptorank"
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Source trust details",
                description_ru="Детали доверия источника",
                example={
                    "source_id": "cryptorank",
                    "trust_score": 0.93,
                    "default_trust": 0.93,
                    "metrics": {
                        "success_rate": 0.97,
                        "schema_stability": 0.95,
                        "freshness": 0.91,
                        "cross_source_agreement": 0.89
                    }
                }
            )
        ]
    ),
    
    # ───────────────────────────────────────────────────────────
    # EXCHANGE API
    # ───────────────────────────────────────────────────────────
    
    ApiEndpoint(
        endpoint_id="exchange_providers",
        path="/api/exchange/providers",
        method=HttpMethod.GET,
        title_en="List Exchange Providers",
        title_ru="Список биржевых провайдеров",
        description_en="Get list of all configured exchange providers with their capabilities (spot, futures, margin, options, websocket).",
        description_ru="Получить список всех настроенных биржевых провайдеров с их возможностями (spot, futures, margin, options, websocket).",
        category="exchange",
        tags=["exchange", "providers", "market_data"],
        parameters=[],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="List of providers",
                description_ru="Список провайдеров",
                example={
                    "ts": 1772717367700,
                    "providers": [
                        {
                            "venue": "hyperliquid",
                            "display_name": "Hyperliquid",
                            "capabilities": {"has_spot": False, "has_futures": True}
                        }
                    ]
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="exchange_ticker",
        path="/api/exchange/ticker",
        method=HttpMethod.GET,
        title_en="Get Exchange Ticker",
        title_ru="Получить тикер биржи",
        description_en="Get real-time ticker data from exchange. Returns last price, 24h change, volume.",
        description_ru="Получить данные тикера в реальном времени с биржи. Возвращает последнюю цену, изменение за 24ч, объём.",
        category="exchange",
        tags=["exchange", "ticker", "price", "realtime"],
        parameters=[
            ApiParameter(
                name="venue",
                type="string",
                required=True,
                location="query",
                description_en="Exchange venue: hyperliquid, coinbase, binance, bybit",
                description_ru="Биржа: hyperliquid, coinbase, binance, bybit",
                example="hyperliquid"
            ),
            ApiParameter(
                name="symbol",
                type="string",
                required=True,
                location="query",
                description_en="Trading symbol",
                description_ru="Торговый символ",
                example="BTC"
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Ticker data",
                description_ru="Данные тикера",
                example={
                    "ts": 1772717367700,
                    "instrument_id": "hyperliquid:perp:BTC-PERP",
                    "last": 96500.5,
                    "change_24h": 2.35,
                    "volume_24h": 4057639146.47
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="exchange_funding",
        path="/api/exchange/funding",
        method=HttpMethod.GET,
        title_en="Get Funding Rate",
        title_ru="Получить ставку финансирования",
        description_en="Get current funding rate for perpetual futures. Important for derivatives trading strategy.",
        description_ru="Получить текущую ставку финансирования для бессрочных фьючерсов. Важно для стратегии торговли деривативами.",
        category="exchange",
        tags=["exchange", "funding", "derivatives", "perp"],
        parameters=[
            ApiParameter(
                name="venue",
                type="string",
                required=True,
                location="query",
                description_en="Exchange venue",
                description_ru="Биржа",
                example="hyperliquid"
            ),
            ApiParameter(
                name="symbol",
                type="string",
                required=True,
                location="query",
                description_en="Symbol",
                description_ru="Символ",
                example="BTC"
            )
        ],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Funding rate data",
                description_ru="Данные ставки финансирования",
                example={
                    "ts": 1772717367700,
                    "instrument_id": "hyperliquid:perp:BTC-PERP",
                    "funding_rate": 0.0000125,
                    "funding_time": 1772720000000
                }
            )
        ]
    ),
    
    # ───────────────────────────────────────────────────────────
    # SYSTEM API
    # ───────────────────────────────────────────────────────────
    
    ApiEndpoint(
        endpoint_id="health",
        path="/api/health",
        method=HttpMethod.GET,
        title_en="Health Check",
        title_ru="Проверка работоспособности",
        description_en="Check API health status. Returns service status and available features.",
        description_ru="Проверить состояние API. Возвращает статус сервиса и доступные функции.",
        category="system",
        tags=["system", "health", "monitoring"],
        parameters=[],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Health status",
                description_ru="Статус работоспособности",
                example={
                    "ok": True,
                    "service": "FOMO Intel API",
                    "features": {
                        "market_data": ["hyperliquid", "coinbase", "binance", "bybit"],
                        "asset_intel": "available"
                    }
                }
            )
        ]
    ),
    
    ApiEndpoint(
        endpoint_id="engine_status",
        path="/api/intel/engine/status",
        method=HttpMethod.GET,
        title_en="Get All Engines Status",
        title_ru="Получить статус всех движков",
        description_en="Get status of all intelligence engines: Correlation, Trust, Query. Shows initialization state and session stats.",
        description_ru="Получить статус всех движков интеллекта: Correlation, Trust, Query. Показывает состояние инициализации и статистику сессии.",
        category="system",
        tags=["system", "engines", "status"],
        parameters=[],
        responses=[
            ApiResponse(
                status_code=200,
                description_en="Engines status",
                description_ru="Статус движков",
                example={
                    "ts": 1772717367700,
                    "engines": {
                        "correlation": {"initialized": True, "entities_processed": 500},
                        "trust": {"initialized": True, "cached_scores": 8},
                        "query": {"initialized": True}
                    }
                }
            )
        ]
    ),
]


class ApiDocumentationRegistry:
    """
    Manages API documentation in MongoDB.
    
    Provides:
    - Store/retrieve structured documentation
    - Bilingual support (EN/RU)
    - Search by category/tag
    """
    
    def __init__(self, db=None):
        self.db = db
        self.collection_name = "api_documentation"
    
    async def seed_documentation(self) -> Dict[str, Any]:
        """
        Seed database with API documentation.
        """
        if self.db is None:
            return {"error": "No database connection"}
        
        collection = self.db[self.collection_name]
        
        # Clear existing
        await collection.delete_many({})
        
        # Insert all documentation
        docs = []
        now = datetime.now(timezone.utc).isoformat()
        
        for endpoint in API_DOCUMENTATION:
            doc = {
                "endpoint_id": endpoint.endpoint_id,
                "path": endpoint.path,
                "method": endpoint.method.value,
                "title_en": endpoint.title_en,
                "title_ru": endpoint.title_ru,
                "description_en": endpoint.description_en,
                "description_ru": endpoint.description_ru,
                "category": endpoint.category,
                "tags": endpoint.tags,
                "parameters": [
                    {
                        "name": p.name,
                        "type": p.type,
                        "required": p.required,
                        "location": p.location,
                        "description_en": p.description_en,
                        "description_ru": p.description_ru,
                        "default": p.default,
                        "example": p.example,
                        "enum": p.enum
                    }
                    for p in endpoint.parameters
                ],
                "request_body": endpoint.request_body,
                "request_example": endpoint.request_example,
                "responses": [
                    {
                        "status_code": r.status_code,
                        "description_en": r.description_en,
                        "description_ru": r.description_ru,
                        "example": r.example
                    }
                    for r in endpoint.responses
                ],
                "version": endpoint.version,
                "deprecated": endpoint.deprecated,
                "auth_required": endpoint.auth_required,
                "rate_limit": endpoint.rate_limit,
                "created_at": now,
                "updated_at": now
            }
            docs.append(doc)
        
        if docs:
            await collection.insert_many(docs)
        
        # Create indexes
        await collection.create_index("endpoint_id", unique=True)
        await collection.create_index("category")
        await collection.create_index("tags")
        await collection.create_index("method")
        
        return {
            "seeded": len(docs),
            "categories": list(set(e.category for e in API_DOCUMENTATION)),
            "methods": list(set(e.method.value for e in API_DOCUMENTATION))
        }
    
    async def get_all(self, lang: str = "en") -> List[Dict]:
        """Get all documentation"""
        if self.db is None:
            return self._get_from_memory(lang)
        
        cursor = self.db[self.collection_name].find({}, {"_id": 0})
        docs = await cursor.to_list(100)
        return self._localize(docs, lang)
    
    async def get_by_category(self, category: str, lang: str = "en") -> List[Dict]:
        """Get documentation by category"""
        if self.db is None:
            return [
                self._localize_single(e, lang)
                for e in API_DOCUMENTATION
                if e.category == category
            ]
        
        cursor = self.db[self.collection_name].find(
            {"category": category},
            {"_id": 0}
        )
        docs = await cursor.to_list(50)
        return self._localize(docs, lang)
    
    async def get_by_endpoint(self, endpoint_id: str, lang: str = "en") -> Optional[Dict]:
        """Get single endpoint documentation"""
        if self.db is None:
            for e in API_DOCUMENTATION:
                if e.endpoint_id == endpoint_id:
                    return self._localize_single(e, lang)
            return None
        
        doc = await self.db[self.collection_name].find_one(
            {"endpoint_id": endpoint_id},
            {"_id": 0}
        )
        return self._localize_single(doc, lang) if doc else None
    
    async def search(self, query: str, lang: str = "en") -> List[Dict]:
        """Search documentation"""
        if self.db is None:
            q = query.lower()
            results = []
            for e in API_DOCUMENTATION:
                if (q in e.title_en.lower() or q in e.title_ru.lower() or
                    q in e.description_en.lower() or q in e.path.lower() or
                    any(q in tag for tag in e.tags)):
                    results.append(self._localize_single(e, lang))
            return results
        
        cursor = self.db[self.collection_name].find(
            {
                "$or": [
                    {"title_en": {"$regex": query, "$options": "i"}},
                    {"title_ru": {"$regex": query, "$options": "i"}},
                    {"description_en": {"$regex": query, "$options": "i"}},
                    {"path": {"$regex": query, "$options": "i"}},
                    {"tags": {"$regex": query, "$options": "i"}}
                ]
            },
            {"_id": 0}
        )
        docs = await cursor.to_list(50)
        return self._localize(docs, lang)
    
    def _get_from_memory(self, lang: str) -> List[Dict]:
        """Get documentation from memory (fallback)"""
        return [self._localize_single(e, lang) for e in API_DOCUMENTATION]
    
    def _localize(self, docs: List[Dict], lang: str) -> List[Dict]:
        """Localize list of documents"""
        return [self._localize_single(d, lang) for d in docs]
    
    def _localize_single(self, doc: Any, lang: str) -> Dict:
        """Localize single document"""
        if isinstance(doc, ApiEndpoint):
            doc = {
                "endpoint_id": doc.endpoint_id,
                "path": doc.path,
                "method": doc.method.value,
                "title_en": doc.title_en,
                "title_ru": doc.title_ru,
                "description_en": doc.description_en,
                "description_ru": doc.description_ru,
                "category": doc.category,
                "tags": doc.tags,
                "parameters": [
                    {
                        "name": p.name,
                        "type": p.type,
                        "required": p.required,
                        "location": p.location,
                        "description_en": p.description_en,
                        "description_ru": p.description_ru,
                        "default": p.default,
                        "example": p.example
                    }
                    for p in doc.parameters
                ],
                "responses": [
                    {
                        "status_code": r.status_code,
                        "description_en": r.description_en,
                        "description_ru": r.description_ru,
                        "example": r.example
                    }
                    for r in doc.responses
                ]
            }
        
        if not doc:
            return doc
        
        # Select language-specific fields
        title_key = f"title_{lang}" if f"title_{lang}" in doc else "title_en"
        desc_key = f"description_{lang}" if f"description_{lang}" in doc else "description_en"
        
        result = {
            "endpoint_id": doc.get("endpoint_id"),
            "path": doc.get("path"),
            "method": doc.get("method"),
            "title": doc.get(title_key, doc.get("title_en")),
            "description": doc.get(desc_key, doc.get("description_en")),
            "category": doc.get("category"),
            "tags": doc.get("tags", []),
            "parameters": [],
            "responses": []
        }
        
        # Localize parameters
        for p in doc.get("parameters", []):
            p_desc_key = f"description_{lang}" if f"description_{lang}" in p else "description_en"
            result["parameters"].append({
                "name": p.get("name"),
                "type": p.get("type"),
                "required": p.get("required"),
                "location": p.get("location"),
                "description": p.get(p_desc_key, p.get("description_en")),
                "default": p.get("default"),
                "example": p.get("example")
            })
        
        # Localize responses
        for r in doc.get("responses", []):
            r_desc_key = f"description_{lang}" if f"description_{lang}" in r else "description_en"
            result["responses"].append({
                "status_code": r.get("status_code"),
                "description": r.get(r_desc_key, r.get("description_en")),
                "example": r.get("example")
            })
        
        return result


# Singleton
_registry: Optional[ApiDocumentationRegistry] = None


def init_api_registry(db):
    """Initialize API documentation registry"""
    global _registry
    _registry = ApiDocumentationRegistry(db)
    return _registry


def get_api_registry():
    """Get API documentation registry"""
    return _registry
