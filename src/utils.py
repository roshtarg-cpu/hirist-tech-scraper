"""Utility functions for Hirist scraper."""
import httpx
from typing import Optional, Dict, Any
from apify import Actor


async def fetch_json(url: str, params: Optional[Dict] = None, client: Optional[httpx.AsyncClient] = None) -> Optional[Dict[str, Any]]:
    """Fetch JSON data from URL with retries."""
    close_client = False
    if client is None:
        client = httpx.AsyncClient(timeout=30.0)
        close_client = True
    
    try:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        for attempt in range(3):
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                if attempt == 2:
                    Actor.log.error(f'Failed to fetch {url} after 3 attempts: {e}')
                    return None
                Actor.log.warning(f'Attempt {attempt + 1} failed for {url}: {e}')
                await httpx.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    finally:
        if close_client:
            await client.aclose()
