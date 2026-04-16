# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ┃  EXTREME OPTIMIZATION UTILITIES - Fast Processing                  ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import asyncio
import time
from typing import Callable, Any, Optional, List
from functools import wraps

class OptimizedSearch:
    """Parallel optimized search with fallbacks"""
    
    @staticmethod
    async def fast_youtube_search(query: str, timeout: int = 5) -> Optional[dict]:
        """Fast YouTube search with timeout"""
        try:
            from SecretMusic import YouTube
            from SecretMusic.utils.cache import get_cached_search, cache_search
            
            # Check cache first
            cached = await get_cached_search(query)
            if cached:
                return cached[0] if cached else None
            
            # Fetch with timeout
            search_task = YouTube.track(query)
            try:
                result, track_id = await asyncio.wait_for(search_task, timeout=timeout)
                # Cache result
                await cache_search(query, [result])
                return result
            except asyncio.TimeoutError:
                return None
        except Exception:
            return None
    
    @staticmethod
    async def fast_jiosaavn_search(query: str, timeout: int = 8) -> Optional[str]:
        """Fast JioSaavn search with timeout"""
        try:
            from SecretMusic.utils.cache import get_cached_jiosaavn, cache_jiosaavn
            from SecretMusic.utils.stream.stream import get_jiosaavn_link
            
            # Check cache
            cached = await get_cached_jiosaavn(query)
            if cached:
                return cached
            
            # Search with timeout
            search_task = get_jiosaavn_link(query)
            try:
                file_path, success = await asyncio.wait_for(search_task, timeout=timeout)
                if file_path and success:
                    await cache_jiosaavn(query, file_path)
                    return file_path
            except asyncio.TimeoutError:
                return None
        except Exception:
            return None

class FastResponses:
    """Fast message handling with minimal edits"""
    
    @staticmethod
    async def quick_reply(message, text: str, reply_markup=None):
        """Send quick response"""
        try:
            return await message.reply_text(text, reply_markup=reply_markup)
        except:
            return None
    
    @staticmethod
    async def quick_edit(msg, text: str, reply_markup=None):
        """Edit with single operation"""
        try:
            await msg.edit_text(text, reply_markup=reply_markup)
        except:
            pass
    
    @staticmethod
    async def safe_delete(msg):
        """Safe delete without errors"""
        try:
            await msg.delete()
        except:
            pass

def optimize_timeout(timeout_seconds: int = 10):
    """Decorator to add timeout to async functions"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=timeout_seconds
                )
            except asyncio.TimeoutError:
                raise TimeoutError(f"Operation timed out after {timeout_seconds} seconds")
        return wrapper
    return decorator

async def parallel_execute(tasks: List[tuple], timeout: int = 30) -> list:
    """Execute multiple tasks in parallel with timeout"""
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*[task for task, _ in tasks], return_exceptions=True),
            timeout=timeout
        )
        return results
    except asyncio.TimeoutError:
        return [None] * len(tasks)

class SmartBitrate:
    """Dynamically adjust bitrate based on conditions"""
    
    @staticmethod
    def get_optimal_bitrate(file_size_bytes: int, duration_seconds: int) -> str:
        """Calculate optimal bitrate to reduce load"""
        if file_size_bytes < 5242880:  # < 5MB
            return "64"  # Very low bitrate
        elif file_size_bytes < 20971520:  # < 20MB
            return "96"
        elif file_size_bytes < 52428800:  # < 50MB
            return "128"
        else:
            return "96"  # Default low

class CacheManager:
    """Manage cache cleanup and optimization"""
    
    @staticmethod
    async def cleanup_old_cache(max_age_seconds: int = 3600):
        """Cleanup cache older than max_age"""
        from SecretMusic.utils.cache import METADATA_CACHE, SEARCH_CACHE
        
        current_time = time.time()
        for cache in [METADATA_CACHE, SEARCH_CACHE]:
            expired_keys = []
            for key, (_, timestamp) in cache.cache.items():
                if current_time - timestamp > max_age_seconds:
                    expired_keys.append(key)
            
            for key in expired_keys:
                await cache.delete(key)

# Performance metrics
class PerformanceMetrics:
    """Track performance metrics"""
    
    _metrics = {
        "searches": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "avg_response_time": 0,
    }
    
    @staticmethod
    def record_search(duration: float):
        """Record search operation"""
        PerformanceMetrics._metrics["searches"] += 1
        total_time = PerformanceMetrics._metrics["avg_response_time"] * (PerformanceMetrics._metrics["searches"] - 1)
        PerformanceMetrics._metrics["avg_response_time"] = (total_time + duration) / PerformanceMetrics._metrics["searches"]
    
    @staticmethod
    def get_metrics() -> dict:
        """Get current metrics"""
        return PerformanceMetrics._metrics.copy()
