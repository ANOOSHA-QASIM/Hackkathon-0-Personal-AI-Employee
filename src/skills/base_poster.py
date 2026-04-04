"""
Base Poster - Abstract base class for all platform posting skills.

All platform skills (LinkedIn, Meta, Twitter) MUST inherit from this class
to ensure consistent interface, logging, and error handling.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from datetime import datetime


class PostingResult:
    """Result of a posting attempt to a single platform."""
    
    def __init__(
        self,
        platform: str,
        status: str,  # 'pending', 'published', 'failed', 'retrying'
        url: Optional[str] = None,
        published_at: Optional[str] = None,
        error: Optional[str] = None,
        retry_count: int = 0,
        next_retry_at: Optional[str] = None
    ):
        self.platform = platform
        self.status = status
        self.url = url
        self.published_at = published_at
        self.error = error
        self.retry_count = retry_count
        self.next_retry_at = next_retry_at
    
    def to_dict(self) -> dict:
        """Convert to dictionary for metadata storage."""
        return {
            'status': self.status,
            'url': self.url,
            'published_at': self.published_at,
            'error': self.error,
            'retry_count': self.retry_count,
            'next_retry_at': self.next_retry_at,
        }


class BasePoster(ABC):
    """
    Abstract base class for all platform posting skills.
    
    Subclasses MUST implement:
    - post(): Publish content to platform
    - authenticate(): Manual authentication (first time only)
    """
    
    def __init__(self, platform_name: str, user_data_dir: Path):
        """
        Initialize platform poster.
        
        Args:
            platform_name: Name of platform (e.g., 'linkedin', 'meta', 'twitter')
            user_data_dir: Path to persistent browser session directory
        """
        self.platform_name = platform_name
        self.user_data_dir = user_data_dir
        self.context = None
        self.is_authenticated = False
    
    @abstractmethod
    def post(self, content: str, media_path: Optional[str] = None) -> PostingResult:
        """
        Post content to platform.
        
        Args:
            content: Post text content
            media_path: Optional path to image/media file
        
        Returns:
            PostingResult with status, URL, timestamps, errors
        """
        pass
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with platform (manual login).
        
        Returns:
            True if authentication successful
        """
        pass
    
    def _launch_browser(self):
        """Launch browser with persistent session."""
        from playwright.sync_api import sync_playwright
        
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        playwright = sync_playwright().start()
        self.context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            timeout=90000  # 90s timeout for slow internet
        )
        
        return self.context.pages[0] if self.context.pages else self.context.new_page()
    
    def close(self):
        """Close browser context."""
        if self.context:
            self.context.close()
            self.context = None
    
    def _validate_content(self, content: str, max_length: int = 3000) -> bool:
        """Validate content length."""
        if not content or len(content.strip()) == 0:
            return False
        if len(content) > max_length:
            return False
        return True
    
    def _validate_media(self, media_path: Optional[str]) -> bool:
        """Validate media file exists."""
        if not media_path:
            return True  # No media is valid
        return Path(media_path).exists()
