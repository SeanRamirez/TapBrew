"""Load brewery data from OpenBreweryDB API."""

from typing import Any

import httpx

from src.utils.logger import logger

OPENBREWERYDB_URL = "https://api.openbrewerydb.org/v1/breweries"


async def fetch_breweries(limit: int = 50, state: str | None = None) -> list[dict[str, Any]]:
    """Fetch breweries from OpenBreweryDB.

    Args:
        limit: Maximum number of breweries to fetch.
        state: Optional US state to filter by.

    Returns:
        List of brewery dictionaries.
    """
    params = {"per_page": min(limit, 200)}
    if state:
        params["by_state"] = state

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENBREWERYDB_URL, params=params)
            response.raise_for_status()
            breweries = response.json()
            logger.info(f"Fetched {len(breweries)} breweries from OpenBreweryDB")
            return breweries
        except httpx.HTTPError as e:
            logger.error(f"Error fetching breweries: {e}")
            return []


def transform_brewery(raw: dict[str, Any]) -> dict[str, Any]:
    """Transform raw brewery data to internal format.

    Args:
        raw: Raw brewery data from API.

    Returns:
        Transformed brewery dictionary.
    """
    return {
        "id": raw.get("id"),
        "name": raw.get("name"),
        "brewery_type": raw.get("brewery_type"),
        "city": raw.get("city"),
        "state": raw.get("state"),
        "postal_code": raw.get("postal_code"),
        "country": raw.get("country", "United States"),
        "latitude": raw.get("latitude"),
        "longitude": raw.get("longitude"),
    }
