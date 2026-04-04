# Social Media Automation Skill

## Purpose
Implementation skill for digital presence. Automates scheduled posts and engagement summaries for LinkedIn, Twitter (X), Facebook, and Instagram using browser automation or dedicated API connectors.

## Capabilities

### Platform Support Matrix
| Platform | Method | Capabilities | Limitations |
|----------|--------|--------------|-------------|
| LinkedIn | API v2 | Posts, articles, comments | Rate limits, no DM |
| Twitter/X | API v2 | Tweets, threads, replies | Paid tier required |
| Facebook | Graph API | Posts, pages, groups | App review required |
| Instagram | Graph API | Posts, stories, reels | Business account only |
| All | Playwright | Universal fallback | Session management, CAPTCHA risk |

### Post Scheduling System
```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ScheduledPost:
    id: str
    platform: str  # linkedin, twitter, facebook, instagram
    content: str
    media: List[str]  # paths to images/videos
    scheduled_time: datetime
    status: str  # draft, scheduled, posted, failed
    tags: List[str]
    
    def to_markdown(self) -> str:
        return f"""---
id: {self.id}
platform: {self.platform}
scheduled_time: {self.scheduled_time.isoformat()}
status: {self.status}
tags: [{', '.join(self.tags)}]
---

# {self.platform.title()} Post

## Content
{self.content}

## Media
{self._format_media()}

## Posted At
{self.posted_at or 'Not yet posted'}
"""
```

### Content Queue Management
```markdown
---
queue_name: March_2026_Content
created: 2026-03-01
platforms: [linkedin, twitter]
---

## Scheduled Posts

### Post 001
- Platform: LinkedIn
- Scheduled: 2026-03-28T09:00:00Z
- Status: posted
- Content: "Excited to announce..."

### Post 002
- Platform: Twitter
- Scheduled: 2026-03-28T14:00:00Z
- Status: scheduled
- Content: "🚀 New feature alert!..."

### Post 003
- Platform: LinkedIn
- Scheduled: 2026-03-29T10:00:00Z
- Status: draft
- Content: "Weekend reflection:..."
```

### LinkedIn Integration
```python
class LinkedInClient:
    def __init__(self, access_token: str, organization_id: str):
        self.base_url = "https://api.linkedin.com/v2"
        self.access_token = access_token
        self.org_id = organization_id
    
    def create_post(self, content: str, media_urls: List[str] = None) -> Dict:
        """Create a post on LinkedIn."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        payload = {
            "author": f"urn:li:organization:{self.org_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": "PUBLIC"
        }
        
        if media_urls:
            # Upload media first, then reference in payload
            media_ids = [self._upload_media(url) for url in media_urls]
            payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
            payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {"media": f"urn:li:image:{mid}", "status": "READY"}
                for mid in media_ids
            ]
        
        response = requests.post(
            f"{self.base_url}/ugcPosts",
            headers=headers,
            json=payload
        )
        return response.json()
```

### Twitter/X Integration
```python
class TwitterClient:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_secret: str):
        import tweepy
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
    
    def create_tweet(self, content: str, media_paths: List[str] = None) -> Dict:
        """Create a tweet, optionally with media."""
        media_ids = []
        if media_paths:
            for path in media_paths:
                media = self.client.media_upload(filename=path)
                media_ids.append(media.media_id)
        
        response = self.client.create_tweet(
            text=content,
            media_ids=media_ids if media_ids else None
        )
        return response.data
```

### Facebook/Instagram Integration
```python
class MetaClient:
    def __init__(self, access_token: str, instagram_business_id: str, page_id: str):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = access_token
        self.ig_business_id = instagram_business_id
        self.page_id = page_id
    
    def create_instagram_post(self, caption: str, image_url: str) -> Dict:
        """Create an Instagram post."""
        # Step 1: Create container
        create_url = f"{self.base_url}/{self.ig_business_id}/media"
        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        response = requests.post(create_url, params=params)
        creation_id = response.json()['id']
        
        # Step 2: Publish container
        publish_url = f"{self.base_url}/{self.ig_business_id}/media_publish"
        params = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        response = requests.post(publish_url, params=params)
        return response.json()
```

### Playwright Fallback (Universal)
```python
from playwright.async_api import async_playwright

class SocialMediaBrowser:
    def __init__(self, session_dir: str):
        self.session_dir = session_dir
        self.browser = None
        self.context = None
    
    async def start(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(
            storage_state=f"{self.session_dir}/storage.json"
        )
    
    async def post_to_linkedin(self, content: str):
        page = await self.context.new_page()
        await page.goto("https://www.linkedin.com/feed/")
        await page.wait_for_selector('.share-box-feed-entry__trigger')
        
        # Click share button
        await page.click('.share-box-feed-entry__trigger')
        await page.wait_for_selector('.ql-editor')
        
        # Type content
        await page.fill('.ql-editor', content)
        
        # Click post
        await page.click('button:has-text("Post")')
        await page.wait_for_load_state('networkidle')
    
    async def save_session(self):
        await self.context.storage_state(path=f"{self.session_dir}/storage.json")
```

### Engagement Summary Generation
```python
def generate_engagement_summary(platform: str, days: int = 7) -> Dict:
    """Generate engagement summary for the past N days."""
    # Platform-specific metrics
    metrics = {
        "posts": count_posts(platform, days),
        "likes": sum_likes(platform, days),
        "comments": sum_comments(platform, days),
        "shares": sum_shares(platform, days),
        "impressions": sum_impressions(platform, days),
        "engagement_rate": calculate_engagement_rate(platform, days)
    }
    
    # Top performing posts
    top_posts = get_top_posts(platform, days, limit=5)
    
    return {
        "platform": platform,
        "period_days": days,
        "generated_at": datetime.now().isoformat(),
        "metrics": metrics,
        "top_posts": top_posts,
        "recommendations": generate_recommendations(metrics)
    }
```

### Summary Report Format
```markdown
---
report_type: engagement_summary
platform: linkedin
period_days: 7
generated_at: 2026-03-28T10:00:00Z
---

# LinkedIn Engagement Summary - Last 7 Days

## Metrics
| Metric | Value | Change |
|--------|-------|--------|
| Posts | 5 | +2 |
| Likes | 342 | +15% |
| Comments | 28 | +5% |
| Shares | 12 | -3% |
| Impressions | 8,450 | +22% |
| Engagement Rate | 4.5% | +8% |

## Top Posts
1. "Excited to announce our new..." - 156 likes, 23 comments
2. "Weekend reflection on..." - 98 likes, 15 comments
3. "🚀 Feature alert:..." - 88 likes, 10 comments

## Recommendations
- Post more technical content (higher engagement)
- Optimal posting time: 9-10 AM weekdays
- Consider video content for higher reach
```

## Configuration
```yaml
social_media:
  linkedin:
    enabled: true
    method: api
    access_token: "${LINKEDIN_ACCESS_TOKEN}"
    organization_id: "${LINKEDIN_ORG_ID}"
    post_frequency: daily
    optimal_times: ["09:00", "14:00", "17:00"]
  
  twitter:
    enabled: true
    method: api
    api_key: "${TWITTER_API_KEY}"
    api_secret: "${TWITTER_API_SECRET}"
    access_token: "${TWITTER_ACCESS_TOKEN}"
    access_secret: "${TWITTER_ACCESS_SECRET}"
  
  instagram:
    enabled: false
    method: api
    access_token: "${META_ACCESS_TOKEN}"
    business_id: "${INSTAGRAM_BUSINESS_ID}"
  
  fallback:
    method: playwright
    session_dir: "./sessions/social"
    browser: chromium
```

## Error Handling
- API rate limits: Queue posts, retry after cooldown
- Session expired (Playwright): Notify user for re-authentication
- Media upload failure: Retry with compressed version
- Content too long: Truncate with ellipsis, flag for review
- Platform outage: Queue locally, retry on recovery

## Security
- API credentials in `.env` only
- Session files encrypted at rest
- Never post sensitive financial/HR information
- HITL approval required for first post to new platform
- Audit log of all posted content
