# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ┃  RELIABILITY & ERROR HANDLING - Enterprise-grade stability            ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import asyncio
import time
from typing import Optional, Callable, Any
from functools import wraps
from datetime import datetime, timedelta

class ErrorRecovery:
    """Smart error recovery with exponential backoff"""
    
    def __init__(self):
        self.error_counts = {}
        self.last_error_time = {}
        self.max_retries = 3
        self.base_delay = 1  # seconds
    
    async def retry_with_backoff(self, func: Callable, max_attempts: int = 3, timeout: int = 30) -> Any:
        """Retry function with exponential backoff"""
        for attempt in range(max_attempts):
            try:
                return await asyncio.wait_for(func(), timeout=timeout)
            except asyncio.TimeoutError:
                if attempt == max_attempts - 1:
                    raise
                delay = self.base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise
                delay = self.base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
        
        return None
    
    def track_error(self, key: str):
        """Track error occurrence"""
        self.error_counts[key] = self.error_counts.get(key, 0) + 1
        self.last_error_time[key] = time.time()
    
    def should_skip_retry(self, key: str, max_threshold: int = 5) -> bool:
        """Check if should skip retrying"""
        count = self.error_counts.get(key, 0)
        if count > max_threshold:
            # Check if enough time has passed
            last_time = self.last_error_time.get(key, 0)
            if time.time() - last_time < 300:  # 5 minutes
                return True
        return False
    
    def reset_error_count(self, key: str):
        """Reset error counter"""
        self.error_counts[key] = 0
        self.last_error_time.pop(key, None)

class SafeOperations:
    """Safe operation wrappers"""
    
    @staticmethod
    async def safe_download(download_func: Callable, video_id: str, max_size_mb: int = 100) -> Optional[str]:
        """Download with safety checks"""
        try:
            result = await asyncio.wait_for(download_func(), timeout=120)
            if result and isinstance(result, str):
                # Verify file size
                import os
                if os.path.exists(result):
                    file_size_mb = os.path.getsize(result) / (1024 * 1024)
                    if file_size_mb > max_size_mb:
                        os.remove(result)
                        return None
                return result
        except asyncio.TimeoutError:
            return None
        except Exception:
            return None
        return None
    
    @staticmethod
    async def safe_stream(stream_func: Callable, timeout: int = 60) -> bool:
        """Stream with error handling"""
        try:
            await asyncio.wait_for(stream_func(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False
        except Exception:
            return False

class HealthCheck:
    """System health monitoring"""
    
    def __init__(self):
        self.last_check = {}
        self.status = {}
    
    async def check_service(self, service_name: str, check_func: Callable) -> bool:
        """Check service health"""
        try:
            result = await asyncio.wait_for(check_func(), timeout=10)
            self.status[service_name] = "healthy"
            self.last_check[service_name] = time.time()
            return True
        except Exception:
            self.status[service_name] = "unhealthy"
            return False
    
    def get_status(self) -> dict:
        """Get overall system status"""
        return {
            "services": self.status.copy(),
            "timestamp": datetime.now().isoformat()
        }

class RateLimiter:
    """Prevent API rate limiting"""
    
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.request_times = {}
    
    async def acquire(self, service: str) -> bool:
        """Check if we can make a request"""
        now = time.time()
        one_minute_ago = now - 60
        
        if service not in self.request_times:
            self.request_times[service] = []
        
        # Clean old requests
        self.request_times[service] = [
            t for t in self.request_times[service] if t > one_minute_ago
        ]
        
        # Check limit
        if len(self.request_times[service]) >= self.requests_per_minute:
            return False
        
        self.request_times[service].append(now)
        return True
    
    async def wait_if_needed(self, service: str):
        """Wait if rate limited"""
        while not await self.acquire(service):
            await asyncio.sleep(1)

# Global instances
error_recovery = ErrorRecovery()
rate_limiter = RateLimiter(requests_per_minute=40)
health_check = HealthCheck()

def safe_operation(timeout: int = 30):
    """Decorator for safe operations"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                return None
            except Exception as e:
                return None
        return wrapper
    return decorator
