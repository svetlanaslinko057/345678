"""
API Documentation Routes

Provides bilingual API documentation from MongoDB.
"""

from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/docs", tags=["documentation"])


def get_registry():
    """Get documentation registry"""
    from server import db
    from .documentation_registry import init_api_registry, get_api_registry
    registry = get_api_registry()
    if registry is None:
        registry = init_api_registry(db)
    return registry


@router.get("/")
async def get_all_documentation(
    lang: str = Query("en", description="Language: en or ru")
):
    """
    Get all API documentation.
    
    Language options:
    - en: English (default)
    - ru: Russian
    """
    registry = get_registry()
    docs = await registry.get_all(lang)
    
    return {
        "ts": int(datetime.now(timezone.utc).timestamp() * 1000),
        "lang": lang,
        "count": len(docs),
        "endpoints": docs
    }


@router.get("/category/{category}")
async def get_by_category(
    category: str,
    lang: str = Query("en", description="Language: en or ru")
):
    """
    Get documentation by category.
    
    Categories: entity, query, correlation, trust, exchange, system
    """
    registry = get_registry()
    docs = await registry.get_by_category(category, lang)
    
    return {
        "ts": int(datetime.now(timezone.utc).timestamp() * 1000),
        "category": category,
        "lang": lang,
        "count": len(docs),
        "endpoints": docs
    }


@router.get("/endpoint/{endpoint_id}")
async def get_endpoint_docs(
    endpoint_id: str,
    lang: str = Query("en", description="Language: en or ru")
):
    """
    Get documentation for specific endpoint.
    """
    registry = get_registry()
    doc = await registry.get_by_endpoint(endpoint_id, lang)
    
    if not doc:
        return {
            "ts": int(datetime.now(timezone.utc).timestamp() * 1000),
            "error": "Endpoint not found",
            "endpoint_id": endpoint_id
        }
    
    return {
        "ts": int(datetime.now(timezone.utc).timestamp() * 1000),
        "lang": lang,
        "endpoint": doc
    }


@router.get("/search")
async def search_documentation(
    q: str = Query(..., min_length=1, description="Search query"),
    lang: str = Query("en", description="Language: en or ru")
):
    """
    Search API documentation.
    
    Searches in titles, descriptions, paths, and tags.
    """
    registry = get_registry()
    docs = await registry.search(q, lang)
    
    return {
        "ts": int(datetime.now(timezone.utc).timestamp() * 1000),
        "query": q,
        "lang": lang,
        "count": len(docs),
        "results": docs
    }


@router.post("/seed")
async def seed_documentation():
    """
    Seed database with API documentation.
    
    Populates api_documentation collection with structured docs.
    """
    registry = get_registry()
    result = await registry.seed_documentation()
    
    return {
        "ts": int(datetime.now(timezone.utc).timestamp() * 1000),
        "ok": True,
        **result
    }


@router.get("/categories")
async def list_categories():
    """
    Get list of documentation categories.
    """
    categories = [
        {"id": "entity", "name_en": "Entity Intelligence", "name_ru": "Интеллект сущностей"},
        {"id": "query", "name_en": "Query Engine", "name_ru": "Движок запросов"},
        {"id": "correlation", "name_en": "Event Correlation", "name_ru": "Корреляция событий"},
        {"id": "trust", "name_en": "Source Trust", "name_ru": "Доверие источников"},
        {"id": "exchange", "name_en": "Exchange Data", "name_ru": "Биржевые данные"},
        {"id": "system", "name_en": "System", "name_ru": "Система"}
    ]
    
    return {
        "ts": int(datetime.now(timezone.utc).timestamp() * 1000),
        "categories": categories
    }
