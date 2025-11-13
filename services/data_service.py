import httpx
from typing import List, Dict, Any
from app.config import settings


class MemberDataService:
    """Service to fetch and cache member messages from the API."""
    
    def __init__(self):
        self.api_url = settings.member_api_url
        self._cache = None
    
    async def fetch_messages(self) -> List[Dict[str, Any]]:
        """Fetch all messages from the member API."""
        if self._cache is not None:
            return self._cache
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Fetch all messages with a high limit (API has 3349 messages)
            response = await client.get(f"{self.api_url}/messages?limit=5000")
            response.raise_for_status()
            data = response.json()
            self._cache = data.get("items", [])
            return self._cache
    
    def clear_cache(self):
        """Clear the cached messages."""
        self._cache = None
