# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ┃  ADVANCED CACHE SYSTEM - Fast Metadata Caching                     ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import time
from typing import Dict, Any, Optional
from collections import OrderedDict
import asyncio

class FastCache:
    """Ultra-fast in-memory cache with TTL support"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache: OrderedDict = OrderedDict()
        self.ttl = ttl  # Time to live in seconds
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with TTL check"""
        async with self._lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            value, timestamp = self.cache[key]
            
            # Check if expired
            if time.time() - timestamp > self.ttl:
                del self.cache[key]
                self.misses += 1
                return None
            
            # Move to end (LRU)
            self.cache.move_to_end(key)
            self.hits += 1
            return value
    
    async def set(self, key: str, value: Any) -> None:
        """Set value in cache with timestamp"""
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
            
            # Remove oldest if max size reached
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
            
            self.cache[key] = (value, time.time())
    
    async def delete(self, key: str) -> None:
        """Delete key from cache"""
        async with self._lock:
            self.cache.pop(key, None)
    
    async def clear(self) -> None:
        """Clear entire cache"""
        async with self._lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

# Global cache instances
METADATA_CACHE = FastCache(max_size=500, ttl=1800)  # 30 minutes
SEARCH_CACHE = FastCache(max_size=300, ttl=900)     # 15 minutes
PLAYLIST_CACHE = FastCache(max_size=200, ttl=3600)  # 1 hour
JIOSAAVN_CACHE = FastCache(max_size=100, ttl=600)   # 10 minutes

async def cache_metadata(video_id: str, data: Dict) -> None:
    """Cache video metadata"""
    await METADATA_CACHE.set(video_id, data)

async def get_cached_metadata(video_id: str) -> Optional[Dict]:
    """Get cached metadata"""
    return await METADATA_CACHE.get(video_id)

async def cache_search(query: str, results: list) -> None:
    """Cache search results"""
    await SEARCH_CACHE.set(query.lower(), results)

async def get_cached_search(query: str) -> Optional[list]:
    """Get cached search results"""
    return await SEARCH_CACHE.get(query.lower())

async def cache_playlist(playlist_id: str, tracks: list) -> None:
    """Cache playlist data"""
    await PLAYLIST_CACHE.set(playlist_id, tracks)

async def get_cached_playlist(playlist_id: str) -> Optional[list]:
    """Get cached playlist"""
    return await PLAYLIST_CACHE.get(playlist_id)

async def cache_jiosaavn(query: str, file_path: str) -> None:
    """Cache JioSaavn download"""
    await JIOSAAVN_CACHE.set(query.lower(), file_path)

async def get_cached_jiosaavn(query: str) -> Optional[str]:
    """Get cached JioSaavn file"""
    return await JIOSAAVN_CACHE.get(query.lower())
